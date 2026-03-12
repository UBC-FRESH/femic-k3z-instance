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
- Treated curves currently use scaled-from-VDYP behavior for K3Z until a new
  approved treated-curve method replaces it.

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
     - ``models/k3z_patchworks_model/yield/forestmodel.xml``
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

- ``reference/TFL26_Information_Package_Sept-2018_v1.1.pdf``
- ``reference/CFA_Analysis_Report.pdf``
- ``reference/FNWL_Analysis_Report.pdf``
