Troubleshooting
===============

Patchworks Launches But Reports Block Join Errors
-------------------------------------------------

Symptoms:

- ``blocks.csv input file contains ... blocks that do not have corresponding polygons``

Actions:

1. Rebuild blocks with current fragments input.
2. Re-run matrix builder.
3. Confirm block-id key consistency in both ``tracks/blocks.csv`` and ``blocks/blocks.shp``.

Species Accounts Missing or Zero
--------------------------------

Symptoms:

- Managed species accounts are unexpectedly absent or all zero.

Actions:

1. Run account-surface diagnostics and capture JSON evidence:

   .. code-block:: bash

      python -m femic instance account-surface \
        --config config/patchworks.runtime.windows.yaml \
        --output vdyp_io/logs/account_surface-<run_id>.json \
        --instance-root .

2. If diagnostics reports ``total OK, species-wise empty``:

   - Inspect ``tracks/products.csv`` + ``tracks/curves.csv`` for nonzero
     species label signal.
   - Inspect matrix manifest ``accounts_sync.excluded_patterns`` for accidental
     over-filtering.
   - Inspect `data/model_input_bundle/curve_table.csv` for missing
     ``treated_species_prop_*`` / ``untreated_species_prop_*`` rows; if they
     are absent, confirm the active post-TIPSY species-universe loader can see
     the shipped checkpoint artifact (for K3Z this is now
     ``data/ria_vri_vclr1p_checkpoint1-tsak3z.feather`` rather than only the
     old generic ``checkpoint8`` path).
   - If ``01a`` prep checkpoints are missing but ``au_table.csv`` persists,
     confirm the post-TIPSY fallback rebuilt unmanaged species proportions from
     ``data/vdyp_lyr-tsak3z.feather`` rather than dropping them to empty maps.
     The repaired fallback is what restores companion ctfert species such as
     ``DR``, ``BA``, and ``SS`` in the shipped K3Z teaching surfaces.
3. Re-run deterministic rebuild with Patchworks enabled:

   .. code-block:: bash

      python -m femic instance rebuild \
        --spec config/rebuild.spec.yaml \
        --with-patchworks \
        --instance-root .

4. Confirm species policy invariants pass in rebuild report:
   ``required_present``, ``expected_absent``, ``required_nonzero``,
   ``expected_zero``.
5. If needed, compare report baseline diff output before changing allowlist.

PCT-Only Subvariant Shows Total Managed Yield But Species Accounts Are Missing
------------------------------------------------------------------------------

This is a regression playbook, not the expected current K3Z ``pct_*``
state. Each checked-in ``pct_light`` / ``pct_moderate`` /
``pct_heavy`` surface should retain species-wise managed yield /
harvest-volume accounts alongside the ``PCT`` treatment path.

Symptoms:

- a ``pct_*`` subvariant launches and treatment products look correct, but managed
  species-wise growing-stock / harvest-volume accounts are absent while
  ``product.Yield.managed.Total`` still exists.

Actions:

1. Confirm you are actually on the intended ``pct_*`` surface:

   .. code-block:: bash

      femic patchworks matrix-build --config config/patchworks.runtime.pct_light.windows.yaml --run-id k3z_pct_light_check

2. Inspect the matching ``models/k3z_patchworks_model/tracks_pct_*/accounts.csv``
   and ``products.csv`` files to confirm whether only total managed yield
   surfaces were compiled.
3. Inspect the matching ``output/patchworks_k3z_pct_*/forestmodel.xml``
   file to see whether species-wise managed yield surfaces were exported
   upstream.
4. Treat this as a regression if the treatment path is otherwise correct. Do
   not reinterpret the result as intentional ``pct_*`` design.
5. Compare against ``base``, ``ctfert_l15h5``, or ``ctfert_l20h0`` to confirm
   the missing surface is a
   variant-specific regression, not a repo-wide account failure.

Patchworks Runtime Preflight Fails
----------------------------------

Symptoms:

- ``femic patchworks preflight`` reports missing runtime prerequisites.

Actions:

1. Confirm Patchworks jar path and SPS license environment.
2. Confirm all config paths are instance-root relative and resolve correctly.
3. Retry preflight with explicit config path.
