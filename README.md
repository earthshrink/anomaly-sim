# Reproduction of the flyby anomaly residuals

<!-- {{{ -->

This repository presents code and Jupyter notebooks that reproduce for the first time a key signature,
_oscillating Doppler residuals_,
seen alongside anomalous velocity gains ΔV  in NEAR's 1998 flyby of Earth [[1](Ref.md#1), [3](Ref.md#3)],
and in Rosetta's in 2005 [[2](Ref.md#2)].
The code uses the [astropy](https://www.astropy.org) and [poliastro](https://www.poliastro.space) python libraries
for orbit propagation,
and [lmfit](https://github.com/lmfit/lmfit-py)
for discovering least square fit trajectories that reproduce the pattern of residuals.

More particularly,
__light-time lags__ had been anticipated in the two-way Doppler and range data
from [a deeper mathematical theory revisiting the wave equation](Theory.md),
shown implied by the SSN radar range residuals in [[5](Ref.md#5)],
and subsequently in [[6](Ref.md#6)],
to closely explain _all aspects_ of the anomalies, including the anomalous velocity gains ΔV to 1%,
using range and range rate data directly from [JPL Horizons](https://ssd.jpl.nasa.gov).
Copies of the residual graphs from JPL, the Horizons queries and the graph computation and overlay scripts
are given and documented in [Github: flyby-analysis](https://github.com/earthshrink/flyby-analysis).
See also the [brief summary](Summary.md) on the anomaly and prior work. 

As briefly explained [separately](Theory.md), the light-time lags expose
a fundamental issue of Doppler under acceleration that was hitherto untreated and renders
the very formalism of relativistic space-time fundamentally incomplete for coherent observations,
and imply that
_modulated range codes were delivered at __speeds exceeding that of light for days___.
These aspects,
if not the promise of rendering current communication and radar technologies obsolete,
make it imperative to verify that
the light-time lags are real and the only explanation possible for the anomalies,
independently now recognized as __already over 100σ__ [[4](Ref.md#4)].

<!-- }}} -->

## Method and scope

[Poliastro](https://www.poliastro.space) defines
an `Orbit` class that encapsulates orbital elements and a method for constructing `Orbit` objects
with reference to a "single attractor"
from position and velocity vector coordinates at a given instant in an inertial frame.
It also defines
an `Ephem` class that encapsulates an ordered sequence of coordinates and corresponding epochs,
and methods to interpolate the coordinates to epochs in-between,
and can thus represent a segment of trajectory.
A `from_horizons` constructor allows obtaining a trajectory from [JPL Horizons](https://ssd.jpl.nasa.gov).
Version 0.17 added a `to_ephem` method to the Orbit class to compute
the trajectory at arbitrary epochs using any of several proven orbit computation algorithms.

Added here are
- a `Station` class to encapsulate tracking station coordinates and methods to compute topocentric (station-relative)
  range, range rate and radial acceleration given the spacecraft position and velocity vectors at a given epoch; and
- an `OrbitFitter` class that encapsulates [lmfit](https://github.com/lmfit/lmfit-py) with methods to compute a best fit
  trajectory (`Ephem`) in the neighbourhood of an initial `Orbit` over the orbital elements parameter space, given
  simulated range or range rate (Doppler) data.

Precession and nutation of the attractor (Earth), 
gravitational influences of other bodies including the Sun,
space-time curvature and cumulative effects of the solar wind, etc.
are not modelled.
An effort to model these would be not only prohibitive in time and effort,
but would at most serve to merely confirm
the 1% fit to NEAR's ΔV and zero-noise fit to the SSN residuals
already obtained with [JPL Horizons](https://ssd.jpl.nasa.gov) data
in [[6](Ref.md#6)].
Specialist expertise would be required that would also defeat
transparency and verifiability of any further improvement or additional result.

This work was therefore meant to explore
- if NASA and ESA orbit determinations (OD) for the flybys could be reproduced more simply without specialist skills;
- whether the Doppler/range rate residual oscillations also seen could be reproduced and experimented with;
- and if so, _whether these residual oscillations also imply the light-time lags or allow other explanations_.

In all cases,
an initial set of position and velocity vectors is obtained using `Ephem.from_horizons`
from the actual flyby and the official NASA/ESA trajectory,
and used to compute a reference set of orbital elements.
Range or range rate data are simulated over a trajectory derived from these reference orbital elements
for a sample set of pre- or post-encounter epochs.
Least square fit is applied to this simulated data to obtain new orbital elements and trajectory,
and the final set of residuals computed during the fit are compared to
those described in [[1](Ref.md#1), [2](Ref.md#2)].


## Results

The main result obtained is that
__the light-time lags are the necessary and sufficient explanation for the Doppler/range-rate residuals__ and thereby
for the anomalies as a whole,
as follows:

- The post-encounter residuals are found very closely reproduced by the least square fit to range rate data simulated
  with the light-time lags against the Horizons-based reference trajectory for both NEAR, in
  [near_sim_postencounter_doppler.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_postencounter_doppler.ipynb)
  and for Rosetta in
  [rosetta_sim_postencounter_rangerate.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/rosetta/rosetta_sim_postencounter_rangerate.ipynb).

  This establishes sufficiency of the light-time lags in the tracking signal.
  <p>

- Replacing the light-time lags with a constant lag is found to also produce oscillation, but with a slope proportional
  to the constant, in
  [near_sim_postencounter_constlag.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_postencounter_constlag.ipynb).
  Keeping the lags proportional to light-time but changed by a constant scale factor results in the oscillations also
  changing by the same scale factor, as found in
  [near_sim_postencounter_scaledlag.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_postencounter_scaledlag.ipynb).

  This proves necessity of exactly light-time lags as the only possible change in the transponded tracking signal that could
  lead to the precise form and magnitude of the residuals.
  It also proves necessity of signal change in the first place, as the oscillations trivially vanish with zero scale
  factor.

In particular, any hypothesis of an external force responsible for the ΔV, including dark matter or relativistic
frame-dragging [[8](Ref.md#8)] or from the Casimir effect [[4](Ref.md#4)], would be incapable of reproducing the
residual oscillations, whereas the light-time lags also explain the ΔV to 1% as mentioned.

Following notebooks were developed _en route_  to this conclusion and provide additional details and insight.

<!-- {{{ table -->
| __Notebook__                                       | __Result shown__                                                                          |
|:--|:--|
| [near_gapcheck.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_gapcheck.ipynb)                           | Establishes that orbit propagation is too inaccurate to test JPL or ESA OD. Horizons can be used only for initial position and velocity for a reference trajectory, and the tests must be limited to reproducing the published residuals. |
|                                                    |                                                                                           |
| [near_sim_ssn_residuals.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_residuals.ipynb)                  | Shows that lags _added to_ the LOS-based trajectory accurately predict the SSN residuals. _But_ inserting a lag at LOS does not, making it a mystery how the SSN residuals could be proportional to range against a trajectory extrapolated from LOS without reference to the SSN radars. |
|                                                    |                                                                                           |
| [near_ssntrack.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_ssntrack.ipynb)                           | Cesium 3d visualization of the SSN locations and trajectory. This suggested that the SSN residuals could result from a small vertical displacement of the trajectory assuring proportionality to range as a 'similar triangles' property. |
|                                                    |                                                                                           |
| [near_sim_ssn_fitlosrange_trajectory.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_fitlosrange_trajectory.ipynb)     | Validated least square fit from simulated range data with lags in the LOS-based reference trajectory as a means to find a similar trajectory. Very similar values are obtained for the SSN residuals. |
|                                                    |                                                                                           |
| [near_sim_ssn_fitlosdoppler_trajectory.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_fitlosdoppler_trajectory.ipynb)   | Validated least square fit from simulated Doppler data with lags also as a means to find a similar trajectory. The values predicted for the SSN residuals are much different, however. |
|                                                    |                                                                                           |
| [near_sim_ssn_revfit_altair.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_revfit_altair.ipynb)              | Fit to simulated range data lags for Altair. Residuals diverge up to 5 km and 0.5 m/s.    |
|                                                    |                                                                                           |
| [near_sim_ssn_revfit_millstone.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_revfit_millstone.ipynb)           | Fit to simulated range data lags for Millstone. Residuals diverge up to 5 km and 0.5 m/s.  |
|                                                    |                                                                                           |
| [near_sim_ssn_revfit_range.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_revfit_range.ipynb)               | Fit to combined range data with lags simulated for the SSNs and Goldstone. The divergence is down to 150 m, finally assuring that (lag induced) error in pre-LOS trajectory sufficed to cause the SSN residuals. |
|                                                    |                                                                                           |
| [near_sim_ssn_revfit_doppler.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/near/near_sim_ssn_revfit_doppler.ipynb)             | Fit to combined Doppler data with lags simulated for the SSNs and Goldstone. The range variation is still only 200 m and almost linear. The Doppler variation is down to 50 mm/s. This exceeds the anomaly, but this is without modelling precession, solar wind, etc. |
|                                                    |                                                                                           |
| [rosetta_sim_approach_rangerate.ipynb](https://nbviewer.org/github/earthshrink/anomaly-sim/blob/master/rosetta/rosetta_sim_approach_rangerate.ipynb)       | Verifies that fit in reverse to simulated range rate with lags from a post-perigee state reproduces the range rate oscillations before and after perigee. |
<!-- }}} -->

