# FreshForge K3Z Materialization Overlay

K3Z is the third acceptance case for the reusable FEMIC FreshForge
materialization provider. Unlike TFL6 and MKRF, the current K3Z teaching
snapshot is plain git rather than a DataLad/git-annex dataset.

The K3Z overlay therefore sets `annex.enabled: false`. The shared
`femic.materialization` provider still initializes the parent submodule,
validates the parent `.venv`, installs FEMIC with `dev` and `freshforge`
extras, installs this K3Z package editable, verifies required tracked paths,
and writes a materialization report. Annex initialization, special-remote
enablement, and annex availability audit nodes become deterministic no-op
success nodes that report annex is disabled by overlay configuration.

The workflow targets the parent FEMIC checkout with K3Z at
`external/femic-k3z-instance`. Standalone K3Z clone materialization and any
future DataLad/LFS migration are separate decisions outside this phase.
