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

These checks apply only to the shipped CT/fert SI-profile subvariants
(``ctfert_l15h5`` and ``ctfert_l20h0``).

Variant command pattern:

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.ctfert_l15h5.windows.yaml --run-id k3z_ctfert_l15h5
   femic patchworks matrix-build --config config/patchworks.runtime.ctfert_l20h0.windows.yaml --run-id k3z_ctfert_l20h0

Variant-specific expectations:

- ``SILV_STATE``-specific tracknames/strata materialize for the CT/fert
  sequence.
- Live Patchworks smoke should show that pulling on a minimum ``F3``
  treated-area target induces upstream ``F2`` -> ``F1`` -> ``CT`` -> ``CC``.
- For ``ctfert_l15h5`` and ``ctfert_l20h0``, confirm the accepted validated
  fragments surfaces preserve the curated 218-fragment geometry footprint from
  ``tmp/CTFert Fragments/fragments_updated3_Usedinbasecase.shp`` exactly, and
  therefore replace the old uniform ``RETENTION = 0.05`` placeholder with the
  student-provided per-fragment values.
- For ``ctfert_l15h5``, confirm the six eligible ``L/M/H`` AUs all materialize
  the ``CT -> F1 -> F2 -> F3`` path.
- For ``ctfert_l20h0``, confirm the two ``H``-class AUs still materialize CT
  but do not compile any ``F1`` / ``F2`` / ``F3`` path.

Deep reference: :doc:`silviculture-logic`


Optional PCT-Only Subvariant QA
-------------------------------

These checks apply only to the three PCT-only subvariants
(``pct_light``, ``pct_moderate``, ``pct_heavy``).

Variant command pattern:

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.pct_light.windows.yaml --run-id k3z_pct_light
   femic patchworks matrix-build --config config/patchworks.runtime.pct_moderate.windows.yaml --run-id k3z_pct_moderate
   femic patchworks matrix-build --config config/patchworks.runtime.pct_heavy.windows.yaml --run-id k3z_pct_heavy

Variant-specific expectations:

- each ``tracks_pct_*`` ``treatments.csv`` includes ``PCT`` and does not
  include ``CT``.
- each ``tracks_pct_*`` ``accounts.csv`` includes
  ``product.Treated.managed.PCT`` and excludes ``product.Treated.managed.CT``.
- each ``tracks_pct_*`` ``products.csv`` includes the matching treated-product surface.
- the issue-14 ``pct_*`` footprint is centered on medium/high SI ``HW+FDC`` and
  ``FDC+HW`` AUs ``985502000``, ``985503000``, ``985502001``, and
  ``985503001``.
- each ``tracks_pct_*`` surface does not materialize ``F1``, ``F2``, or ``F3``.
- each ``tracks_pct_*`` surface materializes ``cc_pl_pct`` and not
  ``cc_pl_pct_ct`` as the treatment-history state.
- the accepted PCT-only fragments surfaces preserve the baseline 218-fragment
  geometry footprint exactly.
- PCT-only fragment differences are limited to treatment-path consequences in
  the exported ForestModel/tracks surface; the checked-in fragments surface
  itself should not diverge from baseline in
  ``AU`` / ``IFM`` / ``RETENTION`` / ``ORIGIN`` / ``SILV_STATE``.
- Refresh the PCT-only ForestModel from canonical bundle/checkpoint inputs, but
  do not replace the checked-in PCT-only fragments surface blindly with raw
  export fragments unless the baseline-footprint invariants still hold.
- each ``tracks_pct_*`` surface retains species-wise managed yield / harvested-volume
  accounts in addition to the ``Total`` surfaces.
- Live Patchworks smoke should show that pulling on a minimum ``PCT``
  treated-area target induces upstream ``CC`` in earlier periods.

Deep reference: :doc:`silviculture-logic`

Optional Full-Intensive Subvariant QA
-------------------------------------

These checks apply only to the three full-intensive subvariants
(``intensive_light``, ``intensive_moderate``, ``intensive_heavy``).

Variant command pattern:

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.intensive_light.windows.yaml --run-id k3z_intensive_light
   femic patchworks matrix-build --config config/patchworks.runtime.intensive_moderate.windows.yaml --run-id k3z_intensive_moderate
   femic patchworks matrix-build --config config/patchworks.runtime.intensive_heavy.windows.yaml --run-id k3z_intensive_heavy

Variant-specific expectations:

- each ``tracks_intensive_*`` ``treatments.csv`` includes ``PCT``, ``CT``,
  ``F1``, ``F2``, and ``F3``.
- each ``tracks_intensive_*`` surface materializes ``cc_pl_pct`` and
  ``cc_pl_pct_ct`` in the treatment-history state chain.
- the combined treatment family is centered on the full 8-AU union of the
  current ``pct_*`` and ``ctfert_l15h5`` families:
  ``985501001``, ``985502001``, ``985503001``, ``985501002``, ``985502002``,
  ``985503002``, ``985502000``, and ``985503000``.
- each ``tracks_intensive_*`` surface exposes AU-wise harvested-QMD numerator /
  denominator / ratio-account support for ``PCT``, ``CT``, and downstream
  ``CC``.
- each ``tracks_intensive_*`` surface exposes AU-wise standing stems-per-ha
  feature accounts on both the managed and unmanaged side.
- the accepted validated fragments surfaces preserve the curated 218-fragment
  geometry footprint from
  ``tmp/CTFert Fragments/fragments_updated3_Usedinbasecase.shp`` exactly.
- live Patchworks smoke should show that pulling on a minimum ``F3``
  treated-area target induces ``F2`` -> ``F1`` -> ``CT`` -> ``PCT`` -> ``CC``.

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
