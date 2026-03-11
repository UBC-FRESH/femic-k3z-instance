Getting Started
===============

Purpose
-------

``femic-k3z-instance`` is a runnable, versioned K3Z deployment instance for
teaching and collaboration.

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

2. Compile/rebuild inputs:

   .. code-block:: bash

      femic run --run-config config/run_profile.k3z.yaml

3. Run Patchworks matrix build:

   .. code-block:: bash

      femic patchworks matrix-build --config config/patchworks.runtime.windows.yaml --run-id k3z_manual_build

Authoritative Paths
-------------------

- Patchworks model root:
  ``models/k3z_patchworks_model/``
- Active tracks:
  ``models/k3z_patchworks_model/tracks/``
- Runtime logs/manifests:
  ``vdyp_io/logs/``
