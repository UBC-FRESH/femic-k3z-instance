Operator Runbook
================

Fresh Setup
-----------

1. Initialize submodules and environment.
2. Validate prerequisites with case preflight.
3. Confirm Patchworks runtime config resolves correctly.
4. On Windows, confirm native runtime prerequisites are present:

- `git`
- `git-annex`
- DataLad (usually via `.venv\Scripts\datalad.exe`)
- Java
- Patchworks
- bundled native `VDYP7Console.exe`
- ArcGIS Pro Python for the SiteProd fallback path

.. code-block:: bash

   git submodule update --init --recursive
   femic prep validate-case --run-config config/run_profile.k3z.yaml --tipsy-config-dir config/tipsy
   femic patchworks preflight --config config/patchworks.runtime.windows.yaml

Rebuild Workflow
----------------

.. code-block:: bash

   femic run --run-config config/run_profile.k3z.yaml --run-id k3z_full_rebuild

At this point FEMIC is expected to stop at the BatchTIPSY freshness boundary.
The canonical handoff files are:

- `data/02_input-tsak3z.dat`
- `data/tipsy_params_tsak3z.xlsx`

Run BatchTIPSY manually on Windows, refresh `data/04_output-tsak3z.out`, then resume:

.. code-block:: bash

   femic tsa post-tipsy --run-config config/run_profile.k3z.yaml --tsa k3z --run-id k3z_full_rebuild
   femic patchworks build-blocks --config config/patchworks.runtime.windows.yaml
   femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_full_rebuild

Diagnostics Workflow
--------------------

.. code-block:: bash

   femic run --run-config config/run_profile.k3z.yaml --run-id k3z_reprocheck
   femic tsa post-tipsy --run-config config/run_profile.k3z.yaml --tsa k3z --run-id k3z_reprocheck
   femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_reprocheck

Review:

- ``vdyp_io/logs/patchworks_matrixbuilder_manifest-<run_id>.json``

Surface Selection Cheatsheet
----------------------------

.. list-table::
   :header-rows: 1

   * - If you need...
     - Launch this
   * - accepted teaching baseline
     - ``config/patchworks.runtime.windows.yaml`` + ``analysis/base.pin``
   * - CT plus fertilization
     - ``config/patchworks.runtime.ctfert.windows.yaml`` + ``analysis/ctfert.pin``
   * - light PCT-only surface
     - ``config/patchworks.runtime.pct_light.windows.yaml`` + ``analysis/pct_light.pin``
   * - moderate PCT-only surface
     - ``config/patchworks.runtime.pct_moderate.windows.yaml`` + ``analysis/pct_moderate.pin``
   * - heavy PCT-only surface
     - ``config/patchworks.runtime.pct_heavy.windows.yaml`` + ``analysis/pct_heavy.pin``
   * - retained-area sensitivity only
     - one of the overlay runtime configs + the matching ``analysis/overlay_*.pin``

Optional CT/Fert Variant Workflow
---------------------------------

Use this only if you intentionally want the teaching variant with commercial
thinning, provisional QMD, and provisional ``F1`` / ``F2`` / ``F3``
fertilization.

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.ctfert.windows.yaml --run-id k3z_ctfert

Variant review points:

- ``config/patchworks.variant.ctfert.yaml`` is the variant spec.
- ``config/silviculture.k3z.ctfert.yaml`` controls the optional treatment scaffold.
- ``models/k3z_patchworks_model/analysis/ctfert.pin`` is the Patchworks launch entrypoint.
- ``models/k3z_patchworks_model/tracks_ctfert/treatments.csv`` should materialize ``CT``, ``F1``, ``F2``, and ``F3``.
- ``models/k3z_patchworks_model/tracks_ctfert/accounts.csv`` / ``products.csv`` should include
  ``product.Treated.managed.{CT,F1,F2,F3}``.
- Patchworks smoke expectation: pulling on the ``F3`` treated-area target should
  induce the upstream chain ``F2`` -> ``F1`` -> ``CT`` -> ``CC``.
- Deep reference: :doc:`silviculture-logic`

Optional PCT-Only Subvariant Workflow
-------------------------------------

Use this only if you intentionally want the teaching variant with
pre-commercial thinning only.

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.pct_light.windows.yaml --run-id k3z_pct_light
   femic patchworks matrix-build --config config/patchworks.runtime.pct_moderate.windows.yaml --run-id k3z_pct_moderate
   femic patchworks matrix-build --config config/patchworks.runtime.pct_heavy.windows.yaml --run-id k3z_pct_heavy

Variant review points:

- `pct_light`:
  - variant spec: ``config/patchworks.variant.pct_light.yaml``
  - silviculture config: ``config/silviculture.k3z.pct_light.yaml``
  - launch entrypoint: ``models/k3z_patchworks_model/analysis/pct_light.pin``
  - tracks surface: ``models/k3z_patchworks_model/tracks_pct_light/``
- `pct_moderate`:
  - variant spec: ``config/patchworks.variant.pct_moderate.yaml``
  - silviculture config: ``config/silviculture.k3z.pct_moderate.yaml``
  - launch entrypoint: ``models/k3z_patchworks_model/analysis/pct_moderate.pin``
  - tracks surface: ``models/k3z_patchworks_model/tracks_pct_moderate/``
- `pct_heavy`:
  - variant spec: ``config/patchworks.variant.pct_heavy.yaml``
  - silviculture config: ``config/silviculture.k3z.pct_heavy.yaml``
  - launch entrypoint: ``models/k3z_patchworks_model/analysis/pct_heavy.pin``
  - tracks surface: ``models/k3z_patchworks_model/tracks_pct_heavy/``
- Each ``tracks_pct_*`` surface should materialize ``PCT`` and not ``CT``.
- Each ``tracks_pct_*`` ``accounts.csv`` / ``products.csv`` should include
  ``product.Treated.managed.PCT`` and exclude ``product.Treated.managed.CT``.
- Each ``output/patchworks_k3z_pct_*_validated/fragments/`` surface should
  preserve the accepted baseline 218-fragment geometry footprint exactly.
- Patchworks smoke expectation: pulling on the ``PCT`` treated-area target
  should induce the upstream chain ``CC``.
- Each ``tracks_pct_*`` ``accounts.csv`` / ``products.csv`` should also
  retain species-wise managed yield / harvest-volume surfaces, not just
  ``Total``.
- Deep reference: :doc:`silviculture-logic`

Baseline Overlay Subvariant Workflow
------------------------------------

Use these only when the exercise is specifically about alternative retained
area on top of the accepted baseline surface.

Use :doc:`overlay-subvariants-workflow` as the canonical source for the source
contract, subvariant meanings, and audit expectations.

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.overlay.basecase_riparian.windows.yaml --run-id k3z_overlay_basecase_riparian
   femic patchworks matrix-build --config config/patchworks.runtime.overlay.basecase_sum.windows.yaml --run-id k3z_overlay_basecase_sum
   femic patchworks matrix-build --config config/patchworks.runtime.overlay.scenario1_sum.windows.yaml --run-id k3z_overlay_scenario1_sum
   femic patchworks matrix-build --config config/patchworks.runtime.overlay.scenario2_sum.windows.yaml --run-id k3z_overlay_scenario2_sum

Review points:

- confirm the intended overlay runtime config and overlay PIN are paired;
- confirm only fragment ``RETENTION`` differs from baseline;
- confirm managed/unmanaged area shifts are explainable from the selected
  overlay retention column;
- confirm any missing managed species accounts are consistent with high
  retained area, not with a bad tracks surface.

Deep references:

- :doc:`variants-and-subvariants`
- :doc:`overlay-subvariants-workflow`

Old-Growth Review Workflow
--------------------------

After a normal baseline rebuild on ``main``, confirm the old-growth surfaces are
present in compiled accounts:

- ``feature.Area.og1.<au_token>``
- ``feature.Area.og2.<au_token>``
- ``feature.Area.og1.total``
- ``feature.Area.og2.total``

Deep reference: :doc:`old-growth-attributes`

Troubleshooting Workflow
------------------------

1. Preflight failure: fix runtime paths/license prerequisites first.
2. Block join mismatch: rebuild blocks and rerun matrix builder.
3. Account anomalies: trace curves -> attributes/products -> accounts.
4. Optional variant anomalies: confirm you launched the intended PIN/runtime pair and that
   ``config/silviculture.k3z.ctfert.yaml`` matches the expected treatment-path build.
5. On the selected ``pct_*`` subvariant, confirm the matching
   ``config/silviculture.k3z.pct_*.yaml`` matches the expected treatment-path
   build and that the corresponding ``tracks_pct_*`` surface is active.

Release Checklist
-----------------

- Rebuild and matrix-build complete without hard errors.
- Invariant report passes baseline checks.
- Required docs pages and contract tests pass.
- Published docs navigation resolves and includes current pages.
- If releasing the optional CT/fert variant, confirm the variant spec, runtime config,
  and ``ctfert.pin`` launch instructions are documented for student groups.
- If releasing the optional PCT-only subvariants, confirm the light/moderate/
  heavy variant specs, runtime configs, and ``pct_*.pin`` launch
  instructions are documented for student groups.

Publication Checklist
---------------------

- Standalone docs build with warnings-as-errors:

  .. code-block:: bash

     python -m sphinx -b html docs docs/_build/html -W

- Parent docs contracts and full validation gates pass before release.

Baseline K3Z Policy Checks
--------------------------

Confirm the current baseline assumptions are still true after rebuild:

- managed curves come from real BatchTIPSY output
- `CWHvm_CW+YC` and `CWHvm_CW+PLC` do not appear in the treated/TIPSY handoff
- those low-yield strata are retained out of THLB via `RETENTION = 1.0`
- remaining treated AUs follow the simplified teaching planting logic in
  `config/tipsy/tsak3z.yaml`
