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

Patchworks Runtime Preflight Fails
----------------------------------

Symptoms:

- ``femic patchworks preflight`` reports missing runtime prerequisites.

Actions:

1. Confirm Patchworks jar path and SPS license environment.
2. Confirm all config paths are instance-root relative and resolve correctly.
3. Retry preflight with explicit config path.
