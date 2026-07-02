from __future__ import annotations

from importlib import metadata
from pathlib import Path

from k3z_femic.patchworks_variants import provider_factory


def test_patchworks_variant_provider_metadata() -> None:
    provider = provider_factory()

    assert provider.provider_id == "k3z"
    assert provider.registry_base_dir == Path(__file__).resolve().parents[1]

    payload = provider.load_registry_payload()
    assert payload["instances"][0]["instance_id"] == "k3z"
    variant_ids = {item["variant_id"] for item in payload["variants"]}
    assert "k3z.base" in variant_ids
    assert "k3z.intensive_light_standstructure" in variant_ids
    base = next(item for item in payload["variants"] if item["variant_id"] == "k3z.base")
    assert base["instance_root"] == "."
    assert base["analysis_pin"] == "models/k3z_patchworks_model/analysis/base.pin"
    assert base["runtime_config"] == "config/patchworks.runtime.windows.yaml"
    assert payload["scenario_sets"][0]["scenario_set_id"] == "k3z.proving_ground"


def test_package_exposes_patchworks_variant_registry_entry_point() -> None:
    entry_points = metadata.entry_points().select(group="femic.patchworks_variant_registries")
    matches = [entry_point for entry_point in entry_points if entry_point.name == "k3z"]
    assert matches
    assert matches[0].value == "k3z_femic.patchworks_variants:provider_factory"
