Silviculture Logic
==================

Purpose
-------

This page documents the actual treatment parameters, gating fields, and
sequencing logic for the two intensive-silviculture K3Z variants.

Control Fields
--------------

- ``ORIGIN`` distinguishes natural vs planted composition.
- ``IFM`` distinguishes managed vs unmanaged land-base behavior.
- ``SILV_STATE`` carries treatment history for the intensive variants.

In both intensive variants, treatment history is carried by ``SILV_STATE``,
not by overloading ``ORIGIN``.

Gate Summary
------------

- ``ORIGIN`` gates entry into both intensive paths: only planted-origin stands
  are eligible.
- ``SILV_STATE`` records where a stand currently sits in the treatment chain
  and therefore gates the next treatment in sequence.
- ``IFM`` still separates managed vs unmanaged land-base behavior; unmanaged
  tracks do not enter the intensive treatment chains.

CT/Fert Variant
---------------

Canonical control files:

- ``config/patchworks.variant.ctfert.yaml``
- ``config/silviculture.k3z.ctfert.yaml``

Treatment parameter table:

.. list-table::
   :header-rows: 1

   * - Element
     - Current implementation
   * - Eligible AUs
     - ``985502001`` and ``985502002``
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
   * - QMD source
     - synthetic placeholder

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

PCT->CT Variant
---------------

Canonical control files:

- ``config/patchworks.variant.pctct.yaml``
- ``config/silviculture.k3z.pctct.yaml``

Treatment parameter table:

.. list-table::
   :header-rows: 1

   * - Element
     - Current implementation
   * - Eligible AUs
     - ``985502001`` and ``985502002``
   * - Eligibility gate
     - planted-only path (``min_origin: planted``)
   * - State transition field
     - ``SILV_STATE``
   * - PCT transition
     - ``cc_pl -> cc_pl_pct``
   * - PCT age
     - age ``10`` for both eligible AUs
   * - Residual stems
     - ``900`` stems/ha
   * - Species removal rule
     - ``remove_species = HW``
   * - CT transition
     - ``cc_pl_pct -> cc_pl_pct_ct``
   * - CT age
     - age ``40`` for both eligible AUs
   * - CT removal
     - ``basal_area_removal_fraction = 0.30``
   * - BA:volume conversion
     - ``basal_area_to_volume_ratio = 1.0``
   * - Fertilization
     - disabled
   * - QMD source
     - synthetic placeholder

Sequencing logic:

1. ``CC`` establishes the planted path.
2. ``PCT`` is available only on the planted eligible AUs.
3. ``PCT`` removes the ``HW`` species component (Western Hemlock) from the
   planted path and leaves the residual post-PCT managed composition.
4. ``CT`` is available only after the ``PCT`` gate is satisfied.
5. No ``F1`` / ``F2`` / ``F3`` chain is compiled in this variant.

State Machines
--------------

``ctfert`` states:

- ``baseline``
- ``cc_pl``
- ``cc_pl_ct``
- ``cc_pl_ct_f1``
- ``cc_pl_ct_f1_f2``
- ``cc_pl_ct_f1_f2_f3``

``pctct`` states:

- ``baseline``
- ``cc_pl``
- ``cc_pl_pct``
- ``cc_pl_pct_ct``

Interpretation Notes
--------------------

- Use ``ctfert`` when the teaching question is about compounded treatment
  sequencing and fertilization response.
- Use ``pctct`` when the teaching question is about gating CT behind an earlier
  stand-tending treatment.
- Do not interpret these surfaces as polished operational prescriptions; they
  are explicit teaching scaffolds built from YAML-facing assumptions.
