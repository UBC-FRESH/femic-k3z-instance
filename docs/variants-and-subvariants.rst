Variants and Subvariants
========================

Purpose
-------

K3Z now ships as one instance checkout with three coexisting top-level
Patchworks variants and four baseline-derived overlay subvariants.

Use this page as the canonical launch and interpretation map.

Quick Launch Selector
---------------------

.. list-table::
   :header-rows: 1

   * - If the teaching question is...
     - Launch this surface
     - Exact pairing
   * - "What does the accepted K3Z baseline do?"
     - ``base``
     - ``config/patchworks.runtime.windows.yaml`` + ``analysis/base.pin``
   * - "What changes if we add CT plus repeated fertilization?"
     - ``ctfert``
     - ``config/patchworks.runtime.ctfert.windows.yaml`` + ``analysis/ctfert.pin``
   * - "What changes if CT is gated behind an earlier PCT?"
     - ``pctct``
     - ``config/patchworks.runtime.pctct.windows.yaml`` + ``analysis/pctct.pin``
   * - "What changes if retained area follows the student overlay table?"
     - one of the four baseline overlay subvariants
     - the matching ``config/patchworks.runtime.overlay.*.windows.yaml`` + ``analysis/overlay_*.pin``

Variant Matrix
--------------

.. list-table::
   :header-rows: 1

   * - Surface
     - Runtime + PIN
     - Tracks / model artifacts
     - What changes upstream from Matrix Builder
     - Expected consequence surface
     - Intended use
   * - ``base``
     - ``config/patchworks.runtime.windows.yaml`` + ``analysis/base.pin``
     - ``tracks/`` + ``yield/forestmodel.xml`` + ``output/patchworks_k3z_validated/fragments/fragments.shp``
     - Nothing beyond the accepted teaching baseline.
     - Baseline managed/unmanaged accounts, species-wise managed yield, seral, and ``og1`` / ``og2``.
     - Default teaching and comparison surface.
   * - ``ctfert``
     - ``config/patchworks.runtime.ctfert.windows.yaml`` + ``analysis/ctfert.pin``
     - ``tracks_ctfert/`` + ``yield/forestmodel_ctfert.xml`` + ``output/patchworks_k3z_ctfert_validated/fragments/fragments.shp``
     - Adds ``SILV_STATE``, CT, synthetic QMD, and the ``F1 -> F2 -> F3`` treatment chain.
     - CT/F1/F2/F3 treated products plus variant-specific managed account surfaces.
     - Intensive-silviculture teaching scaffold with fertilization.
   * - ``pctct``
     - ``config/patchworks.runtime.pctct.windows.yaml`` + ``analysis/pctct.pin``
     - ``tracks_pctct/`` + ``yield/forestmodel_pctct.xml`` + ``output/patchworks_k3z_pctct_validated/fragments/fragments.shp``
     - Adds ``SILV_STATE`` plus a planted-only PCT gate ahead of CT, but no fertilization chain.
     - ``PCT`` and ``CT`` treated products on the ``PCT -> CT`` path, plus species-wise managed yield / harvest-volume surfaces.
     - Intensive-silviculture teaching scaffold without fertilization.
   * - ``basecase_riparian``
     - ``config/patchworks.runtime.overlay.basecase_riparian.windows.yaml`` + ``analysis/overlay_basecase_riparian.pin``
     - ``tracks_overlay_basecase_riparian/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_basecase_riparian_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``Basecase_Riparian`` field.
     - Only the managed/unmanaged split should change relative to baseline.
     - Baseline subvariant for riparian-style retained-area comparison.
   * - ``basecase_sum``
     - ``config/patchworks.runtime.overlay.basecase_sum.windows.yaml`` + ``analysis/overlay_basecase_sum.pin``
     - ``tracks_overlay_basecase_sum/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_basecase_sum_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``BaseCase_Sum`` field.
     - Only the managed/unmanaged split should change relative to baseline.
     - Baseline subvariant for the student's summed base-case retention.
   * - ``scenario1_sum``
     - ``config/patchworks.runtime.overlay.scenario1_sum.windows.yaml`` + ``analysis/overlay_scenario1_sum.pin``
     - ``tracks_overlay_scenario1_sum/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_scenario1_sum_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``Scenario1_Sum`` field.
     - Only the managed/unmanaged split should change relative to baseline.
     - Baseline subvariant for the student's first scenario retention.
   * - ``scenario2_sum``
     - ``config/patchworks.runtime.overlay.scenario2_sum.windows.yaml`` + ``analysis/overlay_scenario2_sum.pin``
     - ``tracks_overlay_scenario2_sum/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_scenario2_sum_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``Scenario2_Sum`` field.
     - Only the managed/unmanaged split should change relative to baseline.
     - Baseline subvariant for the student's second scenario retention.

How to Choose a Surface
-----------------------

1. Start with ``base`` unless you explicitly need a treatment scaffold or an
   overlay sensitivity surface.
2. Choose ``ctfert`` when the class exercise needs ``CT -> F1 -> F2 -> F3``.
3. Choose ``pctct`` when the class exercise needs ``PCT -> CT`` without
   fertilization.
4. Choose one of the four overlay subvariants only when the exercise is about
   alternative retained-area policy on top of the accepted baseline.

Overlay Provenance and Join Contract
------------------------------------

The four overlay subvariants are **subvariants of baseline**, not separate
top-level instance variants.

Current teaching handoff:

- student source is an abandoned GIS fork, represented in the current workflow
  by an attribute-table export named ``Fragments_Retention_HSmith.xls``;
- the workbook key field is ``FEATURE_ID1`` even though the canonical K3Z join
  uses ``FEATURE_ID``;
- the four retention columns are:
  - ``Basecase_Riparian``
  - ``BaseCase_Sum``
  - ``Scenario1_Sum``
  - ``Scenario2_Sum``

Bridge used in the current workflow:

1. Student workbook row keyed by ``FEATURE_ID1``.
2. Join to ``models/k3z_patchworks_model/blocks/blocks.shp`` on
   ``FEATURE_ID``.
3. Use block identity to reach the canonical fragments surface.
4. Write a normalized overlay table keyed to the canonical fragments.
5. Rebuild one fragments surface per selected retention column.

Operationally, the overlay subvariants should differ from baseline only by
fragment-level ``RETENTION`` values and the resulting managed-vs-unmanaged area
split.

Overlay Account-Surface Note
----------------------------

High-retention overlays can legitimately drop some species-wise managed
accounts.

That is not automatically a compile failure. If retained area removes a species
from the managed side of a subvariant, the corresponding managed species
account can disappear from that subvariant's compiled tracks and live Patchworks
account view.

Audit Checklist
---------------

- Keep the runtime config and PIN paired exactly as listed above.
- Compare overlay subvariants against ``base`` first, not against each other.
- Confirm the overlay source table still resolves 1:1 against the canonical
  fragments surface before interpreting results.
- Treat unexpected treatment-path changes on overlay subvariants as a bug,
  because overlays are intended to modify retained area only.
