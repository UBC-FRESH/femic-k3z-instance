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
- run-id-specific matrix logs and manifests under ``vdyp_io/logs/``
- Appendix figure catalog in :ref:`k3z-figure-appendix`

Base Case Output and Interpretation
-----------------------------------

- Use ``accounts.csv`` and Patchworks runtime account views as primary
  interpreted outputs.
- Validate unexpected zeros/nulls by tracing:
  curve definitions -> attributes/products -> accounts -> targets.

Species Code Note (PL vs PLC)
-----------------------------

- For K3Z, ``PLC`` is the canonical species code used in interpreted
  species-wise account surfaces.
- ``PL`` rows are intentionally excluded from promoted
  ``tracks/accounts.csv`` during matrix-build sync using
  ``matrix_builder.accounts_exclude_regex`` in
  ``config/patchworks.runtime.windows.yaml``.
- Do not interpret missing/absent ``PL`` account boxes as a model failure for
  this instance; treat ``PLC`` as the operative lodgepole-pine series signal.

Expected-Empty Account Matrix
-----------------------------

.. list-table::
   :header-rows: 1

   * - Account pattern
     - Expected state in K3Z
   * - ``product.Yield.managed.PLC``
     - present + nonzero
   * - ``product.HarvestedVolume.managed.PLC.CC``
     - present + nonzero
   * - ``product.Yield.managed.PL``
     - absent
   * - ``product.HarvestedVolume.managed.PL.CC``
     - absent

Validation checklist:

1. ``femic instance account-surface`` returns no
   ``total OK, species-wise empty`` diagnosis.
2. ``femic instance rebuild --with-patchworks`` passes fatal species policy
   invariants.
3. Latest matrix manifest confirms
   ``accounts_sync.excluded_patterns`` includes ``\.PL(\.|$)``.


Discussion
----------

K3Z is intentionally compact for training and collaboration. It supports
repeatable end-to-end rebuild/testing while preserving operational realism for
core modeling mechanics.

Figure Appendix Linkage
-----------------------

Use :ref:`k3z-figure-appendix` as the canonical catalog for K3Z diagnostic and
teaching figures. Reference specific plot files by name in interpretation notes
and classroom material so readers can connect narrative claims to exact
artifacts.

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

- TFL26 Timber Supply Analysis Information Package (Version 1.1)
- CFA Timber Supply Analysis Data Package and Base Case Results
- FNWL Timber Supply Analysis Data Package and Base Case Results
