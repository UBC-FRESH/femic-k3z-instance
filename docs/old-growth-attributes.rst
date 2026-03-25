Old-Growth Attributes
=====================

Purpose
-------

K3Z exports two old-growth feature surfaces for every analysis unit and for the
instance-wide total surface.

Attribute Labels
----------------

Per-AU labels:

- ``feature.Area.og1.<au_token>``
- ``feature.Area.og2.<au_token>``

Instance-wide summary labels:

- ``feature.Area.og1.total``
- ``feature.Area.og2.total``

These are feature surfaces, not treatment products.

Current Implementation Contract
-------------------------------

The exporter builds ``og1`` and ``og2`` in ``src/femic/fmg/patchworks.py``.

``og1``:

- source curve is the AU-wise unmanaged total yield curve;
- if an unmanaged total curve is missing, exporter falls back to the managed
  total curve so the surface still compiles;
- ramp start = AU-wise ``CMAI`` age from that source curve;
- ramp end = AU-wise ``peak_yield_age`` from that source curve;
- emitted curve is a two-point ramp:
  - ``(CMAI, 0.0)``
  - ``(peak_yield_age, 1.0)``

``og2``:

- emitted curve is a fixed two-point policy step:
  - ``(249, 0.0)``
  - ``(250, 1.0)``

Why OG1 Uses the Unmanaged Curve
--------------------------------

``og1`` is intentionally tied to unmanaged curve shape because it is meant to
represent old-growth timing against the passive stand-development pathway, not
against whichever treatment sequence happens to be available on the managed
side.

That design keeps ``og1`` interpretable across:

- the baseline model,
- treatment variants such as ``ctfert``, ``pct_light``,
  ``pct_moderate``, and ``pct_heavy``, and
- overlay subvariants that only alter retained area.

Where the Surfaces Appear
-------------------------

After export and Matrix Builder:

- the labels above should appear in the compiled feature/account surfaces;
- they should also be visible in live Patchworks account browsing;
- they should remain available even when treatment variants change managed
  state logic, because old-growth semantics are anchored to the source yield
  curves, not to treatment products.

Interpretation Notes
--------------------

- ``og1`` is a gradual ecological timing proxy driven by curve shape.
- ``og2`` is a hard policy threshold.
- Comparing ``og1`` and ``og2`` together is often more useful than treating
  either one as a standalone old-growth definition.
