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

Runtime account assumptions
---------------------------

The shipped K3Z runtime configs now also carry a downstream recovered-volume
assumption in the ``protoaccounts.csv -> accounts.csv`` promotion layer:

- ``CC`` harvested volume uses utilization ``0.85``
- ``CT`` harvested volume uses utilization ``0.75`` on CT-enabled variants

This is a runtime-account policy only. It does not change standing yield
curves, ForestModel XML, or fragment-level ``RETENTION``.

Standing stems-per-ha account contract
--------------------------------------

The active K3Z launch surfaces now also ship AU-wise standing stems-per-ha
feature accounts:

- ``feature.StemsPerHa.managed.<au_token>``
- ``feature.StemsPerHa.unmanaged.<au_token>``

These are exported from ForestModel as feature attributes, then normalized
downstream during ``protoaccounts.csv -> accounts.csv`` promotion using the
AU-wise managed/unmanaged area implied by the validated fragments plus
``RETENTION``. Read the live ``feature.StemsPerHa.*`` accounts directly as mean
standing stems per hectare, not total stem counts.

Surface Selection Cheatsheet
----------------------------

.. list-table::
   :header-rows: 1

   * - If you need...
     - Launch this
   * - accepted teaching baseline
     - ``config/patchworks.runtime.windows.yaml`` + ``analysis/base.pin``
   * - CT plus fertilization with SI profile ``L15/M10/H5``
     - ``config/patchworks.runtime.ctfert_l15h5.windows.yaml`` + ``analysis/ctfert_l15h5.pin``
   * - CT plus fertilization with SI profile ``L20/M10/H0``
     - ``config/patchworks.runtime.ctfert_l20h0.windows.yaml`` + ``analysis/ctfert_l20h0.pin``
   * - light PCT-only surface
     - ``config/patchworks.runtime.pct_light.windows.yaml`` + ``analysis/pct_light.pin``
   * - moderate PCT-only surface
     - ``config/patchworks.runtime.pct_moderate.windows.yaml`` + ``analysis/pct_moderate.pin``
   * - heavy PCT-only surface
     - ``config/patchworks.runtime.pct_heavy.windows.yaml`` + ``analysis/pct_heavy.pin``
   * - full-intensive light surface
     - ``config/patchworks.runtime.intensive_light.windows.yaml`` + ``analysis/intensive_light.pin``
   * - full-intensive moderate surface
     - ``config/patchworks.runtime.intensive_moderate.windows.yaml`` + ``analysis/intensive_moderate.pin``
   * - full-intensive heavy surface
     - ``config/patchworks.runtime.intensive_heavy.windows.yaml`` + ``analysis/intensive_heavy.pin``
   * - retained-area sensitivity only
     - one of the overlay runtime configs + the matching ``analysis/overlay_*.pin``

Optional CT/Fert Variant Workflow
---------------------------------

Use this only if you intentionally want one of the teaching surfaces with
commercial thinning, approximate QMD, and ``F1`` / ``F2`` / ``F3``
fertilization.

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.ctfert_l15h5.windows.yaml --run-id k3z_ctfert_l15h5
   femic patchworks matrix-build --config config/patchworks.runtime.ctfert_l20h0.windows.yaml --run-id k3z_ctfert_l20h0

Variant review points:

- ``config/patchworks.variant.ctfert_l15h5.yaml`` and
  ``config/patchworks.variant.ctfert_l20h0.yaml`` are the SI-profile
  subvariant specs.
- ``models/k3z_patchworks_model/analysis/ctfert_l15h5.pin`` and
  ``models/k3z_patchworks_model/analysis/ctfert_l20h0.pin`` are the
  Patchworks launch entrypoints for those SI-profiled surfaces.
- ``tracks_ctfert_l15h5`` should compile ``CT`` plus ``F1`` / ``F2`` / ``F3``
  across the six eligible ``L/M/H`` AUs with boosts ``L=15%``, ``M=10%``,
  ``H=5%``.
- ``tracks_ctfert_l20h0`` should compile CT across the same six AUs but
  materialize ``F1`` / ``F2`` / ``F3`` only on the ``L/M`` cohort.
- The CT/fert tracks now expose AU-wise harvested-stem QMD numerator rows:
  - ``product.QMDNumerator.managed.<au_token>.CC``
  - ``product.QMDNumerator.managed.<au_token>.CT`` on the CT-eligible AUs
- The CT/fert tracks also expose AU-wise standing stems-per-ha feature rows:
  - ``feature.StemsPerHa.managed.<au_token>``
  - ``feature.StemsPerHa.unmanaged.<au_token>``
- Matching denominator rows:
  - ``product.Treated.managed.<au_token>.CC``
  - ``product.Treated.managed.<au_token>.CT``
- The live `ctfert_*` Patchworks PIN files register user-facing ratio accounts:
  - ``product.QMD.managed.<au_token>.CC``
  - ``product.QMD.managed.<au_token>.CT``
- Read those live ``product.QMD.*`` ratio accounts directly as mean harvested
  diameter in ``cm``.
- Read ``product.HarvestedVolume.*`` accounts as recovered merchantable volume,
  not perfect-recovery standing merchantable volume; ``CC`` uses downstream
  utilization ``0.85`` and ``CT`` uses downstream utilization ``0.75``.
- The two SI-profiled subvariants should use the curated retention overlay in
  ``tmp/CTFert Fragments/fragments_updated3_Usedinbasecase.shp`` rather than
  the old uniform ``RETENTION = 0.05`` placeholder. In other words, the
  checked-in validated fragments now carry the student-provided per-fragment
  ``RETENTION`` values, not the previous placeholder values.
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
- Each ``tracks_pct_*`` surface should also expose AU-wise harvested-stem QMD
  numerator rows:
  - ``product.QMDNumerator.managed.<au_token>.PCT``
  - ``product.QMDNumerator.managed.<au_token>.CC``
- Each ``tracks_pct_*`` surface should also expose AU-wise standing
  stems-per-ha feature rows:
  - ``feature.StemsPerHa.managed.<au_token>``
  - ``feature.StemsPerHa.unmanaged.<au_token>``
- Matching denominator rows:
  - ``product.Treated.managed.<au_token>.PCT``
  - ``product.Treated.managed.<au_token>.CC``
- The live ``pct_*`` Patchworks PIN files should register user-facing ratio
  accounts:
  - ``product.QMD.managed.<au_token>.PCT``
  - ``product.QMD.managed.<au_token>.CC``
- Read those live ``product.QMD.*`` ratio accounts directly as mean harvested
  diameter in ``cm``.
- Read ``product.HarvestedVolume.*`` accounts as recovered merchantable volume;
  ``CC`` uses downstream utilization ``0.85``. The shipped ``pct_*`` surfaces
  do not expose ``CT``, but the runtime layer reserves ``CT = 0.75`` for
  CT-enabled variants.
- Each ``output/patchworks_k3z_pct_*_validated/fragments/`` surface should
  preserve the accepted baseline 218-fragment geometry footprint exactly.
- Patchworks smoke expectation: pulling on the ``PCT`` treated-area target
  should induce the upstream chain ``CC``.
- Each ``tracks_pct_*`` ``accounts.csv`` / ``products.csv`` should also
  retain species-wise managed yield / harvest-volume surfaces, not just
  ``Total``.
- Deep reference: :doc:`silviculture-logic`

Optional Full-Intensive Subvariant Workflow
-------------------------------------------

Use this only if you intentionally want the full teaching scaffold with
``PCT -> CT -> F1 -> F2 -> F3`` on one launchable surface.

.. code-block:: bash

   femic patchworks matrix-build --config config/patchworks.runtime.intensive_light.windows.yaml --run-id k3z_intensive_light
   femic patchworks matrix-build --config config/patchworks.runtime.intensive_moderate.windows.yaml --run-id k3z_intensive_moderate
   femic patchworks matrix-build --config config/patchworks.runtime.intensive_heavy.windows.yaml --run-id k3z_intensive_heavy

Variant review points:

- `intensive_light`:
  - variant spec: ``config/patchworks.variant.intensive_light.yaml``
  - silviculture config: ``config/silviculture.k3z.intensive_light.yaml``
  - launch entrypoint: ``models/k3z_patchworks_model/analysis/intensive_light.pin``
  - tracks surface: ``models/k3z_patchworks_model/tracks_intensive_light/``
- `intensive_moderate`:
  - variant spec: ``config/patchworks.variant.intensive_moderate.yaml``
  - silviculture config: ``config/silviculture.k3z.intensive_moderate.yaml``
  - launch entrypoint: ``models/k3z_patchworks_model/analysis/intensive_moderate.pin``
  - tracks surface: ``models/k3z_patchworks_model/tracks_intensive_moderate/``
- `intensive_heavy`:
  - variant spec: ``config/patchworks.variant.intensive_heavy.yaml``
  - silviculture config: ``config/silviculture.k3z.intensive_heavy.yaml``
  - launch entrypoint: ``models/k3z_patchworks_model/analysis/intensive_heavy.pin``
  - tracks surface: ``models/k3z_patchworks_model/tracks_intensive_heavy/``
- Each ``tracks_intensive_*`` surface should materialize the full
  ``PCT -> CT -> F1 -> F2 -> F3`` chain.
- Each ``tracks_intensive_*`` surface should expose AU-wise harvested-stem QMD
  numerator rows for ``PCT``, ``CT``, and downstream ``CC``:
  - ``product.QMDNumerator.managed.<au_token>.PCT``
  - ``product.QMDNumerator.managed.<au_token>.CT``
  - ``product.QMDNumerator.managed.<au_token>.CC``
- Matching denominator rows:
  - ``product.Treated.managed.<au_token>.PCT``
  - ``product.Treated.managed.<au_token>.CT``
  - ``product.Treated.managed.<au_token>.CC``
- The live ``intensive_*`` Patchworks PIN files should register user-facing
  ratio accounts:
  - ``product.QMD.managed.<au_token>.PCT``
  - ``product.QMD.managed.<au_token>.CT``
  - ``product.QMD.managed.<au_token>.CC``
- Read the live ``product.QMD.*`` ratio accounts directly as mean harvested
  diameter in ``cm``.
- Read ``product.HarvestedVolume.*`` accounts as recovered merchantable volume:
  ``CC`` uses downstream utilization ``0.85`` and ``CT`` uses downstream
  utilization ``0.75``.
- The ``intensive_*`` family reuses the curated CT/fert retained-area overlay
  from ``tmp/CTFert Fragments/fragments_updated3_Usedinbasecase.shp``.
- Patchworks smoke expectation: pulling on ``F3`` treated area should induce
  ``F2`` -> ``F1`` -> ``CT`` -> ``PCT`` -> ``CC``.
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
- confirm the AU-wise harvested-stem QMD ``CC`` numerator / denominator /
  ratio-account contract still matches baseline;
- confirm the AU-wise standing stems-per-ha feature accounts still match the
  baseline contract;
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
4. Optional variant anomalies: confirm you launched the intended PIN/runtime
   pair and that the matching ``config/silviculture.k3z.ctfert*.yaml`` file
   matches the expected treatment-path build.
5. On the selected ``pct_*`` subvariant, confirm the matching
   ``config/silviculture.k3z.pct_*.yaml`` matches the expected treatment-path
   build and that the corresponding ``tracks_pct_*`` surface is active.

Release Checklist
-----------------

- Rebuild and matrix-build complete without hard errors.
- Invariant report passes baseline checks.
- Required docs pages and contract tests pass.
- Published docs navigation resolves and includes current pages.
- If releasing the optional CT/fert variant family, confirm the
  ``ctfert_l15h5`` / ``ctfert_l20h0`` subvariants have documented variant
  specs, runtime configs, curated ``RETENTION`` provenance, and launch
  instructions for student groups.
- If releasing the optional PCT-only subvariants, confirm the light/moderate/
  heavy variant specs, runtime configs, and ``pct_*.pin`` launch
  instructions are documented for student groups.
- If releasing the optional full-intensive subvariants, confirm the
  ``intensive_light`` / ``intensive_moderate`` / ``intensive_heavy`` variant
  specs, runtime configs, curated ``RETENTION`` provenance, and
  ``intensive_*.pin`` launch instructions are documented for student groups.

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
