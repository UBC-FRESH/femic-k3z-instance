Model Anatomy
=============

Directory Map
-------------

- ``analysis/``: Patchworks PIN files and runtime entrypoints.
- ``blocks/``: block shapefile and topology CSV used by Patchworks joins.
- ``config/``: run profile, seral config, silviculture config, TIPSY rules,
  Patchworks runtime config.
- ``data/``: local case inputs, cached intermediates, model-input bundle tables.
- ``models/k3z_patchworks_model/``: curated Patchworks model package.
- ``output/``: validated export products from FEMIC stages.
- ``plots/``: QA and interpretation figures for strata/curves/overlays.
- ``vdyp_io/logs/``: reproducibility artifacts (manifests, matrix logs,
  reports).

Generated vs Editable
---------------------

Safe to edit directly:

- ``config/run_profile.k3z.yaml``
- ``config/seral.k3z.yaml``
- ``config/tipsy/tsak3z.yaml``
- ``config/silviculture.k3z.ctfert.yaml`` for the optional CT/fert variant
- ``config/silviculture.k3z.pctct.yaml`` for the optional PCT->CT variant
- fragment-level ``RETENTION`` values when/if you intentionally edit retained-area policy in the validated fragments dataset

Regenerate instead of hand-edit:

- ``data/model_input_bundle/*.csv``
- ``models/k3z_patchworks_model/tracks/*.csv``
- ``models/k3z_patchworks_model/yield/forestmodel.xml``
- ``output/patchworks_k3z_validated/fragments/*``

Use caution:

- ``models/k3z_patchworks_model/analysis/base.pin`` (runtime wiring)
- ``models/k3z_patchworks_model/blocks/*`` (must stay join-consistent with tracks)

Core Feature and Product Surfaces
---------------------------------

Seral account surfaces:

- Global compatibility surface: ``feature.Seral.<stage>``
- AU-specific inventory-state surface: ``feature.Seral.<au_id>.<stage>``
- Treatment consequence surface: ``product.Seral.area.<stage>.<au_id>.CC``

Old-growth surfaces:

- ``feature.Area.og1.<au_id>``
- ``feature.Area.og2.<au_id>``
- ``feature.Area.og1.total``
- ``feature.Area.og2.total``

Current old-growth curve semantics:

- ``og1``: unmanaged-curve-driven ramp from CMAI age (0.0) to unmanaged
  peak-yield age (1.0)
- ``og2``: policy-step curve with ``249 -> 0.0`` and ``250 -> 1.0``

Deep reference: :doc:`old-growth-attributes`

These are inventory-state feature surfaces, not treatment-consequence products.
They should appear automatically in compiled Patchworks accounts after Matrix
Builder regenerates ``protoaccounts.csv`` / ``accounts.csv``.

Retention Surface
-----------------

K3Z carries a fragment-level ``RETENTION`` field in the validated Patchworks
fragments dataset.

- ``0.0`` means no retained area is withdrawn from the managed landbase.
- ``1.0`` means the full fragment area is retained.
- intermediate values mean partial retained area.

Current K3Z baseline:

- the teaching baseline on ``main`` uses ``RETENTION = 0.05`` for all fragments
- retained area is therefore withdrawn from the managed landbase and compiled
  into unmanaged area/tracks/accounts in Patchworks

Do not hand-edit retention in multiple places. If you change retention policy,
update the validated fragments dataset and rerun Matrix Builder so the retained
share flows into Patchworks unmanaged area consistently.

Optional CT/Fert Variant Surface
--------------------------------

The optional CT/fert variant adds a second layer
of model anatomy that is intentionally not part of the baseline K3Z teaching
instance on ``main``.

Additional state/config artifacts for that variant:

- fragment/XML state field: ``SILV_STATE``
- silviculture config: ``config/silviculture.k3z.ctfert.yaml``
- provisional QMD outputs:
  - ``feature.QMD.managed.<au_id>``
  - ``feature.QMD.unmanaged.<au_id>``
- treatment-path states:
  - ``baseline``
  - ``cc_pl``
  - ``cc_pl_ct``
  - ``cc_pl_ct_f1``
  - ``cc_pl_ct_f1_f2``
  - ``cc_pl_ct_f1_f2_f3``

Optional treatment surfaces for that variant:

- ``CT`` commercial thinning on two initial eligible AUs
- ``F1`` / ``F2`` / ``F3`` fertilization chain after CT
- matching compiled treatment products/accounts such as:
  - ``product.Treated.managed.CT``
  - ``product.Treated.managed.F1``
  - ``product.Treated.managed.F2``
  - ``product.Treated.managed.F3``

In this variant, ``ORIGIN`` still means natural vs planted. Treatment history is
carried by ``SILV_STATE`` instead of overloading ``ORIGIN``.


Optional PCT->CT Variant Surface
--------------------------------

The optional ``pctct`` variant adds a third coexisting upstream-distinct
surface that keeps the baseline and CT/fert variants intact while inserting a
pre-commercial-thinning gate ahead of CT.

Additional state/config artifacts for that variant:

- fragment/XML state field: ``SILV_STATE``
- silviculture config: ``config/silviculture.k3z.pctct.yaml``
- treatment-path states:
  - ``baseline``
  - ``cc_pl``
  - ``cc_pl_pct``
  - ``cc_pl_pct_ct``

Optional treatment surfaces for that variant:

- ``PCT`` at age 10 by default on the planted path
- post-PCT managed species proportions with the ``HW`` species component
  removed
- ``CT`` available only after ``PCT``
- matching compiled treatment products/accounts such as:
  - ``product.Treated.managed.PCT``
  - ``product.Treated.managed.CT``

This variant is intended as a teaching scaffold for ``PCT`` -> ``CT`` path
logic without the added complexity of fertilization.

Deep references
---------------

- full launch matrix: :doc:`variants-and-subvariants`
- treatment/state-machine details: :doc:`silviculture-logic`
- old-growth attribute logic: :doc:`old-growth-attributes`
