Model Anatomy
=============

Directory Map
-------------

- ``analysis/``: Patchworks PIN files and runtime entrypoints.
- ``blocks/``: block shapefile and topology CSV used by Patchworks joins.
- ``config/``: run profile, seral config, silviculture config, TIPSY rules,
  Patchworks runtime config.
- ``data/``: local case inputs, cached intermediates, model-input bundle tables.
- ``models/k3z_patchworks_model/``: curated Patchworks model package.
- ``output/``: validated export products from FEMIC stages.
- ``plots/``: QA and interpretation figures for strata/curves/overlays.
- ``vdyp_io/logs/``: reproducibility artifacts (manifests, matrix logs,
  reports).

Generated vs Editable
---------------------

Safe to edit directly:

- ``config/run_profile.k3z.yaml``
- ``config/seral.k3z.yaml``
- ``config/tipsy/tsak3z.yaml``
- ``config/silviculture.k3z.base.yaml`` for optional baseline harvested-QMD
  and stems-per-ha support-surface switches
- ``config/silviculture.k3z.ctfert_l15h5.yaml`` for the optional CT/fert
  ``L15/M10/H5`` subvariant
- ``config/silviculture.k3z.ctfert_l20h0.yaml`` for the optional CT/fert
  ``L20/M10/H0`` subvariant
- ``config/silviculture.k3z.pct_light.yaml`` for the optional light PCT-only subvariant
- ``config/silviculture.k3z.pct_moderate.yaml`` for the optional moderate PCT-only subvariant
- ``config/silviculture.k3z.pct_heavy.yaml`` for the optional heavy PCT-only subvariant
- ``config/silviculture.k3z.intensive_light.yaml`` for the optional full-intensive light subvariant
- ``config/silviculture.k3z.intensive_moderate.yaml`` for the optional full-intensive moderate subvariant
- ``config/silviculture.k3z.intensive_heavy.yaml`` for the optional full-intensive heavy subvariant
- fragment-level ``RETENTION`` values when/if you intentionally edit retained-area policy in the validated fragments dataset

Regenerate instead of hand-edit:

- ``data/model_input_bundle/*.csv``
- ``models/k3z_patchworks_model/tracks/*.csv``
- ``output/patchworks_k3z_validated/forestmodel.xml``
- ``output/patchworks_k3z_validated/fragments/*``

Use caution:

- ``models/k3z_patchworks_model/analysis/base.pin`` (runtime wiring)
- ``models/k3z_patchworks_model/blocks/*`` (must stay join-consistent with tracks)

Core Feature and Product Surfaces
---------------------------------

Seral account surfaces:

- Global compatibility surface: ``feature.Seral.<stage>``
- AU-specific inventory-state surface: ``feature.Seral.<au_token>.<stage>``
- Treatment consequence surface: ``product.Seral.area.<stage>.<au_token>.CC``

Old-growth surfaces:

- ``feature.Area.og1.<au_token>``
- ``feature.Area.og2.<au_token>``
- ``feature.Area.og1.total``
- ``feature.Area.og2.total``

Current old-growth curve semantics:

- ``og1``: unmanaged-curve-driven ramp from CMAI age (0.0) to unmanaged
  peak-yield age (1.0)
- ``og2``: policy-step curve with ``249 -> 0.0`` and ``250 -> 1.0``

Deep reference: :doc:`old-growth-attributes`

These are inventory-state feature surfaces, not treatment-consequence products.
They should appear automatically in compiled Patchworks accounts after Matrix
Builder regenerates ``protoaccounts.csv`` / ``accounts.csv``.

Baseline and Overlay Harvested-QMD Surface
------------------------------------------

The accepted K3Z baseline and the four baseline-derived overlay subvariants
now also carry an AU-wise harvested-stem QMD account contract for ``CC``.

Additional baseline/overlay support surfaces:

- standing-stock approximate QMD outputs:
  - ``feature.QMD.managed.<au_token>``
  - ``feature.QMD.unmanaged.<au_token>``
- standing stem-height outputs:
  - ``feature.Height.managed.<au_token>``
  - ``feature.Height.unmanaged.<au_token>``
- standing stems-per-ha outputs:
  - ``feature.StemsPerHa.managed.<au_token>``
  - ``feature.StemsPerHa.unmanaged.<au_token>``
- harvested-QMD numerator attributes:
  - ``product.QMDNumerator.managed.<au_token>.CC``
- matching denominator attributes:
  - ``product.Treated.managed.<au_token>.CC``

The shipped XML/tracks define those numerator and denominator attributes. At
launch time, ``analysis/base.pin`` and the overlay PIN family source the common
ratio-account helper so Patchworks registers live:

- ``product.QMD.managed.<au_token>.CC``

Those live ratio accounts divide the matching
``product.QMDNumerator.managed.<au_token>.CC`` account by the corresponding
``product.Treated.managed.<au_token>.CC`` account with scale ``1``, so the
live values resolve directly to mean harvested-stem diameter in ``cm``.

The standing stems-per-ha feature accounts are normalized downstream during the
``protoaccounts.csv -> accounts.csv`` promotion step, using AU-wise managed and
unmanaged area from the validated fragments surface. Read the live
``feature.StemsPerHa.*`` accounts directly as mean standing stems per hectare,
not total stem counts.

The standing stem-height feature accounts follow the same downstream
area-normalized contract. Read the live ``feature.Height.*`` accounts directly
as mean standing height in ``m`` for the matching AU and IFM side.

These baseline and overlay launch surfaces also apply a downstream recovered-
volume utilization assumption during ``protoaccounts.csv -> accounts.csv``
promotion:

- ``CC`` harvested volume uses utilization ``0.85``
- ``CT`` harvested volume uses utilization ``0.75`` on CT-enabled variants

That policy lives in the runtime config layer, not in the ForestModel XML. The
standing yield curves remain unchanged; only the promoted harvested-volume
accounts are scaled to represent recovered merchantable volume.

Retention Surface
-----------------

K3Z carries a fragment-level ``RETENTION`` field in the validated Patchworks
fragments dataset.

- ``0.0`` means no retained area is withdrawn from the managed landbase.
- ``1.0`` means the full fragment area is retained.
- intermediate values mean partial retained area.

Current K3Z baseline:

- the teaching baseline on ``main`` uses ``RETENTION = 0.05`` for all fragments
- retained area is therefore withdrawn from the managed landbase and compiled
  into unmanaged area/tracks/accounts in Patchworks

Do not hand-edit retention in multiple places. If you change retention policy,
update the validated fragments dataset and rerun Matrix Builder so the retained
share flows into Patchworks unmanaged area consistently.

Optional CT/Fert Variant Surface
--------------------------------

The optional CT/fert variant adds a second layer
of model anatomy that is intentionally not part of the baseline K3Z teaching
instance on ``main``.

Additional state/config artifacts for that variant:

- fragment/XML state field: ``SILV_STATE``
- silviculture configs for the shipped CT/fert SI-profile subvariants:
  - ``config/silviculture.k3z.ctfert_l15h5.yaml``
  - ``config/silviculture.k3z.ctfert_l20h0.yaml``
- approximate QMD outputs:
  - ``feature.QMD.managed.<au_token>``
  - ``feature.QMD.unmanaged.<au_token>``
- standing stem-height outputs:
  - ``feature.Height.managed.<au_token>``
  - ``feature.Height.unmanaged.<au_token>``
- standing stems-per-ha outputs:
  - ``feature.StemsPerHa.managed.<au_token>``
  - ``feature.StemsPerHa.unmanaged.<au_token>``
  - harvested-QMD numerator attributes:
  - ``product.QMDNumerator.managed.<au_token>.CC``
  - ``product.QMDNumerator.managed.<au_token>.CT`` on the CT-eligible AU cohort
- treatment-path states:
  - ``baseline``
  - ``cc_pl``
  - ``cc_pl_ct``
  - ``cc_pl_ct_f1``
  - ``cc_pl_ct_f1_f2``
  - ``cc_pl_ct_f1_f2_f3``

Optional treatment surfaces for that variant:

- ``CT`` commercial thinning on the configured eligible AU cohort
- ``F1`` / ``F2`` / ``F3`` fertilization chain after CT
- matching compiled treatment products/accounts such as:
  - ``product.Treated.managed.CT``
  - ``product.Treated.managed.F1``
  - ``product.Treated.managed.F2``
  - ``product.Treated.managed.F3``
  - ``product.Treated.managed.<au_token>.CC``
  - ``product.Treated.managed.<au_token>.CT``

The shipped XML/tracks define AU-wise harvested-QMD numerator attributes plus
the matching treated-area denominator attributes. At launch time, the CT/fert
PIN files register live Patchworks ratio accounts:

- ``product.QMD.managed.<au_token>.CC``
- ``product.QMD.managed.<au_token>.CT``

Those runtime ratio accounts divide the matching
``product.QMDNumerator.managed.<au_token>.<treatment>`` account by the
corresponding ``product.Treated.managed.<au_token>.<treatment>`` account with
scale ``1``, so the live values resolve directly to mean harvested-stem
diameter in ``cm``.

The standing stems-per-ha surfaces follow the same teaching-model pattern as
standing QMD:

- managed baseline/planted support uses the accepted TIPSY ``TPH`` handoff
  where available;
- unmanaged support uses the checkpoint-derived AU median
  ``STEMS_PER_HA_75`` value;
- post-CT states scale the standing stems surface by the configured CT removal
  fraction from the CT age forward;
- fertilization states carry the same standing stems surface forward unchanged.

The standing ``feature.Height.*`` accounts are exposed on the same AU-wise
managed/unmanaged contract. Read them directly as mean standing height in
``m``.

The shipped CT/fert launch surfaces also apply the downstream recovered-volume
utilization policy during ``protoaccounts.csv -> accounts.csv`` promotion:

- ``CC`` harvested volume uses utilization ``0.85``
- ``CT`` harvested volume uses utilization ``0.75``

That policy does not alter standing yield curves or the ForestModel XML. It
only scales the promoted harvested-volume accounts so teaching runs reflect
recovered merchantable volume rather than perfect recovery.

The SI-profiled CT/fert subvariants extend that same state machine across the
six ``L/M/H`` SI-class ``CWHvm_FDC+HW`` / ``CWHvm_CW+HW`` AUs, but change the
fert response by SI class:

- ``ctfert_l15h5``: ``L=15%``, ``M=10%``, ``H=5%``
- ``ctfert_l20h0``: ``L=20%``, ``M=10%``, and no fert on ``H`` AUs

In this variant, ``ORIGIN`` still means natural vs planted. Treatment history is
carried by ``SILV_STATE`` instead of overloading ``ORIGIN``.


Optional PCT-Only Subvariant Family Surface
-------------------------------------------

The optional ``pct_light``, ``pct_moderate``, and ``pct_heavy``
subvariants add three coexisting upstream-distinct surfaces that keep the
baseline and CT/fert variants intact while inserting a pre-commercial-thinning
gate on the planted path.

Additional state/config artifacts for that variant:

- fragment/XML state field: ``SILV_STATE``
- silviculture configs:
  - ``config/silviculture.k3z.pct_light.yaml``
  - ``config/silviculture.k3z.pct_moderate.yaml``
  - ``config/silviculture.k3z.pct_heavy.yaml``
- treatment-path states:
  - ``baseline``
  - ``cc_pl``
  - ``cc_pl_pct``
- approximate QMD outputs:
  - ``feature.QMD.managed.<au_token>``
  - ``feature.QMD.unmanaged.<au_token>``
- standing stem-height outputs:
  - ``feature.Height.managed.<au_token>``
  - ``feature.Height.unmanaged.<au_token>``
- standing stems-per-ha outputs:
  - ``feature.StemsPerHa.managed.<au_token>``
  - ``feature.StemsPerHa.unmanaged.<au_token>``

Optional treatment surfaces for that variant:

- ``PCT`` eligibility retargeted to medium/high SI ``HW+FDC`` and
  ``FDC+HW`` AUs ``985502000``, ``985503000``, ``985502001``, and
  ``985503001``
- three subvariant-specific age-10 PCT choices on the planted path:
  - ``pct_light`` -> remove ``1000`` HW stems/ha
  - ``pct_moderate`` -> remove ``2000`` HW stems/ha
  - ``pct_heavy`` -> remove ``3000`` HW stems/ha
- planted regen mix for those eligible AUs prepared as ``900 CW + 3100 HW``
- post-PCT managed mixtures of ``900 CW + 2100 HW``, ``900 CW + 1100 HW``, and
  ``900 CW + 100 HW`` respectively
- matching compiled treatment products/accounts such as:
  - ``product.Treated.managed.PCT``
  - ``product.Treated.managed.<au_token>.PCT``
  - ``product.Treated.managed.<au_token>.CC``
  - ``product.QMDNumerator.managed.<au_token>.PCT``
  - ``product.QMDNumerator.managed.<au_token>.CC``

The shipped XML/tracks define AU-wise harvested-QMD numerator attributes for
both ``PCT`` and the downstream planted-path ``CC`` treatment, plus the
matching AU-wise treated-area denominator attributes. At launch time, the
``pct_*`` PIN files register live Patchworks ratio accounts:

- ``product.QMD.managed.<au_token>.PCT``
- ``product.QMD.managed.<au_token>.CC``

Those runtime ratio accounts divide the matching
``product.QMDNumerator.managed.<au_token>.<treatment>`` account by the
corresponding ``product.Treated.managed.<au_token>.<treatment>`` account with
scale ``1``, so the live values resolve directly to mean harvested-stem
diameter in ``cm``.

The standing stems-per-ha surfaces on the ``pct_*`` family use the accepted
managed/unmanaged support inputs, then scale the planted-path standing stems
surface from age 10 onward by the configured PCT residual fraction. In other
words, the light/moderate/heavy subvariants now expose standing-density
surfaces that are distinct, not just different product/yield paths.

The standing ``feature.Height.*`` accounts are available alongside
``feature.StemsPerHa.*`` and ``feature.QMD.*``, so the ``pct_*`` family now
exposes standing height, standing density, and harvested-diameter views in
parallel.

The shipped ``pct_*`` launch surfaces inherit the same downstream recovered-
volume utilization policy during ``protoaccounts.csv -> accounts.csv``
promotion:

- ``CC`` harvested volume uses utilization ``0.85``
- ``CT`` would use utilization ``0.75`` if present, but the shipped
  ``pct_*`` family does not expose ``CT``

This variant is intended as a teaching scaffold for PCT intensity comparison
without the added complexity of CT or fertilization.

Optional Full-Intensive Subvariant Family Surface
-------------------------------------------------

The optional ``intensive_light``, ``intensive_moderate``, and
``intensive_heavy`` subvariants add a coexisting teaching family that combines
the current PCT-only and CT/fert scaffolds on one planted-path surface.

Additional state/config artifacts for that variant:

- fragment/XML state field: ``SILV_STATE``
- silviculture configs:
  - ``config/silviculture.k3z.intensive_light.yaml``
  - ``config/silviculture.k3z.intensive_moderate.yaml``
  - ``config/silviculture.k3z.intensive_heavy.yaml``
- treatment-path states:
  - ``baseline``
  - ``cc_pl``
  - ``cc_pl_pct``
  - ``cc_pl_pct_ct``
  - ``cc_pl_ct_f1``
  - ``cc_pl_ct_f1_f2``
  - ``cc_pl_ct_f1_f2_f3``
- approximate QMD outputs:
  - ``feature.QMD.managed.<au_token>``
  - ``feature.QMD.unmanaged.<au_token>``
- standing stem-height outputs:
  - ``feature.Height.managed.<au_token>``
  - ``feature.Height.unmanaged.<au_token>``
- standing stems-per-ha outputs:
  - ``feature.StemsPerHa.managed.<au_token>``
  - ``feature.StemsPerHa.unmanaged.<au_token>``

Optional treatment surfaces for that variant:

- ``PCT`` on the full 8-AU union of the current ``pct_*`` and
  ``ctfert_l15h5`` families
- ``CT`` after ``PCT`` on that same 8-AU cohort
- ``F1`` / ``F2`` / ``F3`` after ``CT`` using the accepted
  ``ctfert_l15h5`` response profile
- matching compiled treatment products/accounts such as:
  - ``product.Treated.managed.PCT``
  - ``product.Treated.managed.CT``
  - ``product.Treated.managed.F1``
  - ``product.Treated.managed.F2``
  - ``product.Treated.managed.F3``
  - ``product.Treated.managed.<au_token>.PCT``
  - ``product.Treated.managed.<au_token>.CT``
  - ``product.Treated.managed.<au_token>.CC``
  - ``product.QMDNumerator.managed.<au_token>.PCT``
  - ``product.QMDNumerator.managed.<au_token>.CT``
  - ``product.QMDNumerator.managed.<au_token>.CC``

The shipped XML/tracks define AU-wise harvested-QMD numerator attributes for
``PCT``, ``CT``, and downstream ``CC``, plus the matching AU-wise treated-area
denominator attributes. At launch time, the ``intensive_*`` PIN files register
live Patchworks ratio accounts:

- ``product.QMD.managed.<au_token>.PCT``
- ``product.QMD.managed.<au_token>.CT``
- ``product.QMD.managed.<au_token>.CC``

Those runtime ratio accounts divide the matching
``product.QMDNumerator.managed.<au_token>.<treatment>`` account by the
corresponding ``product.Treated.managed.<au_token>.<treatment>`` account with
scale ``1``, so the live values resolve directly to mean harvested-stem
diameter in ``cm``.

The standing stems-per-ha surfaces on the ``intensive_*`` family follow the
same teaching-model pattern as the current CT/fert and PCT families:

- managed baseline/planted support uses the accepted TIPSY ``TPH`` handoff
  where available;
- unmanaged support uses the checkpoint-derived AU median
  ``STEMS_PER_HA_75`` value;
- post-PCT states scale the planted-path standing stems surface by the
  configured residual-stems fraction from age 10 onward;
- post-CT states scale that standing stems surface again by the configured CT
  removal fraction from age 40 onward;
- fertilization states carry the same standing stems surface forward unchanged.

The standing ``feature.Height.*`` accounts are available on the same AU-wise
contract as ``feature.StemsPerHa.*`` and ``feature.QMD.*``, so the full
intensive family now exposes standing height, standing density, and harvested
diameter views together.

The shipped ``intensive_*`` launch surfaces inherit the same downstream
recovered-volume utilization policy during ``protoaccounts.csv -> accounts.csv``
promotion:

- ``CC`` harvested volume uses utilization ``0.85``
- ``CT`` harvested volume uses utilization ``0.75``

This variant is intended as a teaching scaffold for combined treatment-path
comparison, not as a polished operational prescription package.

Deep references
---------------

- full launch matrix: :doc:`variants-and-subvariants`
- treatment/state-machine details: :doc:`silviculture-logic`
- student-facing treated curve gallery: :doc:`yield-curve-comparisons`
- old-growth attribute logic: :doc:`old-growth-attributes`
