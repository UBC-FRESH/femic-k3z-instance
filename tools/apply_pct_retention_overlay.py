from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import pandas as pd


VARIANT_OUTPUT_DIRS = {
    "pct_light": "output/patchworks_k3z_pct_light_validated/fragments/fragments.shp",
    "pct_moderate": "output/patchworks_k3z_pct_moderate_validated/fragments/fragments.shp",
    "pct_heavy": "output/patchworks_k3z_pct_heavy_validated/fragments/fragments.shp",
}
DEFAULT_SOURCE_TABLE = "tmp/k3z_pct_thinners_retention_join.csv"
BLOCK_COLUMN = "BLOCK"
RETENTION_COLUMN = "RETENTION"
SOURCE_RETENTION_COLUMN = "retention_thinners"


@dataclass(frozen=True)
class OverlayResult:
    variant_id: str
    fragments_path: Path
    rows: int
    retained_area_before: float
    retained_area_after: float


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the tracked student thinners RETENTION overlay to the three "
            "validated K3Z pct* fragments surfaces."
        )
    )
    parser.add_argument(
        "--instance-root",
        type=Path,
        default=Path("."),
        help="Path to the femic-k3z-instance checkout root.",
    )
    parser.add_argument(
        "--source-table",
        type=Path,
        default=Path(DEFAULT_SOURCE_TABLE),
        help="Tracked normalized block-key retention table.",
    )
    return parser.parse_args()


def _load_source_table(path: Path) -> pd.DataFrame:
    payload = pd.read_csv(path)
    required = {BLOCK_COLUMN, SOURCE_RETENTION_COLUMN}
    missing = sorted(required.difference(payload.columns))
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"Source retention table missing required columns: {missing_text}")

    if payload[BLOCK_COLUMN].duplicated().any():
        raise ValueError("Source retention table contains duplicate BLOCK values.")

    retention = pd.to_numeric(payload[SOURCE_RETENTION_COLUMN], errors="coerce")
    if retention.isna().any():
        raise ValueError("Source retention table contains non-numeric retention values.")
    if ((retention < 0.0) | (retention > 1.0)).any():
        raise ValueError("Source retention table has retention values outside [0, 1].")

    payload = payload.copy()
    payload[SOURCE_RETENTION_COLUMN] = retention.astype(float)
    return payload


def _remove_existing_shapefile_family(path: Path) -> None:
    for suffix in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
        candidate = path.with_suffix(suffix)
        if candidate.exists():
            candidate.unlink()


def _apply_overlay_to_variant(
    *,
    variant_id: str,
    fragments_path: Path,
    source_table: pd.DataFrame,
) -> OverlayResult:
    fragments = gpd.read_file(fragments_path)
    required = {BLOCK_COLUMN, RETENTION_COLUMN, "AREA_HA"}
    missing = sorted(required.difference(fragments.columns))
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(
            f"{variant_id} fragments surface missing required columns: {missing_text}"
        )

    if fragments[BLOCK_COLUMN].duplicated().any():
        raise ValueError(f"{variant_id} fragments surface contains duplicate BLOCK values.")

    retained_area_before = float(
        (
            pd.to_numeric(fragments["AREA_HA"], errors="raise")
            * pd.to_numeric(fragments[RETENTION_COLUMN], errors="raise")
        ).sum()
    )

    merged = fragments.merge(
        source_table[[BLOCK_COLUMN, SOURCE_RETENTION_COLUMN]],
        on=BLOCK_COLUMN,
        how="left",
        validate="1:1",
    )
    if merged[SOURCE_RETENTION_COLUMN].isna().any():
        missing_blocks = merged.loc[merged[SOURCE_RETENTION_COLUMN].isna(), BLOCK_COLUMN].tolist()
        raise ValueError(
            f"{variant_id} fragments surface has BLOCK rows missing from the source table: "
            f"{missing_blocks[:10]}"
        )

    merged[RETENTION_COLUMN] = merged[SOURCE_RETENTION_COLUMN].astype(float)
    merged = merged.drop(columns=[SOURCE_RETENTION_COLUMN])
    retained_area_after = float(
        (
            pd.to_numeric(merged["AREA_HA"], errors="raise")
            * pd.to_numeric(merged[RETENTION_COLUMN], errors="raise")
        ).sum()
    )

    _remove_existing_shapefile_family(fragments_path)
    gpd.GeoDataFrame(merged, geometry="geometry", crs=fragments.crs).to_file(fragments_path)

    return OverlayResult(
        variant_id=variant_id,
        fragments_path=fragments_path,
        rows=len(merged),
        retained_area_before=retained_area_before,
        retained_area_after=retained_area_after,
    )


def main() -> int:
    args = _parse_args()
    instance_root = args.instance_root.expanduser().resolve()
    source_table_path = (instance_root / args.source_table).resolve()
    if not source_table_path.exists():
        raise FileNotFoundError(f"Source retention table not found: {source_table_path}")

    source_table = _load_source_table(source_table_path)

    print(f"instance_root: {instance_root}")
    print(f"source_table: {source_table_path}")
    if "AREA_HA" in source_table.columns:
        source_retained_area = float(
            (
                pd.to_numeric(source_table["retention_thinners"], errors="raise")
                * pd.to_numeric(source_table["AREA_HA"], errors="raise")
            ).sum()
        )
        print(
            f"source_rows: {len(source_table)}  retained_area_ha={source_retained_area:.6f}"
        )
    else:
        print(f"source_rows: {len(source_table)}")

    for variant_id, rel_path in VARIANT_OUTPUT_DIRS.items():
        fragments_path = (instance_root / rel_path).resolve()
        result = _apply_overlay_to_variant(
            variant_id=variant_id,
            fragments_path=fragments_path,
            source_table=source_table,
        )
        print(
            f"{result.variant_id}: rows={result.rows} "
            f"retained_area_before={result.retained_area_before:.6f} "
            f"retained_area_after={result.retained_area_after:.6f} "
            f"path={result.fragments_path}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
