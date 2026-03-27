Silviculture Logic
==================

Purpose
-------

This page documents the actual treatment parameters, gating fields, and
sequencing logic for the shipped intensive-silviculture K3Z variant families.

Control Fields
--------------

- ``ORIGIN`` distinguishes natural vs planted composition.
- ``IFM`` distinguishes managed vs unmanaged land-base behavior.
- ``SILV_STATE`` carries treatment history for the intensive variants.

In all intensive variants, treatment history is carried by ``SILV_STATE``,
not by overloading ``ORIGIN``.

Gate Summary
------------

- ``ORIGIN`` gates entry into both intensive paths: only planted-origin stands
  are eligible.
- ``SILV_STATE`` records where a stand currently sits in the treatment chain
  and therefore gates the next treatment in sequence.
- ``IFM`` still separates managed vs unmanaged land-base behavior; unmanaged
  tracks do not enter the intensive treatment chains.

CT/Fert Variant Family
----------------------

Canonical control files:

- ``config/patchworks.variant.ctfert_l15h5.yaml`` +
  ``config/silviculture.k3z.ctfert_l15h5.yaml``
- ``config/patchworks.variant.ctfert_l20h0.yaml`` +
  ``config/silviculture.k3z.ctfert_l20h0.yaml``

Treatment parameter table:

.. list-table::
   :header-rows: 1

   * - Element
     - Current implementation
   * - Eligible AUs
     - ``985502001`` and ``985502002``
   * - SI-profiled CT/fert subvariants
     - ``ctfert_l15h5`` and ``ctfert_l20h0``
   * - SI-profiled eligible AUs
     - ``985501001``, ``985502001``, ``985503001``, ``985501002``, ``985502002``, and ``985503002``
   * - Eligibility gate
     - planted-only path (``min_origin: planted``)
   * - State transition field
     - ``SILV_STATE``
   * - CT transition
     - ``cc_pl -> cc_pl_ct``
   * - CT age
     - age ``40`` for both eligible AUs
   * - CT removal
     - ``basal_area_removal_fraction = 0.30``
   * - BA:volume conversion
     - ``basal_area_to_volume_ratio = 1.0``
   * - CT final-felling gap factor
     - ``final_felling_gap_factor = 1.0`` means the post-CT final-felling volume gap stays equal to the CT harvest volume; ``0.0`` means that gap linearly closes by ``cmai_argmax``
   * - F1 transition
     - ``cc_pl_ct -> cc_pl_ct_f1`` at ``cai_argmax``
   * - F2 transition
     - ``cc_pl_ct_f1 -> cc_pl_ct_f1_f2`` after ``10`` years
   * - F3 transition
     - ``cc_pl_ct_f1_f2 -> cc_pl_ct_f1_f2_f3`` after ``10`` years
   * - Fert response window
     - ``response_years = 10``
   * - Fert growth speedup
     - ``growth_speedup_fraction = 0.10``
   * - SI-profiled fert growth speedup
     - ``ctfert_l15h5`` = ``L=0.15``, ``M=0.10``, ``H=0.05``; ``ctfert_l20h0`` = ``L=0.20``, ``M=0.10``, and no fert on ``H`` AUs
   * - QMD source
     - reverse-engineered approximation from accepted stand yield, BatchTIPSY
       height/TPH where available, and linear site-index height plus VDYP-side
       stems-per-hectare proxies otherwise

SI-profile notes:

1. ``ctfert_l15h5`` keeps the full ``CT -> F1 -> F2 -> F3`` chain on all six
   eligible ``L/M/H`` AUs.
2. ``ctfert_l20h0`` keeps CT on all six eligible ``L/M/H`` AUs but disables
   fertilization entirely on the two ``H``-class AUs instead of compiling a
   null-effect fert chain there.
3. Both SI-profile subvariants use the curated CT/fert retention overlay in
   ``tmp/CTFert Fragments/fragments_updated3_Usedinbasecase.shp``.
4. Both SI-profile subvariants now set ``commercial_thinning.final_felling_gap_factor``
   to ``0.0``, so the immediate CT harvest still occurs at age 40 but the
   residual final-felling volume gap is forced to taper to zero by
   ``cmai_argmax`` instead of remaining fixed forever.
5. That curated fragments source replaces the old placeholder
   ``RETENTION = 0.05`` pattern with the student-provided per-fragment
   ``RETENTION`` values on the shipped validated ``ctfert_l15h5`` and
   ``ctfert_l20h0`` surfaces.

Sequencing logic:

1. ``CC`` establishes the planted path.
2. ``CT`` is available only on the planted eligible AUs at the configured age.
3. ``F1`` is available only after ``CT`` and fires at ``cai_argmax``.
4. ``F2`` is available only after ``F1`` and waits ``10`` years.
5. ``F3`` is available only after ``F2`` and waits ``10`` years.

Retention and low-yield policy in this variant:

- default retained fraction is ``0.05``;
- ``CWHvm_CW+YC`` and ``CWHvm_CW+PLC`` remain full-retention strata;
- those low-yield strata stay out of the treated/TIPSY path even on the
  intensive variant.

PCT-Only Subvariants
--------------------

Canonical control files:

- ``config/patchworks.variant.pct_light.yaml`` +
  ``config/silviculture.k3z.pct_light.yaml``
- ``config/patchworks.variant.pct_moderate.yaml`` +
  ``config/silviculture.k3z.pct_moderate.yaml``
- ``config/patchworks.variant.pct_heavy.yaml`` +
  ``config/silviculture.k3z.pct_heavy.yaml``

Treatment parameter table:

.. list-table::
   :header-rows: 1

   * - Element
     - Current implementation
   * - Eligible AUs
     - ``985502000``, ``985503000``, ``985502001``, and ``985503001``
   * - Subvariant names
     - ``pct_light``, ``pct_moderate``, and ``pct_heavy``
   * - Eligibility gate
     - planted-only path (``min_origin: planted``)
   * - State transition field
     - ``SILV_STATE``
   * - PCT transition
     - ``cc_pl -> cc_pl_pct``
   * - PCT age
     - age ``10`` for all eligible AUs
   * - Planted regen mix
     - ``900 CW + 3100 HW`` for all eligible AUs
   * - PCT flavors
     - ``pct_light`` removes ``1000`` HW stems/ha, ``pct_moderate`` removes ``2000``, and ``pct_heavy`` removes ``3000``
   * - Post-PCT managed mixes
     - ``900 CW + 2100 HW``, ``900 CW + 1100 HW``, and ``900 CW + 100 HW``

Sequencing logic:

1. ``CC`` establishes the planted path.
2. One age-10 ``PCT`` option is available per selected ``pct_*``
   subvariant.
3. The selected subvariant controls how much ``HW`` (Western Hemlock) is
   removed from the planted path:
   - ``pct_light``: remove ``1000`` stems/ha
   - ``pct_moderate``: remove ``2000`` stems/ha
   - ``pct_heavy``: remove ``3000`` stems/ha
4. No ``CT`` / ``F1`` / ``F2`` / ``F3`` chain is compiled in this variant.

Full-Intensive Subvariants
--------------------------

Canonical control files:

- ``config/patchworks.variant.intensive_light.yaml`` +
  ``config/silviculture.k3z.intensive_light.yaml``
- ``config/patchworks.variant.intensive_moderate.yaml`` +
  ``config/silviculture.k3z.intensive_moderate.yaml``
- ``config/patchworks.variant.intensive_heavy.yaml`` +
  ``config/silviculture.k3z.intensive_heavy.yaml``

Treatment parameter table:

.. list-table::
   :header-rows: 1

   * - Element
     - Current implementation
   * - Eligible AUs
     - ``985501001``, ``985502001``, ``985503001``, ``985501002``, ``985502002``, ``985503002``, ``985502000``, and ``985503000``
   * - Subvariant names
     - ``intensive_light``, ``intensive_moderate``, and ``intensive_heavy``
   * - Eligibility gate
     - planted-only path (``min_origin: planted``)
   * - State transition field
     - ``SILV_STATE``
   * - Combined state chain
     - ``cc_pl -> cc_pl_pct -> cc_pl_pct_ct -> cc_pl_ct_f1 -> cc_pl_ct_f1_f2 -> cc_pl_ct_f1_f2_f3``
   * - PCT transition
     - ``cc_pl -> cc_pl_pct`` at age ``10``
   * - CT transition
     - ``cc_pl_pct -> cc_pl_pct_ct`` at age ``40``
   * - PCT flavors
     - ``intensive_light`` removes ``1000`` HW stems/ha, ``intensive_moderate`` removes ``2000``, and ``intensive_heavy`` removes ``3000``
   * - Fert response profile
     - reuse the accepted ``ctfert_l15h5`` profile: ``L=15%``, ``M=10%``, ``H=5%``
   * - F1 transition
     - ``cc_pl_pct_ct -> cc_pl_ct_f1`` at ``cai_argmax``
   * - F2 transition
     - ``cc_pl_ct_f1 -> cc_pl_ct_f1_f2`` after ``10`` years
   * - F3 transition
     - ``cc_pl_ct_f1_f2 -> cc_pl_ct_f1_f2_f3`` after ``10`` years
   * - CT final-felling gap factor
     - ``0.0`` so the residual final-felling volume gap tapers to zero by ``cmai_argmax``
   * - Curated retention overlay
     - reuse the accepted CT/fert curated fragments surface from ``tmp/CTFert Fragments/fragments_updated3_Usedinbasecase.shp``

Sequencing logic:

1. ``CC`` establishes the planted path.
2. One age-10 ``PCT`` option is compiled per selected ``intensive_*``
   subvariant.
3. ``CT`` is available only after ``PCT`` and only on the eight eligible AUs.
4. ``F1`` is available only after ``CT`` and fires at ``cai_argmax``.
5. ``F2`` is available only after ``F1`` and waits ``10`` years.
6. ``F3`` is available only after ``F2`` and waits ``10`` years.

State Machines
--------------

``ctfert_l15h5`` / ``ctfert_l20h0`` states:

- ``baseline``
- ``cc_pl``
- ``cc_pl_ct``
- ``cc_pl_ct_f1``
- ``cc_pl_ct_f1_f2``
- ``cc_pl_ct_f1_f2_f3``

``pct_*`` states:

- ``baseline``
- ``cc_pl``
- ``cc_pl_pct``

``intensive_*`` states:

- ``baseline``
- ``cc_pl``
- ``cc_pl_pct``
- ``cc_pl_pct_ct``
- ``cc_pl_ct_f1``
- ``cc_pl_ct_f1_f2``
- ``cc_pl_ct_f1_f2_f3``

Interpretation Notes
--------------------

- Use ``ctfert_l15h5`` or ``ctfert_l20h0`` when the teaching question is about
  SI-specific fertilization response differences across the six eligible
  ``CWHvm_FDC+HW`` / ``CWHvm_CW+HW`` AUs.
- Use ``pct_light`` / ``pct_moderate`` / ``pct_heavy`` when the teaching
  question is about comparing PCT intensity on an otherwise consistent
  planted stand-tending path.
- Use ``intensive_light`` / ``intensive_moderate`` / ``intensive_heavy`` when
  the teaching question needs the full ``PCT -> CT -> F1 -> F2 -> F3``
  treatment scaffold on one launchable K3Z surface.
- Do not interpret these surfaces as polished operational prescriptions; they
  are explicit teaching scaffolds built from YAML-facing assumptions.
