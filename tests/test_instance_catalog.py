from __future__ import annotations

from importlib import metadata

from k3z_femic.instance_catalog import provider_factory


def test_instance_catalog_provider_metadata() -> None:
    provider = provider_factory()

    assert provider.provider_id == "k3z"
    payload = provider.load_catalog_payload()
    assert payload["support_repos"][0]["repo_id"] == "femic-public-data"
    assert payload["instances"][0]["builtin_id"] == "k3z"
    assert payload["instances"][0]["target_dirname"] == "femic-k3z-instance"


def test_package_exposes_instance_catalog_entry_point() -> None:
    entry_points = metadata.entry_points().select(group="femic.instance_catalogs")
    matches = [entry_point for entry_point in entry_points if entry_point.name == "k3z"]
    assert matches
    assert matches[0].value == "k3z_femic.instance_catalog:provider_factory"
