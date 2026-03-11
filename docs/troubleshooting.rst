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

1. Confirm species-proportion source data exists in bundle tables.
2. Rebuild ForestModel XML and tracks.
3. Inspect rebuild report for invariant failures and baseline diffs.

Patchworks Runtime Preflight Fails
----------------------------------

Symptoms:

- ``femic patchworks preflight`` reports missing runtime prerequisites.

Actions:

1. Confirm Patchworks jar path and SPS license environment.
2. Confirm all config paths are instance-root relative and resolve correctly.
3. Retry preflight with explicit config path.
