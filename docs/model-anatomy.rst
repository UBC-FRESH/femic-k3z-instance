Model Anatomy
=============

Directory Map
-------------

- ``analysis/``: Patchworks PIN files and runtime entrypoints.
- ``blocks/``: block shapefile and topology CSV used by Patchworks joins.
- ``config/``: run profile, seral config, TIPSY rules, Patchworks runtime config.
- ``data/``: local case inputs, cached intermediates, model-input bundle tables.
- ``models/k3z_patchworks_model/``: curated Patchworks model package.
- ``output/``: validated export products from FEMIC stages.
- ``plots/``: QA and interpretation figures for strata/curves/overlays.
- ``vdyp_io/logs/``: reproducibility artifacts (manifests, matrix logs, reports).

Generated vs Editable
---------------------

Safe to edit directly:

- ``config/run_profile.k3z.yaml``
- ``config/seral.k3z.yaml``
- ``config/tipsy/tsak3z.yaml``

Regenerate instead of hand-edit:

- ``data/model_input_bundle/*.csv``
- ``models/k3z_patchworks_model/tracks/*.csv``
- ``models/k3z_patchworks_model/yield/forestmodel.xml``

Use caution:

- ``models/k3z_patchworks_model/analysis/base.pin`` (runtime wiring)
- ``models/k3z_patchworks_model/blocks/*`` (must stay join-consistent with tracks)
