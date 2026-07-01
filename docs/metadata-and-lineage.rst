Metadata and Lineage
====================

Artifact Family Inventory
-------------------------

This inventory maps core K3Z artifact families, authoritative locations, and
how they are produced.

.. list-table::
   :header-rows: 1

   * - Artifact Family
     - Authoritative Location
     - Produced By
     - QA Signal
   * - Runtime configs
     - ``config/*.yaml``
     - manual authoring + reviewed defaults
     - preflight + dry-run sanity
   * - Bundle tables
     - ``data/model_input_bundle/*.csv``
     - ``femic run --run-config ...``
     - schema/column expectations + downstream load
   * - Patchworks model package
     - ``models/k3z_patchworks_model/``
     - export + matrix builder stages
     - Patchworks load success + invariant checks
   * - Validated export mirrors
     - ``output/patchworks_k3z_validated/``
     - validation stage outputs
     - matrix build manifests + startup checks
   * - Rebuild evidence
     - ``runtime/logs/`` for non-VDYP manifests/reports; ``vdyp_io/logs/`` for VDYP-specific logs
     - run-id workflow + matrix build
     - manifest/log timestamps + command status

Build-Lineage Chain
-------------------

1. Case config and source inputs are compiled by FEMIC pipeline stages.
2. Bundle tables feed Patchworks export model generation.
3. Matrix builder generates tracks and account surfaces.
4. Run-id workflow artifacts and manifests are reviewed for acceptance.

Validation Evidence
-------------------

- Matrix builder manifests: ``runtime/logs/patchworks_matrixbuilder_manifest-*.json``
- Patchworks runtime startup/load checks using ``analysis/base.pin``.

Provenance Versioning Policy
----------------------------

- Config and docs are versioned in git with explicit changelog entries.
- Generated artifacts are accepted only with matching rebuild evidence.
- Intentional structural deltas require baseline update review.

References
----------

- TFL26 Timber Supply Analysis Information Package (Version 1.1)
- CFA Timber Supply Analysis Data Package and Base Case Results
- FNWL Timber Supply Analysis Data Package and Base Case Results
