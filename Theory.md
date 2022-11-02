# Expanding solutions of the wave equation

## Mathematical basis

D'Alembert solutions, i.e., solutions to the wave equation,
of the form exp(iω<sub>0</sub>e<sup>β[t±r/c]</sup>/β), where β ≡ ω<sup>-1</sup>dω/dt,
that expand or contract with travelled distance and correspondingly change in frequencies and wavelengths with travel
as ω(r,t)=ω<sub>0</sub>e<sup>β[t±r/c]</sup>,
thereby constitute _chirp propagation modes_,
were first described in [[5](Ref.md#5)],
along with spectrometer and receiver modifications necessary for observing them.
Observational support was identified in the radar range residuals reported for Galileo and NEAR in [[1](Ref.md#1)]
for their reality and realizability at communication range,
as opposed to astronomical scales from which their possibility had been inferred
in anticipation of the acceleration of cosmological expansion, as explained in the PCT filing [[5](Ref.md#5)].
These expanding and contracting solutions 

- are equivalent to the sinusoidal solutions over a domain contracting or expanding at the specific rate β, respectively,
- represent the Fourier spectrum as seen under an acceleration a ≡ -β.cγ due to the changing Doppler, and
- form a _continuum_ of spectra _isomorphic yet orthogonal_ over the same domain to the Fourier spectrum, to which they
  reduce in the limit β=0.

Shown in [[10](Ref.md#10)] is that these solutions had been obfuscated by
a traditional assumption in introductory calculus that
the time and space parts of partial differential equations, being independent in variables,
can be related only via constants.
The constants are subsequently identified as frequencies and as time and space eigenvalues.
Fourier introduced this assumption for solving the heat diffusion problem,
relying on the sufficiency of modal decomposition for string vibrations
that had been famously proved by his mentor Lagrange [a].
Fourier's use of _m_ for the constants underscores the intuition of modes
and an expectation of their discreteness,
whereas _f_ or _k_ or _ω_ for frequency or _λ_ for a Lagrange multiplier
would have suggested a continuum of values.

With the Fourier representation taught _incorrectly_ as complete for arbitrary functions of interest in physics,
the fact that
the wave equation _algebraically_ factors into first order "advection" equations leading to d'Alembert solutions
appears commonly confused as somehow making constant frequencies a result.
The present solutions would not have been fundamental had they been representable by a Fourier transform,
which would have also precluded change in frequency with distance.
While Fourier argued the completeness for treating heat and arbitrary _static_ (~β=0) boundary conditions,
subsequent discussions by mathematicians like Cauchy, Weierstrass and Dirichlet
focused exclusively on continuity [b].
Topological transformations of time or space domains like expansion had little interest till relativity.

## Technological challenges and significance

These solutions have been extraordinarily difficult to demonstrate because
- the speed of light _c_ is so large that very large specific frequency rates or phase accelerations (β≡Δω/ω) become
  necessary to obtain measurable shifts within laboratory distances, and
- the spectrometric wavelength or receiver frequency selection processes must be varied at equal rates (because of the
  orthogonality), for which technology has been impossible or prohibitive to build.

While smaller frequency rates would be entailed say for sound in air or water, 
lower frequencies must be used, entailing longer integrations and consequently larger bandwidths
than readily available in instruments.

Even comprehending these chirp solutions tends to be a challenge as
our biological vision and hearing as well as instruments
are selective towards colours and tones of fixed frequencies.
Only deep diving whales seem to at all experience changing pressure on their ears long enough
to allow cognitive exploitation of these chirp modes,
in which sounds of surface prey change in pitch by vertical distance.

Nevertheless,
these expanding solutions promise (see [arXiv:physics/0812.2652](https://arxiv.org/abs/0812.2652))
- instant separation of transmitting sources by range, including
	- separation of non-colocated jammers and noise sources,
	- exposure of covert spread-spectrum sources,
	- and thus to __fundamentally obsolete EW/ECM__ (electronic warfare and counter measures);

- obsoletion of spectrum administration and need for dominance, since
	- non-colocated transmitters could emit the same frequencies without interfering with reception;

- as well as general accessibility to arbitrary wavelengths even without smart materials,
	such as for THz or X-ray imaging with ambient light
	(see [arXiv:physics/0812.1004](https://arxiv.org/abs/0812.1004)).


## Theoretical impact

- __Quantum mechanics__. As the Fourier transform is central to its mathematical formalism, QM depends on the
  traditionally assumed completeness on that of the Fourier transform over arbitrary analytic functions. However, that
  assumption neglects the Dirichlet condition of periodicity: the Fourier representation is only complete over (a)
  _finite_ intervals and (b) infinite _repetitions_ of finite intervals.

  The present solutions exp(iω<sub>0</sub>e<sup>β[t±r/c]</sup>/β) are just as single finite valued and analytic over the
  real domain (t) as a sinusoidal d'Alembert solution exp(iω[t±r/c]), as would be clear from considering arbitrary small
  values for β. It is effectively Fourier-unrepresentable, however, as its frequency varies from -∞ to +∞ over time, so
  its equal power gets spread over the infinite frequency axis. (Note the fundamental difference from the vanishing of
  a finite _energy_ signal in a power spectrum- here the spread is of power from one point in the spectrum.) The very
  existence of these solutions thus means that QM has been incomplete in its mathematical considerations.

  Photon quantization E=ħω must be understood differently in these _chirp_ or _acceleration spectra_. The energy E gets
  _preserved_ by proportional expansion or compression over the spectrum, as formally shown by the Parseval-Plancherel
  theorem for these solutions given in the PCT [[5](Ref.md#5)].

  The main impact appears to be in astrophysics, as cosmological redshifts were hitherto expected to weaken photon
  energies, and this energy loss has been relied on in the reasoning of Olbers' paradox [c].


- __Relativistic Doppler theory__ did not treat accelerations at all [d]. The relativistic space-time representation of
  electromagnetic waves by phase surfaces automatically accounts for relativistic Doppler ([e], §4.2). However, there
  has never been a consideration in physics of _phase lock_, which by definition requires the receiver's reference clock
  to synchronize with the arriving waves _instead of tracking local physical time_. As the very notion of _coherent
  observation_ should be equivalent to observing under phase lock, it follows that relativity never treated coherent
  observations in adequate detail.

  More particularly, the relativistic corrections in current technology, including in NASA's orbit determination and
  tracking, were never correct and sufficient.
  As treated in [[10](Ref.md#10)], the light-time lags arise from the phase acceleration
  of the locked local oscillator (LO) in effect cancelling the incremental Doppler shift from acceleration while the
  signal is in transit.
  The carrier loop locks to ω'
  = ω<sub>0</sub>e<sup>β[t-r/c]</sup>
  ≡ e<sup>-βr/c</sup>.ω<sub>0</sub>e<sup>βt</sup>,
  i.e., to e<sup>-βr/c</sup> times the source-emitted frequency ω=ω<sub>0</sub>e<sup>βt</sup>,
  presenting a lag in the Doppler Δω = -βωr/c
  exactly equal to the expected Doppler change at specific rate β over the light-time r/c.

  The lag is what one expects in FM radars, now common in new cars, in which a ramping frequency is
  continuously transmitted, and the lagging frequencies in returning echoes reveal target ranges.
  In deep space tracking, however,
  the ramp is due to acceleration of the spacecraft,
  and should ramp the uplink frequency arriving at the spacecraft relative to the frequency transmitted from ground.
  The Doppler as eventually measured on the downlink with a fixed turn-around ratio refers to
  the frequency arriving at the spacecraft.
  Each cycle of the uplink signal should therefore exhibit
  the Doppler for the relative velocity v(t) at instant it left the ground station
  and the incremental velocity increase Δv = -a/c by the time that cycle arrives at the spacecraft.
  The lag means that the incremental increase Δv is only seen with a cycle transmitted at time t+r/c,
  and is fundamentally inconsistent with Doppler theory.

  All anomalous aspects of the NEAR and Rosetta 2005 flybys have been very consistent with these lags.
  Furthermore, the anomalies have been consistently absent in similar NASA flybys involving
  newer transponders that have foregone phase lock, making the Doppler tracking _non-coherent_,
  as described in multiple JHU/APL papers on the transponder evolution cited in [[10](Ref.md#10)].
  The very occurrence of the anomalies, and their consistency with these lags, thus implies
  that phase lock and non-phase lock transponders see the signal itself differently.


- __The speed of light postulate__ is broken by the same light-time lags in the range data, implied by the fact that the
  same anomalies resulted when the trajectory was estimated using range data instead of Doppler data
  [[1](Ref.md#1), [2](Ref.md#2), [3](Ref.md#3)].

  While the lags in Doppler could arise simply as shifts as initially described with the present solutions, range data
  comprise round trip times of modulated range codes. The lags therefore necessarily signify longer or _shorter_ round
  trips than expected for light and radar pulses over the same paths, during approach and post-encounter, respectively.

  The lags signify that _modulated information was consistently delivered at speeds c'≈c+v,
  v denoting the instantaneous radial velocity or range rate,
  for over 4 days before and after perigee in both NEAR and Rosetta 2005 flybys_,
  involving over 20 million independent Doppler and range data samples at 10 samples per second.


## Additional references

a. G F Wheeler and W P Crummett, _The vibrating string controversy_, Am J Phys, 56, 1, 33-37 (1987).

b. I Kleiner, _Evolution of the function concept: A brief survey_, The College Math J, 20, 4, 282-300 (1989).

c. P S Wesson, _Olbers's paradox and the spectral intensity of the extragalactic background light_, ApJ, 367, 399-406
   (1991). A Sandage and L M Lubin, The Tolman Surface Brightness Test for the Reality of the Expansion. I-IV,
   arXiv:astro-ph/0102213, Astro J, 121:2271-300, 122:1071-1103 (2001).

d. A Einstein, _On the electrodynamics of moving bodies_, Ann Phys, 17, 10, 891-921 (1905).

e. R M Wald, _General Relativity_, Univ of Chicago (1984).

