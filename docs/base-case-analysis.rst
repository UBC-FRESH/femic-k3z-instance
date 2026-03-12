Base Case Analysis
==================

Analysis Report
---------------

Base-case interpretation for K3Z should include:

- managed/passive area outcomes,
- species-wise managed-yield behavior,
- treatment area trajectories (including seral-linked treatment outcomes),
- key constraint/account trends from generated tracks and runtime reports.

Primary evidence sources:

- ``models/k3z_patchworks_model/tracks/*.csv``
- ``vdyp_io/logs/patchworks_matrixbuilder_manifest-*.json``
- deterministic rebuild reports in ``vdyp_io/logs/k3z_rebuild_report-*.json``

Base Case Output and Interpretation
-----------------------------------

- Use ``accounts.csv`` and Patchworks runtime account views as primary
  interpreted outputs.
- Validate unexpected zeros/nulls by tracing:
  curve definitions -> attributes/products -> accounts -> targets.

Discussion
----------

K3Z is intentionally compact for training and collaboration. It supports
repeatable end-to-end rebuild/testing while preserving operational realism for
core modeling mechanics.

Known Limitations and Uncertainty
---------------------------------

- Legacy provenance quality varies across some historical input layers.
- THLB uncertainty remains intentionally simplified in this baseline.
- Species coding edge cases (for example PL vs PLC semantics) require periodic
  review with regenerated outputs.

Provenance Table
----------------

.. list-table::
   :header-rows: 1

   * - Artifact Family
     - Update Date
     - Source Path/URL
     - Transform Stage
     - QA Status
   * - Base-case forestmodel
     - Per export rebuild
     - ``output/patchworks_k3z_validated/forestmodel.xml``
     - export validation stage
     - Verified by Patchworks startup
   * - Base-case tracks/accounts
     - Per matrix build
     - ``models/k3z_patchworks_model/tracks/``
     - matrix builder stage
     - Verified by invariant tests
   * - Rebuild evidence
     - Per run-id
     - ``vdyp_io/logs/``
     - reproducibility script
     - Verified by report pass/fail flags

What to Edit vs Regenerate
--------------------------

- Edit: narrative interpretation docs and scenario notes.
- Regenerate: output artifacts and evidence manifests.
- Treat all generated XML/CSV analysis artifacts as rebuild products.

How to Validate Reruns
----------------------

1. Rebuild with a unique run-id.
2. Review matrix-build manifest and rebuild report.
3. Confirm baseline checks pass before publishing interpretation updates.

References
----------

- ``reference/TFL26_Information_Package_Sept-2018_v1.1.pdf``
- ``reference/CFA_Analysis_Report.pdf``
- ``reference/FNWL_Analysis_Report.pdf``
