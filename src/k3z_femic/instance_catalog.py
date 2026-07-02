"""K3Z-owned FEMIC instance catalog provider."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from typing import Any

import yaml


@dataclass(frozen=True)
class K3zInstanceCatalogProvider:
    """Expose the K3Z installable instance catalog entry to FEMIC."""

    provider_id: str = "k3z"

    def load_catalog_payload(self) -> dict[str, Any]:
        resource = resources.files("k3z_femic.resources").joinpath("instance_catalog.yaml")
        payload = yaml.safe_load(resource.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("K3Z instance catalog payload must be a mapping.")
        return payload


def provider_factory() -> K3zInstanceCatalogProvider:
    """Return the K3Z instance catalog provider."""

    return K3zInstanceCatalogProvider()
