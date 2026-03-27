Variants and Subvariants
========================

Purpose
-------

K3Z now ships as one instance checkout with one baseline surface, a small
family of coexisting CT/fert surfaces, a full-intensive teaching family,
three PCT-only teaching subvariants, and four baseline-derived overlay
subvariants.

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
   * - "What changes if CT/fert expands to L/M/H SI classes with profile ``L15/M10/H5``?"
     - ``ctfert_l15h5``
     - ``config/patchworks.runtime.ctfert_l15h5.windows.yaml`` + ``analysis/ctfert_l15h5.pin``
   * - "What changes if CT/fert expands to L/M/H SI classes with profile ``L20/M10/H0``?"
     - ``ctfert_l20h0``
     - ``config/patchworks.runtime.ctfert_l20h0.windows.yaml`` + ``analysis/ctfert_l20h0.pin``
   * - "What changes if we combine ``PCT -> CT -> F1 -> F2 -> F3`` with light PCT?"
     - ``intensive_light``
     - ``config/patchworks.runtime.intensive_light.windows.yaml`` + ``analysis/intensive_light.pin``
   * - "What changes if we combine ``PCT -> CT -> F1 -> F2 -> F3`` with moderate PCT?"
     - ``intensive_moderate``
     - ``config/patchworks.runtime.intensive_moderate.windows.yaml`` + ``analysis/intensive_moderate.pin``
   * - "What changes if we combine ``PCT -> CT -> F1 -> F2 -> F3`` with heavy PCT?"
     - ``intensive_heavy``
     - ``config/patchworks.runtime.intensive_heavy.windows.yaml`` + ``analysis/intensive_heavy.pin``
   * - "What changes if we apply light PCT at age 10?"
     - ``pct_light``
     - ``config/patchworks.runtime.pct_light.windows.yaml`` + ``analysis/pct_light.pin``
   * - "What changes if we apply moderate PCT at age 10?"
     - ``pct_moderate``
     - ``config/patchworks.runtime.pct_moderate.windows.yaml`` + ``analysis/pct_moderate.pin``
   * - "What changes if we apply heavy PCT at age 10?"
     - ``pct_heavy``
     - ``config/patchworks.runtime.pct_heavy.windows.yaml`` + ``analysis/pct_heavy.pin``
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
     - Nothing beyond the accepted teaching baseline, plus AU-wise standing QMD, standing stems-per-ha, and harvested-QMD support surfaces.
     - Baseline managed/unmanaged accounts, species-wise managed yield, seral, ``og1`` / ``og2``, AU-wise standing stems-per-ha, and AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for ``CC``.
     - Default teaching and comparison surface.
   * - ``ctfert_l15h5``
     - ``config/patchworks.runtime.ctfert_l15h5.windows.yaml`` + ``analysis/ctfert_l15h5.pin``
     - ``tracks_ctfert_l15h5/`` + ``yield/forestmodel_ctfert_l15h5.xml`` + ``output/patchworks_k3z_ctfert_l15h5_validated/fragments/fragments.shp``
     - Keeps the CT/QMD/F1/F2/F3 chain, expands eligibility to six ``L/M/H`` SI AUs, applies fert boosts ``L=15%``, ``M=10%``, ``H=5%``, ramps the CT final-felling gap to ``0.0`` by ``cmai_argmax``, rebuilds QMD from accepted yield/height/TPH support inputs instead of the old placeholder age heuristic, and uses the student-provided curated ``RETENTION`` overlay instead of the old uniform ``0.05`` placeholder.
     - CT/F1/F2/F3 treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD product numerators/treated-area companions, plus SI-profile-specific managed account surfaces.
     - CT/fert teaching scaffold with explicit low/medium/high SI fert response differences.
   * - ``ctfert_l20h0``
     - ``config/patchworks.runtime.ctfert_l20h0.windows.yaml`` + ``analysis/ctfert_l20h0.pin``
     - ``tracks_ctfert_l20h0/`` + ``yield/forestmodel_ctfert_l20h0.xml`` + ``output/patchworks_k3z_ctfert_l20h0_validated/fragments/fragments.shp``
     - Keeps CT on six ``L/M/H`` SI AUs, applies fert boosts ``L=20%`` and ``M=10%``, disables fert on ``H``-class AUs, ramps the CT final-felling gap to ``0.0`` by ``cmai_argmax``, rebuilds QMD from accepted yield/height/TPH support inputs instead of the old placeholder age heuristic, and uses the student-provided curated ``RETENTION`` overlay instead of the old uniform ``0.05`` placeholder.
     - CT/F1/F2/F3 treated products on eligible AUs, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD product numerators/treated-area companions, plus CT-only surfaces on the ``H`` cohort.
     - CT/fert teaching scaffold for comparing a stronger low-SI response with no fertilization on high-SI AUs.
   * - ``intensive_light``
     - ``config/patchworks.runtime.intensive_light.windows.yaml`` + ``analysis/intensive_light.pin``
     - ``tracks_intensive_light/`` + ``yield/forestmodel_intensive_light.xml`` + ``output/patchworks_k3z_intensive_light_validated/fragments/fragments.shp``
     - Adds light PCT ahead of the ``ctfert_l15h5`` CT/fert chain, expands the combined treatment family to the full 8-AU union of the current ``pct_*`` and ``ctfert_l15h5`` families, and keeps the curated CT/fert retention overlay.
     - ``PCT`` plus ``CT/F1/F2/F3`` treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for ``PCT``, ``CT``, and downstream ``CC``.
     - Full intensive-silviculture teaching scaffold with light PCT.
   * - ``intensive_moderate``
     - ``config/patchworks.runtime.intensive_moderate.windows.yaml`` + ``analysis/intensive_moderate.pin``
     - ``tracks_intensive_moderate/`` + ``yield/forestmodel_intensive_moderate.xml`` + ``output/patchworks_k3z_intensive_moderate_validated/fragments/fragments.shp``
     - Adds moderate PCT ahead of the ``ctfert_l15h5`` CT/fert chain, expands the combined treatment family to the full 8-AU union of the current ``pct_*`` and ``ctfert_l15h5`` families, and keeps the curated CT/fert retention overlay.
     - ``PCT`` plus ``CT/F1/F2/F3`` treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for ``PCT``, ``CT``, and downstream ``CC``.
     - Full intensive-silviculture teaching scaffold with moderate PCT.
   * - ``intensive_heavy``
     - ``config/patchworks.runtime.intensive_heavy.windows.yaml`` + ``analysis/intensive_heavy.pin``
     - ``tracks_intensive_heavy/`` + ``yield/forestmodel_intensive_heavy.xml`` + ``output/patchworks_k3z_intensive_heavy_validated/fragments/fragments.shp``
     - Adds heavy PCT ahead of the ``ctfert_l15h5`` CT/fert chain, expands the combined treatment family to the full 8-AU union of the current ``pct_*`` and ``ctfert_l15h5`` families, and keeps the curated CT/fert retention overlay.
     - ``PCT`` plus ``CT/F1/F2/F3`` treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for ``PCT``, ``CT``, and downstream ``CC``.
     - Full intensive-silviculture teaching scaffold with heavy PCT.
   * - ``pct_light``
     - ``config/patchworks.runtime.pct_light.windows.yaml`` + ``analysis/pct_light.pin``
     - ``tracks_pct_light/`` + ``yield/forestmodel_pct_light.xml`` + ``output/patchworks_k3z_pct_light_validated/fragments/fragments.shp``
     - Adds ``SILV_STATE`` plus a planted-only light PCT gate, but no CT or fertilization chain.
     - ``PCT`` treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for both ``PCT`` and ``CC``, plus species-wise managed yield / harvest-volume surfaces.
     - Light-intensity stand-tending teaching scaffold.
   * - ``pct_moderate``
     - ``config/patchworks.runtime.pct_moderate.windows.yaml`` + ``analysis/pct_moderate.pin``
     - ``tracks_pct_moderate/`` + ``yield/forestmodel_pct_moderate.xml`` + ``output/patchworks_k3z_pct_moderate_validated/fragments/fragments.shp``
     - Adds ``SILV_STATE`` plus a planted-only moderate PCT gate, but no CT or fertilization chain.
     - ``PCT`` treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for both ``PCT`` and ``CC``, plus species-wise managed yield / harvest-volume surfaces.
     - Moderate-intensity stand-tending teaching scaffold.
   * - ``pct_heavy``
     - ``config/patchworks.runtime.pct_heavy.windows.yaml`` + ``analysis/pct_heavy.pin``
     - ``tracks_pct_heavy/`` + ``yield/forestmodel_pct_heavy.xml`` + ``output/patchworks_k3z_pct_heavy_validated/fragments/fragments.shp``
     - Adds ``SILV_STATE`` plus a planted-only heavy PCT gate, but no CT or fertilization chain.
     - ``PCT`` treated products, AU-wise standing stems-per-ha, AU-wise harvested-stem QMD numerator / treated-area / live ratio accounts for both ``PCT`` and ``CC``, plus species-wise managed yield / harvest-volume surfaces.
     - Heavy-intensity stand-tending teaching scaffold.
   * - ``basecase_riparian``
     - ``config/patchworks.runtime.overlay.basecase_riparian.windows.yaml`` + ``analysis/overlay_basecase_riparian.pin``
     - ``tracks_overlay_basecase_riparian/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_basecase_riparian_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``Basecase_Riparian`` field.
     - Only the managed/unmanaged split should change relative to baseline; the AU-wise standing stems-per-ha and harvested-QMD ``CC`` account contracts should remain parallel to baseline.
     - Baseline subvariant for riparian-style retained-area comparison.
   * - ``basecase_sum``
     - ``config/patchworks.runtime.overlay.basecase_sum.windows.yaml`` + ``analysis/overlay_basecase_sum.pin``
     - ``tracks_overlay_basecase_sum/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_basecase_sum_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``BaseCase_Sum`` field.
     - Only the managed/unmanaged split should change relative to baseline; the AU-wise standing stems-per-ha and harvested-QMD ``CC`` account contracts should remain parallel to baseline.
     - Baseline subvariant for the student's summed base-case retention.
   * - ``scenario1_sum``
     - ``config/patchworks.runtime.overlay.scenario1_sum.windows.yaml`` + ``analysis/overlay_scenario1_sum.pin``
     - ``tracks_overlay_scenario1_sum/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_scenario1_sum_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``Scenario1_Sum`` field.
     - Only the managed/unmanaged split should change relative to baseline; the AU-wise standing stems-per-ha and harvested-QMD ``CC`` account contracts should remain parallel to baseline.
     - Baseline subvariant for the student's first scenario retention.
   * - ``scenario2_sum``
     - ``config/patchworks.runtime.overlay.scenario2_sum.windows.yaml`` + ``analysis/overlay_scenario2_sum.pin``
     - ``tracks_overlay_scenario2_sum/`` + baseline ``yield/forestmodel.xml`` + ``output/patchworks_k3z_overlay_scenario2_sum_validated/fragments/fragments.shp``
     - Baseline fragment ``RETENTION`` is replaced by the student's ``Scenario2_Sum`` field.
     - Only the managed/unmanaged split should change relative to baseline; the AU-wise standing stems-per-ha and harvested-QMD ``CC`` account contracts should remain parallel to baseline.
     - Baseline subvariant for the student's second scenario retention.

How to Choose a Surface
-----------------------

1. Start with ``base`` unless you explicitly need a treatment scaffold or an
   overlay sensitivity surface.
2. Choose ``ctfert_l15h5`` or ``ctfert_l20h0`` when the class exercise is
   about SI-specific fertilization response across the six ``L/M/H`` CT-eligible
   ``CWHvm_FDC+HW`` / ``CWHvm_CW+HW`` AUs.
3. Choose one of ``intensive_light``, ``intensive_moderate``, or
   ``intensive_heavy`` when the class exercise needs the full
   ``PCT -> CT -> F1 -> F2 -> F3`` scaffold on one launchable K3Z surface.
4. Choose one of ``pct_light``, ``pct_moderate``, or ``pct_heavy`` when
   the class exercise needs PCT intensity comparison without CT or fertilization.
5. Choose one of the four overlay subvariants only when the exercise is about
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

For the repeatable student/operator workflow, use
:doc:`overlay-subvariants-workflow`.

Audit Checklist
---------------

- Keep the runtime config and PIN paired exactly as listed above.
- Compare overlay subvariants against ``base`` first, not against each other.
- Confirm the overlay source table still resolves 1:1 against the canonical
  fragments surface before interpreting results.
- Treat unexpected treatment-path changes on overlay subvariants as a bug,
  because overlays are intended to modify retained area only.
