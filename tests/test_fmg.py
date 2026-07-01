from __future__ import annotations

from importlib import metadata
from pathlib import Path

import pandas as pd
import pytest
from femic.fmg import CurvePoint

from k3z_femic import build_k3z_bundle_model_context, provider_factory
from k3z_femic.fmg import load_managed_stems_per_ha_by_au_from_btc_input


def _write_bundle_tables(bundle_dir: Path) -> None:
    bundle_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {
                "au_id": 985502001,
                "tsa": "k3z",
                "stratum_code": "CWHvm_FDC+HW",
                "si_level": "M",
                "treated_curve_id": 985522001,
                "untreated_curve_id": 985502001,
                "source_local_au_id": 2001,
                "source_managed_local_au_id": 22001,
                "source_unmanaged_local_au_id": 2001,
            }
        ]
    ).to_csv(bundle_dir / "au_table.csv", index=False)
    pd.DataFrame(
        [
            {"curve_id": 985502001, "curve_type": "untreated"},
            {"curve_id": 985522001, "curve_type": "treated"},
        ]
    ).to_csv(bundle_dir / "curve_table.csv", index=False)
    pd.DataFrame(
        [
            {"curve_id": 985502001, "x": 0, "y": 0.0},
            {"curve_id": 985502001, "x": 10, "y": 30.0},
            {"curve_id": 985522001, "x": 0, "y": 0.0},
            {"curve_id": 985522001, "x": 10, "y": 36.0},
        ]
    ).to_csv(bundle_dir / "curve_points_table.csv", index=False)


def test_provider_factory_metadata() -> None:
    provider = provider_factory()
    assert provider.provider_id == "k3z"
    assert hasattr(provider, "build_bundle_auxiliary")


def test_package_exposes_fmg_auxiliary_entry_point() -> None:
    entry_points = metadata.entry_points().select(group="femic.fmg_bundle_auxiliary")
    matches = [entry_point for entry_point in entry_points if entry_point.name == "k3z"]
    assert matches
    assert matches[0].value == "k3z_femic.fmg:provider_factory"


def test_managed_stems_loader_uses_k3z_btc_input_filename(tmp_path: Path) -> None:
    pd.DataFrame(
        [
            {
                "feature_id": 22001,
                "planted_density1": 630,
                "planted_density2": 180,
                "planted_density3": 90,
                "natural_density1": 0,
            }
        ]
    ).to_csv(tmp_path / "03_input-tsak3z.csv", index=False)

    assert load_managed_stems_per_ha_by_au_from_btc_input(tmp_path)[22001] == (pytest.approx(900.0))


def test_build_k3z_bundle_model_context_loads_managed_support(
    tmp_path: Path,
) -> None:
    bundle_dir = tmp_path / "data" / "model_input_bundle"
    _write_bundle_tables(bundle_dir)
    pd.DataFrame(
        [
            {"AU": 22001, "Age": 0, "Yield": 0.0, "Height": 0.0, "TPH": float("nan")},
            {"AU": 22001, "Age": 10, "Yield": 36.0, "Height": 4.0, "TPH": float("nan")},
        ]
    ).to_csv(tmp_path / "data" / "tipsy_curves_tsak3z.csv", index=False)
    pd.DataFrame(
        [
            {
                "feature_id": 22001,
                "planted_density1": 630,
                "planted_density2": 180,
                "planted_density3": 90,
                "natural_density1": 0,
            }
        ]
    ).to_csv(tmp_path / "data" / "03_input-tsak3z.csv", index=False)

    context = build_k3z_bundle_model_context(bundle_dir=bundle_dir)

    support = context.qmd_support_by_au[985502001]
    assert support.managed_stems_per_ha == pytest.approx(900.0)
    assert support.managed_tph_points == ()


def test_build_k3z_bundle_model_context_loads_indicator_curves(
    tmp_path: Path,
) -> None:
    bundle_dir = tmp_path / "data" / "model_input_bundle"
    _write_bundle_tables(bundle_dir)
    pd.DataFrame(
        [
            {
                "AU": 22001,
                "Age": 0,
                "Yield": 0.0,
                "Height": 0.0,
                "TPH": 0.0,
                "Logs_Grade_J": 0.0,
            },
            {
                "AU": 22001,
                "Age": 10,
                "Yield": 36.0,
                "Height": 4.0,
                "TPH": 900.0,
                "Logs_Grade_J": 12.0,
            },
        ]
    ).to_csv(tmp_path / "data" / "tipsy_curves_tsak3z.csv", index=False)

    context = build_k3z_bundle_model_context(bundle_dir=bundle_dir)

    assert context.managed_indicator_curves_by_au[985502001]["Logs_Grade_J"] == (
        CurvePoint(x=0.0, y=0.0),
        CurvePoint(x=10.0, y=12.0),
    )
