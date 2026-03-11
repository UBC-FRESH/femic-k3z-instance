Rebuild and QA
==============

Deterministic Rebuild Script
----------------------------

Use FEMIC repository helper script for reproducible K3Z rebuild checks:

.. code-block:: bash

   python scripts/k3z/rebuild_k3z_instance.py --run-id k3z_rebuild_check

Outputs
-------

- Rebuild report:
  ``vdyp_io/logs/k3z_rebuild_report-<run_id>.json``
- Matrix logs:
  ``vdyp_io/logs/patchworks_matrixbuilder_{stdout,stderr,manifest}-<run_id>.log``

Key Invariants
--------------

- Managed area should remain near expected baseline.
- Block joins must remain 1:1 between ``tracks/blocks.csv`` and ``blocks/blocks.shp``.
- Seral accounts must exist in ``tracks/accounts.csv``.
- Required managed species yields must remain non-zero (except explicitly allowed species).

Baseline Workflow
-----------------

Initialize baseline (once per accepted model state):

.. code-block:: bash

   python scripts/k3z/rebuild_k3z_instance.py --run-id k3z_baseline --write-baseline

Validate against baseline:

.. code-block:: bash

   python scripts/k3z/rebuild_k3z_instance.py --run-id k3z_compare
