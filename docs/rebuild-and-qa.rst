Rebuild and QA
==============

Deterministic Rebuild Script
----------------------------

Primary source of truth for K3Z rebuild sequence and invariants:

- ``config/rebuild.spec.yaml``

Use instance-local FEMIC rebuild orchestration for reproducible K3Z checks:

.. code-block:: bash

   femic instance rebuild \
     --run-config config/run_profile.k3z.yaml \
     --patchworks-config config/patchworks.runtime.windows.yaml \
     --with-patchworks \
     --run-id k3z_rebuild_check

Preview planned step order without mutation:

.. code-block:: bash

   femic instance rebuild \
     --run-config config/run_profile.k3z.yaml \
     --patchworks-config config/patchworks.runtime.windows.yaml \
     --with-patchworks \
     --dry-run \
     --run-id k3z_rebuild_plan

Manual equivalent command sequence (mirrors rebuild spec):

.. code-block:: bash

   femic prep validate-case --run-config config/run_profile.k3z.yaml --tipsy-config-dir config/tipsy
   femic prep geospatial-preflight
   femic run --run-config config/run_profile.k3z.yaml --run-id k3z_rebuild_check
   femic tsa post-tipsy --run-config config/run_profile.k3z.yaml --tsa k3z --run-id k3z_rebuild_check
   femic patchworks preflight --config config/patchworks.runtime.windows.yaml
   femic patchworks build-blocks --config config/patchworks.runtime.windows.yaml
   femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_rebuild_check

Outputs
-------

- Rebuild report:
  ``vdyp_io/logs/instance_rebuild_report-<run_id>.json``
- Matrix logs:
  ``vdyp_io/logs/patchworks_matrixbuilder_{stdout,stderr,manifest}-<run_id>.log``

Key Invariants
--------------

- Managed area should remain near expected baseline.
- Block joins must remain 1:1 between ``tracks/blocks.csv`` and ``blocks/blocks.shp``.
- Seral accounts must exist in ``tracks/accounts.csv``.
- Required managed species yields must remain non-zero (except explicitly allowed species).
- `CWHvm_CW+YC` and `CWHvm_CW+PLC` should remain excluded from the treated/TIPSY path.
- Matching low-yield fragments should remain fully retained (`RETENTION = 1.0`).
- Remaining treated AUs should reflect the simplified teaching species-mix logic from `config/tipsy/tsak3z.yaml`.

Baseline Workflow
-----------------

Initialize accepted baseline evidence (once per accepted model state):

.. code-block:: bash

   femic run --run-config config/run_profile.k3z.yaml --run-id k3z_baseline
   femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_baseline

Validate against baseline:

.. code-block:: bash

   femic run --run-config config/run_profile.k3z.yaml --run-id k3z_compare
   femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_compare

Optional CT/Fert Variant QA
---------------------------

These checks apply only to the CT/fert variant
(``config/patchworks.variant.ctfert.yaml``, ``analysis/ctfert.pin``).

Variant command pattern:

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.ctfert.windows.yaml --run-id k3z_ctfert

Variant-specific expectations:

- ``tracks_ctfert/treatments.csv`` includes ``CT``, ``F1``, ``F2``, and
  ``F3``.
- ``tracks_ctfert/accounts.csv`` includes the matching
  ``product.Treated.managed.*`` surfaces.
- ``tracks_ctfert/products.csv`` includes the matching treated-product
  surfaces.
- ``SILV_STATE``-specific tracknames/strata materialize for the CT/fert
  sequence.
- The accepted CT/fert fragments surface preserves the baseline 218-fragment
  geometry footprint exactly.
- CT/fert fragment differences are limited to the low-yield AUs ``985502006``
  and ``985502008``, where 9 fragments are retained out of THLB via
  ``RETENTION = 1.0``.
- Refresh the CT/fert ForestModel from canonical bundle/checkpoint inputs, but
  do not replace the checked-in CT/fert fragments surface blindly with raw
  export fragments unless the baseline-footprint invariants still hold.
- Live Patchworks smoke should show that pulling on a minimum ``F3``
  treated-area target induces upstream ``F2`` -> ``F1`` -> ``CT`` -> ``CC``.

Deep reference: :doc:`silviculture-logic`


Optional PCT->CT Variant QA
---------------------------

These checks apply only to the PCT->CT variant (``config/patchworks.variant.pctct.yaml``, ``analysis/pctct.pin``).

Variant command pattern:

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.pctct.windows.yaml --run-id k3z_pctct

Variant-specific expectations:

- ``tracks_pctct/treatments.csv`` includes ``PCT`` and ``CT``.
- ``tracks_pctct/accounts.csv`` includes ``product.Treated.managed.PCT`` and ``product.Treated.managed.CT``.
- ``tracks_pctct/products.csv`` includes the matching treated-product surface.
- the issue-14 `pctct` footprint is centered on medium/high SI ``HW+FDC`` and
  ``FDC+HW`` AUs ``985502000``, ``985503000``, ``985502001``, and
  ``985503001``.
- ``tracks_pctct`` does not materialize ``F1``, ``F2``, or ``F3``.
- ``SILV_STATE``-specific tracknames/strata materialize for:
  - ``cc_pl_pct``
  - ``cc_pl_pct_ct``
- The accepted PCT->CT fragments surface preserves the baseline 218-fragment
  geometry footprint exactly.
- PCT->CT fragment differences are limited to treatment-path consequences in
  the exported ForestModel/tracks surface; the checked-in fragments surface
  itself should not diverge from baseline in
  ``AU`` / ``IFM`` / ``RETENTION`` / ``ORIGIN`` / ``SILV_STATE``.
- Refresh the PCT->CT ForestModel from canonical bundle/checkpoint inputs, but
  do not replace the checked-in PCT->CT fragments surface blindly with raw
  export fragments unless the baseline-footprint invariants still hold.
- ``tracks_pctct`` retains species-wise managed yield / harvested-volume
  accounts in addition to the ``Total`` surfaces.
- Live Patchworks smoke should show that pulling on a minimum ``CT``
  treated-area target induces upstream ``PCT`` and ``CC`` in earlier periods.

Deep reference: :doc:`silviculture-logic`

Baseline Overlay Subvariant QA
------------------------------

These checks apply only to the four baseline-derived overlay subvariants.

For the source contract, subvariant meaning map, and repeatable launch
workflow, use :doc:`overlay-subvariants-workflow`.

Variant command pattern:

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.overlay.basecase_riparian.windows.yaml --run-id k3z_overlay_basecase_riparian

Variant-specific expectations:

- overlay builds still use baseline ``yield/forestmodel.xml``;
- only fragment ``RETENTION`` and resulting managed/unmanaged area balance
  should differ from baseline;
- the student join contract still resolves through ``blocks.shp`` without nulls
  on the selected retention field;
- higher-retention overlays can legitimately drop some managed species
  accounts if that species no longer appears on the managed side.

Deep references:

- :doc:`variants-and-subvariants`
- :doc:`overlay-subvariants-workflow`
