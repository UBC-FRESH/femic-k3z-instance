Edit Policy and Scenarios
=========================

Edit Policy Matrix
------------------

.. list-table::
   :header-rows: 1

   * - Asset Class
     - Policy
     - Rationale
   * - ``config/*.yaml``
     - Safe to edit
     - Scenario and runtime controls are intentional operator inputs.
   * - ``docs/*.rst``
     - Safe to edit
     - Narrative/metadata documentation evolves with model understanding.
   * - ``data/model_input_bundle/*.csv``
     - Regenerate preferred
     - Generated from upstream logic; direct edits are fragile.
   * - ``models/k3z_patchworks_model/tracks/*.csv``
     - Regenerate preferred
     - Matrix builder outputs; hand edits can break joins/targets.
   * - ``models/k3z_patchworks_model/yield/forestmodel.xml``
     - Regenerate preferred
     - Export product tied to source assumptions and curve logic.

Scenario Comparison Guidance
----------------------------

Compare scenarios using consistent metrics and reporting windows:

- managed total/product yields,
- species-wise managed products,
- seral-stage area and treatment-shift trajectories,
- old-growth area trajectories from ``og1`` / ``og2``,
- key constraints/targets and infeasibility indicators.

Interpretation Workflow
-----------------------

1. Run baseline and variant scenarios with explicit run-ids.
2. Compare account trajectories period-by-period.
3. Flag differences caused by assumption changes vs data/build drift.

Optional CT/Fert Branch Guidance
--------------------------------

The CT/QMD/fert work is intentionally isolated as a variant spec/runtime/PIN set so only some student groups need to
pull it.

Recommended workflow:

1. Start from a clean, accepted ``main`` baseline.
2. If your group needs CT/fert, use the CT/fert variant spec and launch ``analysis/ctfert.pin``.
3. If your group needs the PCT->CT teaching scaffold, choose one of
   ``pctct_light``, ``pctct_moderate``, or ``pctct_heavy`` and launch the
   matching ``analysis/pctct_*.pin`` surface.
4. Rebuild before interpreting any optional-variant surfaces.
5. Keep variant choice explicit in reports, screenshots, and classroom notes.
6. Use the overlay subvariants only when the question is about retained-area
   sensitivity on top of baseline.
7. Keep any K3Z-specific VDYP fit exceptions in ``config/vdyp_fit_policy.yaml``
   so DR+HW tail-policy changes remain auditable and do not require parent
   source edits.

Classroom Use Guidance
----------------------

- Start from reproducible baseline before exploring policy changes.
- Change one assumption family at a time when teaching sensitivity.
- Preserve run manifests/reports for each scenario to support auditability.
- Treat the optional CT/fert variant as a teaching/scenario scaffold, not a
  polished silviculture prescription package.

How to Validate Reruns
----------------------

1. Confirm matrix-build manifest success.
2. Confirm rebuild report invariants pass.
3. Confirm scenario deltas are explainable by intentional config edits.
4. On the optional variant, confirm compiled tracks and live Patchworks behavior
   agree about the ``CT`` -> ``F1`` -> ``F2`` -> ``F3`` chain.
5. On the selected ``pctct_*`` subvariant, confirm compiled tracks and live
   Patchworks behavior agree about the ``PCT`` -> ``CT`` -> ``CC`` chain.
6. On overlay subvariants, confirm the only intended behavioral change is the
   managed-vs-unmanaged split driven by fragment ``RETENTION``.

Deep references
---------------

- launch matrix and overlay provenance: :doc:`variants-and-subvariants`
- repeatable overlay student/operator workflow: :doc:`overlay-subvariants-workflow`
- treatment parameter tables and state machines: :doc:`silviculture-logic`
- old-growth semantics: :doc:`old-growth-attributes`
