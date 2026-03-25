Getting Started
===============

Purpose
-------

``femic-k3z-instance`` is a runnable, versioned K3Z deployment instance for
teaching and collaboration.

This repository now carries multiple coexisting Patchworks variants inside one
instance checkout.

Current variants:

- baseline teaching variant
  - no separate variant spec file; baseline is the default runtime surface
  - runtime config: ``config/patchworks.runtime.windows.yaml``
  - Patchworks PIN: ``models/k3z_patchworks_model/analysis/base.pin``
- optional CT/QMD/fert variant
  - variant spec: ``config/patchworks.variant.ctfert.yaml``
  - runtime config: ``config/patchworks.runtime.ctfert.windows.yaml``
  - Patchworks PIN: ``models/k3z_patchworks_model/analysis/ctfert.pin``
- optional PCT->CT light subvariant:
  ``config/patchworks.variant.pctct_light.yaml`` +
  ``config/patchworks.runtime.pctct_light.windows.yaml`` +
  ``models/k3z_patchworks_model/analysis/pctct_light.pin``
- optional PCT->CT moderate subvariant:
  ``config/patchworks.variant.pctct_moderate.yaml`` +
  ``config/patchworks.runtime.pctct_moderate.windows.yaml`` +
  ``models/k3z_patchworks_model/analysis/pctct_moderate.pin``
- optional PCT->CT heavy subvariant:
  ``config/patchworks.variant.pctct_heavy.yaml`` +
  ``config/patchworks.runtime.pctct_heavy.windows.yaml`` +
  ``models/k3z_patchworks_model/analysis/pctct_heavy.pin``

Baseline-derived overlay subvariants:

- ``basecase_riparian``
- ``basecase_sum``
- ``scenario1_sum``
- ``scenario2_sum``

For the repeatable overlay workflow, use :doc:`overlay-subvariants-workflow`.

Students should choose a variant by config/PIN, not by switching git branches.

The intended launch pairings are:

- baseline: ``config/patchworks.runtime.windows.yaml`` + ``analysis/base.pin``
- CT/fert variant: ``config/patchworks.runtime.ctfert.windows.yaml`` + ``analysis/ctfert.pin``
- PCT->CT light subvariant: ``config/patchworks.runtime.pctct_light.windows.yaml`` + ``analysis/pctct_light.pin``
- PCT->CT moderate subvariant: ``config/patchworks.runtime.pctct_moderate.windows.yaml`` + ``analysis/pctct_moderate.pin``
- PCT->CT heavy subvariant: ``config/patchworks.runtime.pctct_heavy.windows.yaml`` + ``analysis/pctct_heavy.pin``

For the full launch matrix, use :doc:`variants-and-subvariants`.

Quick Surface Picker
--------------------

.. list-table::
   :header-rows: 1

   * - Use case
     - Recommended surface
   * - Default teaching runs, baseline comparisons, and old-growth review
     - ``base``
   * - CT plus fertilization teaching exercise
     - ``ctfert``
   * - PCT-gated CT teaching exercise
     - ``pctct_light``, ``pctct_moderate``, or ``pctct_heavy``
   * - Retained-area sensitivity exercise driven by the student workbook
     - one of the four baseline overlay subvariants

Prerequisites
-------------

- Python environment with ``femic`` installed.
- Patchworks runtime installed and licensed on the host machine.
- Local checkout with required submodules initialized.

Quickstart
----------

1. Validate case prerequisites:

   .. code-block:: bash

      femic prep validate-case --run-config config/run_profile.k3z.yaml --tipsy-config-dir config/tipsy

2. Compile/rebuild upstream inputs:

   .. code-block:: bash

      femic run --run-config config/run_profile.k3z.yaml --run-id k3z_stage01a

3. Run BatchTIPSY manually on Windows using the freshly generated:

   - `data/02_input-tsak3z.dat`
   - `data/tipsy_params_tsak3z.xlsx` (or the current timestamped fallback workbook if Excel had the canonical workbook locked)

4. Resume downstream from the fresh BatchTIPSY output:

   .. code-block:: bash

      femic tsa post-tipsy --run-config config/run_profile.k3z.yaml --tsa k3z --run-id k3z_stage01a

5. Run the baseline Patchworks matrix build:

   .. code-block:: bash

      femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_baseline

6. Run the optional CT/fert Patchworks matrix build:

   .. code-block:: bash

      femic patchworks matrix-build --config config/patchworks.runtime.ctfert.windows.yaml --run-id k3z_ctfert

7. Run one of the optional PCT->CT subvariant matrix builds:

   .. code-block:: bash

      femic patchworks matrix-build --config config/patchworks.runtime.pctct_light.windows.yaml --run-id k3z_pctct_light
      femic patchworks matrix-build --config config/patchworks.runtime.pctct_moderate.windows.yaml --run-id k3z_pctct_moderate
      femic patchworks matrix-build --config config/patchworks.runtime.pctct_heavy.windows.yaml --run-id k3z_pctct_heavy

Variant-Specific Operator Inputs
--------------------------------

Baseline teaching variant:

- ``config/patchworks.runtime.windows.yaml``
- ``models/k3z_patchworks_model/analysis/base.pin``
- deep reference: :doc:`variants-and-subvariants`

Optional CT/fert variant:

- ``config/patchworks.variant.ctfert.yaml``
- ``config/silviculture.k3z.ctfert.yaml``

The CT/fert variant YAML controls:

- CT eligibility AUs,
- CT age and removal assumptions,
- provisional BA:volume conversion,
- fertilization response window and speedup fraction,
- ``F1`` / ``F2`` / ``F3`` timing rules.
- deep reference: :doc:`silviculture-logic`

Optional PCT->CT subvariants:

- ``config/patchworks.variant.pctct_light.yaml`` +
  ``config/silviculture.k3z.pctct_light.yaml``
- ``config/patchworks.variant.pctct_moderate.yaml`` +
  ``config/silviculture.k3z.pctct_moderate.yaml``
- ``config/patchworks.variant.pctct_heavy.yaml`` +
  ``config/silviculture.k3z.pctct_heavy.yaml``

The three PCT->CT subvariant YAMLs share the same:

- issue-14 eligible AU cohort: medium/high SI ``HW+FDC`` and ``FDC+HW``
  AUs ``985502000``, ``985503000``, ``985502001``, and ``985503001``,
- planted regen mix: ``900 CW + 3100 HW``,
- PCT timing: age ``10``,
- CT timing: age ``40``,
- treatment-state chain: ``cc_pl -> cc_pl_pct -> cc_pl_pct_ct``,
- no-fertilization policy.

The subvariant-specific PCT flavors are:

- ``pctct_light``: remove ``1000`` HW stems/ha, leaving ``900 CW + 2100 HW``
- ``pctct_moderate``: remove ``2000`` HW stems/ha, leaving
  ``900 CW + 1100 HW``
- ``pctct_heavy``: remove ``3000`` HW stems/ha, leaving ``900 CW + 100 HW``
- deep reference: :doc:`silviculture-logic`

Baseline overlay subvariants:

- ``config/patchworks.runtime.overlay.basecase_riparian.windows.yaml``
- ``config/patchworks.runtime.overlay.basecase_sum.windows.yaml``
- ``config/patchworks.runtime.overlay.scenario1_sum.windows.yaml``
- ``config/patchworks.runtime.overlay.scenario2_sum.windows.yaml``
- deep references:
  - :doc:`variants-and-subvariants`
  - :doc:`overlay-subvariants-workflow`

Authoritative Paths
-------------------

- Patchworks model root:
  ``models/k3z_patchworks_model/``
- Baseline tracks:
  ``models/k3z_patchworks_model/tracks/``
- CT/fert tracks:
  ``models/k3z_patchworks_model/tracks_ctfert/``
- PCT->CT light tracks:
  ``models/k3z_patchworks_model/tracks_pctct_light/``
- PCT->CT moderate tracks:
  ``models/k3z_patchworks_model/tracks_pctct_moderate/``
- PCT->CT heavy tracks:
  ``models/k3z_patchworks_model/tracks_pctct_heavy/``
- Runtime logs/manifests:
  ``vdyp_io/logs/``

Baseline K3Z Policy Notes
-------------------------

- Managed curves now come from real BatchTIPSY output.
- `CWHvm_CW+YC` and `CWHvm_CW+PLC` are intentionally excluded from the
  treated/TIPSY path and retained out of THLB with `RETENTION = 1.0`.
- Remaining treated AUs use the simplified teaching planting rules documented
  in `config/tipsy/tsak3z.yaml`.
- The accepted K3Z-specific VDYP smoothing exceptions for ``CWHvm_DR+HW`` now
  live in ``config/vdyp_fit_policy.yaml`` beside the instance rather than in
  parent FEMIC source code.
- ``og1`` / ``og2`` semantics are documented in :doc:`old-growth-attributes`.
