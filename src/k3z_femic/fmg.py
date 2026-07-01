"""K3Z FMG auxiliary data provider."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import numpy as np
import pandas as pd
from femic.fmg import (
    AnalysisUnitDefinition,
    BundleAuxiliaryData,
    BundleAuxiliaryRequest,
    BundleModelContext,
    CurvePoint,
    QmdSupportDefinition,
    build_bundle_model_context,
)
from femic.pipeline.bundle import tsa_curve_id_prefix
from femic.pipeline.tsa import (
    assign_si_levels_from_stratum_quantiles,
    assign_stratum_matches_from_au_table,
    lookup_scsi_au_base,
)
from femic.pipeline.vri import assign_stratum_codes_with_lexmatch

K3Z_TSA_CODE = "k3z"
TIPSY_PARAMS_FILENAME = "tipsy_params_tsak3z.xlsx"
BTC_INPUT_FILENAME = "03_input-tsak3z.csv"
TIPSY_CURVES_FILENAME = "tipsy_curves_tsak3z.csv"
CHECKPOINT_FILENAME = "ria_vri_vclr1p_checkpoint1-tsak3z.feather"
VDYP_LAYER_FILENAME = "vdyp_lyr-tsak3z.feather"

MANAGED_BANK_INDICATOR_COLUMNS = (
    "MAI",
    "BasalArea000",
    "DBHg000",
    "Logs_Grade_D",
    "Logs_Grade_F",
    "Logs_Grade_H",
    "Logs_Grade_I",
    "Logs_Grade_J",
    "Logs_Grade_U",
    "Logs_Grade_X",
    "Logs_Grade_Y",
    "Logs_Grade_All",
    "SPH000",
    "StemCount000",
    "StemCount125",
    "StemCount175",
)


def _coerce_int(value: Any) -> int:
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return int(value)
    return int(str(value))


def _normalize_tsa_code(value: Any) -> str:
    text = str(value).strip()
    if text.isdigit():
        return text.zfill(2)
    return text.lower()


def _derive_local_au_from_namespaced_curve_id(*, tsa: str, curve_id: int) -> int | None:
    prefix = 100000 * tsa_curve_id_prefix(_normalize_tsa_code(tsa))
    local_au = int(curve_id) - prefix
    if local_au <= 0:
        return None
    return int(local_au)


def _resolve_source_managed_local_au_id(au: AnalysisUnitDefinition) -> int | None:
    if au.source_managed_local_au_id is not None:
        return int(au.source_managed_local_au_id)
    if int(au.managed_curve_id) == int(au.unmanaged_curve_id):
        return None
    derived = _derive_local_au_from_namespaced_curve_id(
        tsa=au.tsa,
        curve_id=int(au.managed_curve_id),
    )
    if derived is not None and derived != int(au.managed_curve_id):
        return int(derived)
    return None


def load_site_index_by_au_from_tipsy_input(data_dir: Path) -> dict[int, float]:
    """Load K3Z TIPSY site-index support keyed by local AU."""
    workbook_path = data_dir / TIPSY_PARAMS_FILENAME
    if not workbook_path.is_file():
        return {}
    input_df = pd.read_excel(
        workbook_path,
        sheet_name="TIPSY_inputTBL",
        usecols=["AU", "SI"],
    )
    input_df["AU"] = pd.to_numeric(input_df["AU"], errors="coerce")
    input_df["SI"] = pd.to_numeric(input_df["SI"], errors="coerce")
    input_df = input_df.dropna(subset=["AU", "SI"])
    if input_df.empty:
        return {}
    return {
        _coerce_int(au): float(si)
        for au, si in input_df.groupby("AU")["SI"].median().items()
        if np.isfinite(float(si))
    }


def load_managed_stems_per_ha_by_au_from_btc_input(data_dir: Path) -> dict[int, float]:
    """Load K3Z planted/natural density support keyed by local AU."""
    input_path = data_dir / BTC_INPUT_FILENAME
    if not input_path.is_file():
        return {}
    input_df = pd.read_csv(input_path)
    if "feature_id" not in input_df.columns:
        return {}
    density_cols = [
        column
        for column in input_df.columns
        if column.startswith("planted_density") or column.startswith("natural_density")
    ]
    if not density_cols:
        return {}
    input_df["feature_id"] = pd.to_numeric(input_df["feature_id"], errors="coerce")
    for column in density_cols:
        input_df[column] = pd.to_numeric(input_df[column], errors="coerce").fillna(0.0)
    input_df = input_df.dropna(subset=["feature_id"])
    if input_df.empty:
        return {}
    input_df["managed_stems_per_ha"] = input_df.loc[:, density_cols].sum(axis=1)
    summary = (
        input_df.groupby("feature_id", as_index=False)
        .agg(managed_stems_per_ha=("managed_stems_per_ha", "median"))
        .dropna(subset=["managed_stems_per_ha"])
    )
    summary["managed_stems_per_ha"] = pd.to_numeric(
        summary["managed_stems_per_ha"], errors="coerce"
    )
    return {
        _coerce_int(row.feature_id): float(cast(float, managed_stems_per_ha))
        for row in summary.itertuples(index=False)
        for managed_stems_per_ha in [row.managed_stems_per_ha]
        if pd.notna(managed_stems_per_ha)
        and np.isfinite(float(cast(float, managed_stems_per_ha)))
        and float(cast(float, managed_stems_per_ha)) > 0.0
    }


def load_managed_qmd_support_from_tipsy(
    *,
    data_dir: Path,
    analysis_units: tuple[AnalysisUnitDefinition, ...],
) -> dict[int, QmdSupportDefinition]:
    """Load K3Z managed QMD support from TIPSY curves."""
    tipsy_path = data_dir / TIPSY_CURVES_FILENAME
    if not tipsy_path.is_file():
        return {}
    tipsy_df = pd.read_csv(tipsy_path)
    required = {"AU", "Age", "Yield", "Height", "TPH"}
    if not required.issubset(tipsy_df.columns):
        return {}
    tipsy_df["AU"] = pd.to_numeric(tipsy_df["AU"], errors="coerce")
    tipsy_df["Age"] = pd.to_numeric(tipsy_df["Age"], errors="coerce")
    tipsy_df["Yield"] = pd.to_numeric(tipsy_df["Yield"], errors="coerce")
    tipsy_df["Height"] = pd.to_numeric(tipsy_df["Height"], errors="coerce")
    tipsy_df["TPH"] = pd.to_numeric(tipsy_df["TPH"], errors="coerce")
    tipsy_df = tipsy_df.dropna(subset=["AU", "Age", "Yield"])
    if tipsy_df.empty:
        return {}

    site_index_by_local_au = load_site_index_by_au_from_tipsy_input(data_dir=data_dir)
    managed_stems_per_ha_by_local_au = load_managed_stems_per_ha_by_au_from_btc_input(
        data_dir=data_dir
    )
    grouped = {_coerce_int(au): sub.copy() for au, sub in tipsy_df.groupby("AU")}
    out: dict[int, QmdSupportDefinition] = {}
    for au in analysis_units:
        matched_local_au = _resolve_source_managed_local_au_id(au)
        if matched_local_au is None or matched_local_au not in grouped:
            continue
        matched_rows = grouped[matched_local_au].sort_values("Age")
        height_points = tuple(
            CurvePoint(x=float(age), y=float(height))
            for age, height in zip(
                matched_rows["Age"].tolist(),
                matched_rows["Height"].tolist(),
                strict=False,
            )
            if np.isfinite(float(age)) and np.isfinite(float(height))
        )
        tph_points = tuple(
            CurvePoint(x=float(age), y=float(tph))
            for age, tph in zip(
                matched_rows["Age"].tolist(),
                matched_rows["TPH"].tolist(),
                strict=False,
            )
            if np.isfinite(float(age)) and np.isfinite(float(tph))
        )
        out[int(au.au_id)] = QmdSupportDefinition(
            site_index=site_index_by_local_au.get(matched_local_au),
            unmanaged_stems_per_ha=None,
            managed_stems_per_ha=managed_stems_per_ha_by_local_au.get(matched_local_au),
            managed_height_points=height_points,
            managed_tph_points=tph_points,
        )
    return out


def load_managed_indicator_curves_from_tipsy(
    *,
    data_dir: Path,
    analysis_units: tuple[AnalysisUnitDefinition, ...],
) -> dict[int, dict[str, tuple[CurvePoint, ...]]]:
    """Load K3Z managed indicator curves from TIPSY curve output."""
    tipsy_path = data_dir / TIPSY_CURVES_FILENAME
    if not tipsy_path.is_file():
        return {}
    tipsy_df = pd.read_csv(tipsy_path)
    required = {"AU", "Age", *MANAGED_BANK_INDICATOR_COLUMNS}
    available = required.intersection(set(tipsy_df.columns))
    if not {"AU", "Age"}.issubset(tipsy_df.columns) or len(available) <= 2:
        return {}
    tipsy_df["AU"] = pd.to_numeric(tipsy_df["AU"], errors="coerce")
    tipsy_df["Age"] = pd.to_numeric(tipsy_df["Age"], errors="coerce")
    for column in MANAGED_BANK_INDICATOR_COLUMNS:
        if column in tipsy_df.columns:
            tipsy_df[column] = pd.to_numeric(tipsy_df[column], errors="coerce")
    tipsy_df = tipsy_df.dropna(subset=["AU", "Age"])
    if tipsy_df.empty:
        return {}

    rows_by_local_au = {
        _coerce_int(au): subdf.sort_values("Age").copy() for au, subdf in tipsy_df.groupby("AU")
    }
    out: dict[int, dict[str, tuple[CurvePoint, ...]]] = {}
    for au in analysis_units:
        matched_local_au = _resolve_source_managed_local_au_id(au)
        if matched_local_au is None:
            continue
        managed_rows = rows_by_local_au.get(matched_local_au)
        if managed_rows is None or managed_rows.empty:
            continue
        curves_by_name: dict[str, tuple[CurvePoint, ...]] = {}
        for column in MANAGED_BANK_INDICATOR_COLUMNS:
            if column not in managed_rows.columns:
                continue
            points = tuple(
                CurvePoint(x=float(age), y=float(value))
                for age, value in zip(
                    managed_rows["Age"].tolist(),
                    managed_rows[column].tolist(),
                    strict=False,
                )
                if np.isfinite(float(age)) and pd.notna(value) and np.isfinite(float(value))
            )
            if points:
                curves_by_name[column] = points
        if curves_by_name:
            out[int(au.au_id)] = curves_by_name
    return out


def load_unmanaged_qmd_support_from_checkpoint(
    *,
    data_dir: Path,
    au_table: pd.DataFrame,
) -> dict[int, QmdSupportDefinition]:
    """Load K3Z unmanaged QMD support from checkpoint and VDYP layer artifacts."""
    checkpoint_path = data_dir / CHECKPOINT_FILENAME
    vdyp_layer_path = data_dir / VDYP_LAYER_FILENAME
    if not checkpoint_path.is_file() or not vdyp_layer_path.is_file():
        return {}

    checkpoint = pd.read_feather(checkpoint_path)
    vdyp_lyr = pd.read_feather(vdyp_layer_path)
    if "FEATURE_ID" not in checkpoint.columns or "FEATURE_ID" not in vdyp_lyr.columns:
        return {}

    def _row_apply(table: pd.DataFrame, func: Any, axis: int = 1) -> Any:
        _ = axis
        return table.apply(func, axis=1)

    assigned = checkpoint.copy()
    assigned["tsa_code"] = K3Z_TSA_CODE
    assigned = assign_stratum_codes_with_lexmatch(
        f_table=assigned,
        row_apply_fn=_row_apply,
        bec_grouping="subzone",
        species_combo_count=2,
        include_tm_species2_for_single=True,
    )
    assigned["stratum_matched"] = None
    assigned = assign_stratum_matches_from_au_table(
        f_table=assigned,
        au_table=au_table,
        tsa_list=[K3Z_TSA_CODE],
        stratum_col="stratum",
        message_fn=lambda *_: None,
    )
    allowed_levels_by_stratum: dict[str, list[str]] = {
        str(stratum_code): sorted({str(value) for value in levels.dropna().values})
        for stratum_code, levels in au_table.groupby("stratum_code")["si_level"]
    }
    assigned, _ = assign_si_levels_from_stratum_quantiles(
        f_table=assigned,
        si_levelquants={"L": [5, 20, 35], "M": [35, 50, 65], "H": [65, 80, 95]},
        allowed_levels_by_stratum=allowed_levels_by_stratum,
        stratum_matched_col="stratum_matched",
        site_index_col="SITE_INDEX",
        si_level_col="si_level",
        message_fn=lambda *_: None,
    )
    assigned["au_base"] = [
        lookup_scsi_au_base(
            scsi_au={
                K3Z_TSA_CODE: {
                    (str(row.stratum_code), str(row.si_level)): _coerce_int(row.au_id)
                    for row in au_table.itertuples(index=False)
                }
            },
            tsa_code=K3Z_TSA_CODE,
            stratum_code=stratum_code,
            si_level=si_level,
        )
        for stratum_code, si_level in zip(
            assigned["stratum_matched"].tolist(),
            assigned["si_level"].tolist(),
            strict=False,
        )
    ]
    assigned = assigned.reset_index()
    merged = assigned.merge(
        vdyp_lyr.loc[:, ["FEATURE_ID", "STEMS_PER_HA_75"]],
        on="FEATURE_ID",
        how="left",
    )
    merged["SITE_INDEX"] = pd.to_numeric(merged["SITE_INDEX"], errors="coerce")
    merged["STEMS_PER_HA_75"] = pd.to_numeric(merged["STEMS_PER_HA_75"], errors="coerce")
    merged = merged.dropna(subset=["au_base"])
    if merged.empty:
        return {}

    summary = (
        merged.groupby("au_base", as_index=False)
        .agg(
            site_index=("SITE_INDEX", "median"),
            unmanaged_stems_per_ha=("STEMS_PER_HA_75", "median"),
        )
        .dropna(subset=["site_index"], how="all")
    )
    return {
        _coerce_int(row.au_base): QmdSupportDefinition(
            site_index=(
                float(row.site_index)
                if pd.notna(row.site_index) and np.isfinite(float(row.site_index))
                else None
            ),
            unmanaged_stems_per_ha=(
                float(row.unmanaged_stems_per_ha)
                if pd.notna(row.unmanaged_stems_per_ha)
                and np.isfinite(float(row.unmanaged_stems_per_ha))
                else None
            ),
            managed_stems_per_ha=None,
            managed_height_points=(),
            managed_tph_points=(),
        )
        for row in summary.itertuples(index=False)
    }


def _merge_qmd_support(
    *sources: dict[int, QmdSupportDefinition],
) -> dict[int, QmdSupportDefinition]:
    merged: dict[int, QmdSupportDefinition] = {}
    for source in sources:
        for au_id, support in source.items():
            current = merged.get(int(au_id))
            if current is None:
                merged[int(au_id)] = support
                continue
            merged[int(au_id)] = QmdSupportDefinition(
                site_index=support.site_index
                if support.site_index is not None
                else current.site_index,
                unmanaged_stems_per_ha=support.unmanaged_stems_per_ha
                if support.unmanaged_stems_per_ha is not None
                else current.unmanaged_stems_per_ha,
                managed_stems_per_ha=support.managed_stems_per_ha
                if support.managed_stems_per_ha is not None
                else current.managed_stems_per_ha,
                managed_height_points=support.managed_height_points
                or current.managed_height_points,
                managed_tph_points=support.managed_tph_points or current.managed_tph_points,
            )
    return merged


@dataclass(frozen=True)
class K3zFmgBundleAuxiliaryProvider:
    """Instance-owned FMG auxiliary provider for the K3Z teaching model."""

    provider_id: str = "k3z"

    def build_bundle_auxiliary(self, request: BundleAuxiliaryRequest) -> BundleAuxiliaryData:
        if request.bundle_dir is None:
            return BundleAuxiliaryData()
        data_dir = request.bundle_dir.parent
        managed_support = load_managed_qmd_support_from_tipsy(
            data_dir=data_dir,
            analysis_units=request.analysis_units,
        )
        unmanaged_support = load_unmanaged_qmd_support_from_checkpoint(
            data_dir=data_dir,
            au_table=request.au_table,
        )
        indicator_curves = load_managed_indicator_curves_from_tipsy(
            data_dir=data_dir,
            analysis_units=request.analysis_units,
        )
        return BundleAuxiliaryData(
            qmd_support_by_au=_merge_qmd_support(unmanaged_support, managed_support),
            managed_indicator_curves_by_au=indicator_curves,
        )


def provider_factory() -> K3zFmgBundleAuxiliaryProvider:
    """Return the K3Z FMG auxiliary provider."""
    return K3zFmgBundleAuxiliaryProvider()


def build_k3z_bundle_model_context(
    *,
    bundle_dir: Path,
    tsa_list: Iterable[str] = (K3Z_TSA_CODE,),
) -> BundleModelContext:
    """Build a K3Z bundle model context with K3Z auxiliary data loaded."""
    return build_bundle_model_context(
        bundle_dir=bundle_dir,
        tsa_list=tsa_list,
        auxiliary_providers=[provider_factory()],
        discover_auxiliary=False,
    )
