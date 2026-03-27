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
2. If your group needs SI-specific CT/fert behavior, launch either
   ``analysis/ctfert_l15h5.pin`` or ``analysis/ctfert_l20h0.pin``.
3. If your group needs the PCT-only teaching scaffold, choose one of
   ``pct_light``, ``pct_moderate``, or ``pct_heavy`` and launch the
   matching ``analysis/pct_*.pin`` surface.
4. If your group needs the full ``PCT -> CT -> F1 -> F2 -> F3`` teaching
   scaffold, choose one of ``intensive_light``, ``intensive_moderate``, or
   ``intensive_heavy`` and launch the matching ``analysis/intensive_*.pin``
   surface.
5. Rebuild before interpreting any optional-variant surfaces.
6. Keep variant choice explicit in reports, screenshots, and classroom notes.
7. Use the overlay subvariants only when the question is about retained-area
   sensitivity on top of baseline.
8. Keep any K3Z-specific VDYP fit exceptions in ``config/vdyp_fit_policy.yaml``
   so DR+HW tail-policy changes remain auditable and do not require parent
   source edits.

Classroom Use Guidance
----------------------

- Start from reproducible baseline before exploring policy changes.
- Change one assumption family at a time when teaching sensitivity.
- Preserve run manifests/reports for each scenario to support auditability.
- Treat the optional CT/fert variant as a teaching/scenario scaffold, not a
  polished silviculture prescription package.
- Treat the optional full-intensive family the same way: useful for classroom
  comparison of compounded treatments, but still a teaching scaffold.

How to Validate Reruns
----------------------

1. Confirm matrix-build manifest success.
2. Confirm rebuild report invariants pass.
3. Confirm scenario deltas are explainable by intentional config edits.
4. On the selected CT/fert surface, confirm compiled tracks and live Patchworks
   behavior agree about the intended ``CT`` -> ``F1`` -> ``F2`` -> ``F3`` chain,
   or CT-only behavior on ``H`` AUs for ``ctfert_l20h0``.
5. On the selected ``pct_*`` subvariant, confirm compiled tracks and live
   Patchworks behavior agree about the ``PCT`` -> ``CC`` chain.
6. On the selected ``intensive_*`` subvariant, confirm compiled tracks and live
   Patchworks behavior agree about the full
   ``PCT`` -> ``CT`` -> ``F1`` -> ``F2`` -> ``F3`` chain.
7. On overlay subvariants, confirm the only intended behavioral change is the
   managed-vs-unmanaged split driven by fragment ``RETENTION``.

Deep references
---------------

- launch matrix and overlay provenance: :doc:`variants-and-subvariants`
- repeatable overlay student/operator workflow: :doc:`overlay-subvariants-workflow`
- treatment parameter tables and state machines: :doc:`silviculture-logic`
- old-growth semantics: :doc:`old-growth-attributes`
