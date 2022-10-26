# Reproduction of the Earth flyby anomalies by orbit simulation

This repository presents code and Jupyter notebooks that successfully reproduce the Earth flyby anomalies 
described in NEAR's 1998 flyby in [1, 3],
using the [astropy](https://www.astropy.org) and [poliastro](https://www.poliastro.space) python libraries
for orbit propagation.


## Background and significance

The fact that the same anomalies were being obtained
regardless of whether the trajectory was inferred from the range data or from the Doppler data in the coherent two-way tracking
not only of Galileo and NEAR but also of Rosetta in its 2005 flyby [2],
had prompted a hypothesis of anomalous velocity (and energy) gain _ΔV_.
There have been numerous speculations as to its cause, including notably
dark matter surrounding satellite orbits
[4]
and
gravito-magnetic frame dragging
[9].

However,
_dynamical_ causes are inherently untenable as
_all_ of the anomalies occurred at altitudes far below the hundreds of GNSS and geostationary satellites.
NEAR's closest approach of 538 km is about the altitude of the Hubble Space Telescope,
and the gap in its tracking, across which the anomaly was detected,
began at an altitude below 32,000 km.
Any unanticipated dynamical effect manifesting in the single pass of a flyby
should have been replicated in every orbit of every satellite at and above the range of
the gaps in the flyby tracking across which the anomalies had been detected,
as pointed out in [10].

More particularly,
rather large and remarkably linear discrepancies against the US Space Surveillance Network (SSN) radars
had been noted for NEAR in [1].
They were subsequently confirmed also for Galileo
but had been overlooked in JPL's own investigation ([8]).
They were shown in [5]
to almost exactly correspond to __light-time lags__ in the Doppler tracking data
and to also explain the ΔV to within 20%.
A subsequent independent check using JPL Horizons that had just become available
[6]
ended up finding the same correlation and into a pre-relativity aether-theoretic hypothesis
[7].
That the correlation in fact holds to within the individual radar accuracies,
explains NEAR's _and Rosetta_'s anomalies to 1% and 3%, respectively,
and accounts for numerous detailed features of the residuals given in
[1, 2, 3]
has been rigorously shown directly from JPL Horizons range and range rate data
[8].

Shown in [11] is that the light-time lags are in fact
mathematically dictated for coherent reception under acceleration,
which has eluded rigorous treatment in Doppler and relativity theories.
This makes it imperative to rigorously verify that
the anomalies were not somehow coincidental, and more so, that
the SSN residuals most directly indicative of the light-time lags do not imply
a peculiar, one-time (or two-time, considering Galileo) error by the SSN radars.



## Investigation and results

Accordingly, two results were sought beyond the close fit to ΔV in [8], 
and are shown using Jupyter notebooks:

- The SSN residuals can be explained by an actual trajectory and tracking signal lags to within the accuracy of orbit
  propagation, so there is indeed no basis to attribute them to radar error.

- The main signature, a large diurnal oscillation in the post-encounter Doppler residual sustained for days, is almost
  exactly reproduced, which had not been possible from Horizons data alone in [8].

The notebooks present the investigation as follows.
__The last two notebooks represent the above results__.


| __Notebook__	| __Result obtained__ |
| :-- | :-- |
| [near_gapcheck.ipynb](near/near_gapcheck.ipynb)	|	Establishes that orbit propagation is too inaccurate to test JPL or ESA OD. Horizons can be used only for conditions at one epoch to generate reference orbital elements. |
| [near_sim_ssn_residuals.ipynb](near/near_sim_ssn_residuals.ipynb)	|	Verifies that lags on the LOS-based trajectory fit the SSN residuals accurately. __But__ the lags diverge at LOS. |
| [near_ssntrack.ipynb](near/near_ssntrack.ipynb)	|	3d visualization of SSN locations and trajectory, which suggested a dynamically-valid adjacent trajectory might fit the anomalies. |
| [near_sim_range_residuals.ipynb](near/near_sim_range_residuals.ipynb)	|	Test of least square fit of orbital elements on range data. |
| [near_sim_doppler_residuals.ipynb](near/near_sim_doppler_residuals.ipynb)	|	Test of least square fit of orbital elements on Doppler data. |
| [near_sim_ssn_fitlosrange_trajectory.ipynb](near/near_sim_ssn_fitlosrange_trajectory.ipynb)	|	Showed that least square fit of orbital elements to the LOS-based range data leads to slight change in SSN residuals. |
| [near_sim_ssn_fitlosdoppler_trajectory.ipynb](near/near_sim_ssn_fitlosdoppler_trajectory.ipynb)	|	Showed that least square fit of orbital elements to the LOS-based Doppler data leads to substantial change in SSN residuals. |
| [near_sim_ssn_revfit_altair.ipynb](near/near_sim_ssn_revfit_altair.ipynb)	|	Fit to range data with lags computed from the Horizons LOS state for Altair. Residuals diverge up to 5 km and 0.5 m/s. |
| [near_sim_ssn_revfit_millstone.ipynb](near/near_sim_ssn_revfit_millstone.ipynb)	|	Fit to range data with lags computed from the Horizons LOS state for Millstone. Residuals diverge up to 5 km and 0.5 m/s. |
| [near_sim_ssn_revfit_range.ipynb](near/near_sim_ssn_revfit_range.ipynb)	|	Fit to range data with lags computed using Horizons LOS for the SSNs and Goldstone together. Range divergence down to 150 m, and no longer linear. Doppler varies to 0.6 m/s. |
| [near_sim_ssn_revfit_doppler.ipynb](near/near_sim_ssn_revfit_doppler.ipynb)	|	Fit to Doppler data with lags computed from Horizons LOS for the SSNs and Goldstone together. Range variation 200 m almost linear. Doppler variation is down to 50 mm/s. This exceeds the anomaly but to be expected given the simplistic orbit propagation used. |
| [near_sim_postencounter_doppler.ipynb](near/near_sim_postencounter_doppler.ipynb)	|	Verifies that fit LOS and AOS Horizons states in fact reproduces the 1 mm/s = 50 mHz Doppler oscillations. |


## Update (2022-10-26)

A fit to Rosetta's 2005 post-encounter range rate residual oscillations described in [2] (Figure 6) [emerged](rosetta/rosetta_sim_postencounter_rangerate.ipynb) with almost no effort. 

## [References](#references)
(_in chronological order_)

[1] P G Antreasian and J R Guinn,
_Investigations into the unexpected Delta-V increases during the earth gravity assists of Galileo and NEAR_,
AIAA, 98-4287 (1998) 

[2]
T Morley and F Budnik, _Rosetta Navigation at its First Earth-Swingby_, 19th Intl Symp Space Flight Dynamics, ISTS 2006-d-52 (2006)

[3] J D Anderson, J K Campbell, J E Ekelund, J Ellis and J F Jordan,
_Anomalous Orbital-Energy Changes Observed during Spacecraft Flybys of Earth_,
PRL, 100, 9, 091102 (2008);
J D Anderson and M M Nieto,
_Astrometric Solar-System Anomalies_,
Proc IAU Symp No. 261 (2009)
[arXiv:0907.2469v2](https://arXiv.org/abs/0907.2469)

[4]
S L Adler,
_Can the flyby anomaly be attributed to Earth-bound dark matter?_,
Phys Rev D, 79, 2, 023505, 10,
[arXiv:0805.2895](https://arxiv.org/abs/0805.2895) (2009)

[5] V Guruprasad,
_Observational evidence for travelling wave modes bearing distance proportional shifts_,
[arXiv:1507.08222](https://arXiv.org/abs/1507.08222),
EPL, 110, 5,
[54001](http://stacks.iop.org/0295-5075/110/i=5/a=54001)
(2015) 

[6]
J D Giorgini,
_Status of the JPL Horizons Ephemeris System_,
IAU General Assembly (2015)

[7]
L Bilbao,
_Does the velocity of light depend on the source movement?_,
Prog in Phys (12) 307-312
[arXiv:1606.03921](https://arXiv.org/abs/1606.03921)
(2016)

[8] V Guruprasad,
_Conclusive analysis and cause of the flyby anomaly_,
Presented at [IEEE NAECON
2019](https://attend.ieee.org/naecon-2019/wp-content/uploads/sites/29/2019/08/Guruprasad-483-Radar-2.pdf).
([Proceedings preprint](https://doi.org/10.36227/techrxiv.10252871)).
For the Horizons query and graphs generating code,
see [github:earthshrink/flyby-analysis](https://github.com/earthshrink/flyby-analysis).

[9]
B M Mirza,
_The Flyby Anomaly and the Gravitational-Magnetic Field Induced Frame-Dragging Effect around the Earth_,
MNRAS, 489, 3, 3232-3235, [arXiv:1909.08083](https://arXiv.org/abs/1909.08083) (2019) 

[10]
V Guruprasad, _Comment on "The Flyby Anomaly and the Gravitational-Magnetic Field Induced Frame-Dragging Effect around
the Earth"_,
[arXiv:1911.05453](https://arxiv.org/abs/1911.05453) (2019)

[11]
V Guruprasad,
_Parametric separation of variables and the complete propagation law_,
[progress report](https://doi.org/10.36227/techrxiv.196204771) (2022)

---

