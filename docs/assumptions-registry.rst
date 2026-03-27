Assumptions Registry
====================

Non-Timber Assumptions
----------------------

- Seral-stage tracking and feature-state reporting are enabled via
  K3Z-specific model wiring.
- Non-timber constraints are represented as account/target structures from
  generated tracks and PIN logic.

Harvesting Assumptions
----------------------

- Baseline treatment focus is clearcut (CC) as configured in current K3Z model
  setup.
- Minimum harvest age follows current K3Z policy configuration
  (for example CC min age relative to CMAI).

Growth and Yield Assumptions
----------------------------

- Untreated/treated curve-source terminology is used consistently.
- K3Z baseline managed curves now use real BatchTIPSY output driven by
  VDYP-derived SI, not the older scaled-from-VDYP fallback.
- ``CWHvm_CW+YC`` and ``CWHvm_CW+PLC`` are intentionally excluded from the
  BatchTIPSY treated path and retained out of THLB with ``RETENTION = 1.0``.
- Issue-14 ``pct_light``, ``pct_moderate``, and ``pct_heavy`` target
  AUs ``985502000``, ``985503000``, ``985502001``, and ``985503001`` all use
  ``900 CW + 3100 HW`` as the planted regen mix.
- The three PCT-only subvariants differ only by the age-10 ``HW`` removal
  intensity:
  - ``pct_light`` removes ``1000`` HW stems/ha.
  - ``pct_moderate`` removes ``2000`` HW stems/ha.
  - ``pct_heavy`` removes ``3000`` HW stems/ha.
- Remaining treated AUs outside that `pct_*` cohort use the simplified
  teaching planting logic:
  FD-pair AUs use ``900 FD + 3100 HW``; CW-pair AUs use ``900 CW + 3100 HW``;
  all other remaining treated AUs use ``600 CW + 300 FD + 3100 HW``.
- Current unmanaged smoothing baseline is the accepted relaxed toe/tail policy
  plus extra DR+HW-specific overrides recorded in the Phase 23 notes.

Natural Disturbance Assumptions
-------------------------------

- Disturbance behavior outside explicit modeled treatments is limited in this
  training baseline and should be treated as scenario-dependent.

Modeling Assumptions
--------------------

- Patchworks matrix-build outputs are authoritative for tracks.
- ``protoaccounts.csv -> accounts.csv`` synchronization is part of the rebuild
  pipeline with backup behavior.
- Relative paths are PIN-relative under ``models/k3z_patchworks_model/analysis``.

Provenance Table
----------------

.. list-table::
   :header-rows: 1

   * - Artifact Family
     - Update Date
     - Source Path/URL
     - Transform Stage
     - QA Status
   * - Yield model definition
     - Per export rebuild
     - ``output/patchworks_k3z_validated/forestmodel.xml``
     - ``femic export patchworks``
     - Verified by Patchworks load + matrix build
   * - Tracks assumptions surface
     - Per matrix build
     - ``models/k3z_patchworks_model/tracks/*.csv``
     - ``femic patchworks matrix-build``
     - Verified by invariant checks
   * - Runtime assumptions
     - When runtime config changes
     - ``config/patchworks.runtime.windows.yaml``
     - preflight + matrix-build execution
     - Verified by preflight success

What to Edit vs Regenerate
--------------------------

- Edit: assumption YAMLs and docs.
- Regenerate: forestmodel and tracks from source pipeline commands.
- Avoid direct edits to generated CSV/XML unless the change is intentionally
  outside FEMIC generation logic.

How to Validate Reruns
----------------------

1. Execute deterministic rebuild script and capture run-id report.
2. Confirm invariant checks pass (managed area, species, seral, block joins).
3. Compare against baseline snapshot and review deltas before accepting.

References
----------

- TFL26 Timber Supply Analysis Information Package (Version 1.1)
- CFA Timber Supply Analysis Data Package and Base Case Results
- FNWL Timber Supply Analysis Data Package and Base Case Results
