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

PCT->CT Subvariant Shows Total Managed Yield But Species Accounts Are Missing
-----------------------------------------------------------------------------

This is a regression playbook, not the expected current K3Z ``pctct_*``
state. Each checked-in ``pctct_light`` / ``pctct_moderate`` /
``pctct_heavy`` surface should retain species-wise managed yield /
harvest-volume accounts alongside the ``PCT -> CT`` treatment path.

Symptoms:

- a ``pctct_*`` subvariant launches and treatment products look correct, but managed
  species-wise growing-stock / harvest-volume accounts are absent while
  ``product.Yield.managed.Total`` still exists.

Actions:

1. Confirm you are actually on the intended ``pctct_*`` surface:

   .. code-block:: bash

      femic patchworks matrix-build --config config/patchworks.runtime.pctct_light.windows.yaml --run-id k3z_pctct_light_check

2. Inspect the matching ``models/k3z_patchworks_model/tracks_pctct_*/accounts.csv``
   and ``products.csv`` files to confirm whether only total managed yield
   surfaces were compiled.
3. Inspect the matching ``models/k3z_patchworks_model/yield/forestmodel_pctct_*.xml``
   file to see whether species-wise managed yield surfaces were exported
   upstream.
4. Treat this as a regression if the treatment path is otherwise correct. Do
   not reinterpret the result as intentional ``pctct_*`` design.
5. Compare against ``base`` or ``ctfert`` to confirm the missing surface is a
   variant-specific regression, not a repo-wide account failure.

Patchworks Runtime Preflight Fails
----------------------------------

Symptoms:

- ``femic patchworks preflight`` reports missing runtime prerequisites.

Actions:

1. Confirm Patchworks jar path and SPS license environment.
2. Confirm all config paths are instance-root relative and resolve correctly.
3. Retry preflight with explicit config path.
