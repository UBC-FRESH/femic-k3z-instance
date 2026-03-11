# femic-k3z-instance

Canonical standalone **K3Z example FEMIC instance** for teaching, onboarding, and reproducible case setup.

## Purpose

This repository is a snapshot-style, runnable example instance for the K3Z case.
It is intended to show how a complete FEMIC instance is structured and versioned.

## Source Provenance

- FEMIC source repo: `https://github.com/UBC-FRESH/femic`
- FEMIC source commit: `a7a397a`

## What Is Included

- `config/` K3Z run + seral + TIPSY config
- `data/bc/cfa/k3z/` K3Z boundary package and source PDFs
- `data/model_input_bundle/` compiled AU/curve tables
- `data/02_input-tsak3z.dat` and `data/04_output-tsak3z.out`
- K3Z tipsy/vdyp intermediate artifacts (`tipsy_*tsak3z*`, `vdyp_*tsak3z*`)
- `plots/` regenerated K3Z diagnostics and overlays
- `models/k3z_patchworks_model/` tracked Patchworks teaching model
- `output/patchworks_k3z_validated/` validated export package

## What Is Excluded

- Non-K3Z provincial base datasets
- Secrets/credentials and machine-local environment files

## Quickstart

1. Install FEMIC from source checkout:

```bash
python -m pip install /path/to/femic
```

2. Validate case configuration and required paths:

```bash
femic prep validate-case --run-config config/run_profile.k3z.yaml --tipsy-config-dir config/tipsy
```

3. Run K3Z compile flow:

```bash
femic run --run-config config/run_profile.k3z.yaml
```

## Standalone Docs

This repository now includes a standalone Sphinx docs site under `docs/`.

Build locally:

```bash
python -m pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html -W
```

## Update Cadence

This repository is maintained as **snapshot releases** tied to FEMIC run/release milestones.
Use tags (for example `v0.1.0`) for teaching baselines.

## Storage Note

Current payload size is suitable for plain git. If future snapshots grow materially,
migrate large binary families to Git LFS or DataLad-based annexing.
