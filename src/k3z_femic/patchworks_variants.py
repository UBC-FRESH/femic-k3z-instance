"""K3Z-owned Patchworks variant registry provider."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class K3zPatchworksVariantRegistryProvider:
    """Expose K3Z Patchworks variants to FEMIC through entry-point discovery."""

    provider_id: str = "k3z"
    registry_base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])

    def load_registry_payload(self) -> dict[str, Any]:
        resource = resources.files("k3z_femic.resources").joinpath("patchworks_variants.yaml")
        payload = yaml.safe_load(resource.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("K3Z Patchworks variant registry payload must be a mapping.")
        return payload


def provider_factory() -> K3zPatchworksVariantRegistryProvider:
    """Return the K3Z Patchworks variant registry provider."""

    return K3zPatchworksVariantRegistryProvider()
