Land Base and Netdown
=====================

Introduction
------------

This page documents K3Z land-base compilation assumptions in the same style as
BC timber supply data packages.

Land Base Definition
--------------------

K3Z land base for Patchworks runtime is represented by:

- source fragments in ``output/patchworks_k3z_validated/fragments/``
- model blocks in ``models/k3z_patchworks_model/blocks/``
- active tracks in ``models/k3z_patchworks_model/tracks/``

Data Sources and Inventory
--------------------------

- Base inventory inputs from instance ``data/`` and staged bundle outputs in
  ``data/model_input_bundle/``.
- Curated model package under ``models/k3z_patchworks_model/`` is authoritative
  for Patchworks loading.

Exclusions from Contributing Forest
-----------------------------------

Current K3Z baseline treats all modeled fragments as contributing for this
training case. Exclusions are introduced only when encoded explicitly in
upstream bundle transforms.

Reductions from THLB (Netdown Logic)
------------------------------------

Current training baseline forces THLB-equivalent treatment eligibility to full
coverage for modeled fragments, with deferred refinement of uncertain legacy
raster-derived THLB layers.

Landbase Characteristics
------------------------

- Block joins are expected 1:1 between ``tracks/blocks.csv`` and
  ``blocks/blocks.shp``.
- Managed area baseline is validated through reproducibility checks in
  ``rebuild-and-qa.rst``.

Provenance Table
----------------

.. list-table::
   :header-rows: 1

   * - Artifact Family
     - Update Date
     - Source Path/URL
     - Transform Stage
     - QA Status
   * - Fragments inputs
     - Per rebuild run
     - ``output/patchworks_k3z_validated/fragments/``
     - Patchworks export validation
     - Verified by matrix-build manifest
   * - Blocks and topology
     - Per rebuild run
     - ``models/k3z_patchworks_model/blocks/``
     - ``femic patchworks build-blocks``
     - Verified by join invariants
   * - Tracks block mapping
     - Per matrix build
     - ``models/k3z_patchworks_model/tracks/blocks.csv``
     - ``femic patchworks matrix-build``
     - Verified by reproducibility checks

What to Edit vs Regenerate
--------------------------

- Edit: ``config/*.yaml`` assumptions and runtime settings.
- Regenerate: ``blocks/*`` and ``tracks/*.csv`` outputs.
- Do not hand-edit generated block/track tables unless you also update
  reproducibility baselines.

How to Validate Reruns
----------------------

1. Run ``femic patchworks build-blocks`` then ``femic patchworks matrix-build``.
2. Run the deterministic rebuild check described in ``rebuild-and-qa.rst``.
3. Confirm managed-area and block-join invariants remain within baseline.
