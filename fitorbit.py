"""Least square fit of orbital elements under a perturbation"""

from astropy import units as u

from poliastro.bodies import Earth
from poliastro.frames import Planes
from poliastro.twobody.orbit import Orbit
from poliastro.twobody.sampling import EpochsArray

from lmfit import Parameters, minimize, fit_report

import numpy as np

from util import describe_orbit, describe_state, describe_trajectory

class OrbitFitter:

    def __init__(self, orbit, stations, var=0.01, debug=False, epoch=None):
        """Reference orbit and tracking stations to which the perturbations must be minimized."""

        self._debug = debug

        # compute min/max for critical parameters
        aref = orbit.a.to_value(u.m)
        amin = aref * (1-var)
        amax = aref * (1+var)

        eref = orbit.ecc.to_value(u.one)
        emin = eref * (1-var)
        emax = eref * (1+var)

        iref = orbit.inc.to_value(u.rad)
        imin = iref * (1-var)
        imax = iref * (1+var)

        if self._debug:
            print("Range constraints:")
            print("a:", amin, amax)
            print("ecc:", emin, emax)
            print("inc:", imin, imax)

        params = Parameters()
        params.add('a', min = amin, max = amax, value = aref)
        params.add('ecc', min = emin, max = emax, value = eref)
        params.add('inc', min = imin, max = imax, value = iref)
        params.add('nu', min = -np.pi, max = np.pi, value = orbit.nu.to_value(u.rad))
        params.add('raan', min = 0, max = 2*np.pi, value = orbit.raan.to_value(u.rad))
        params.add('argp', min = 0, max = 2*np.pi, value = orbit.argp.to_value(u.rad))

        if epoch is None:
            epoch = orbit.epoch

        self._params = params
        self._stations = stations
        self._epoch = epoch

        # computed by fitting
        self._orbit = None
        self._ephem = None
        self._result = None

    @property
    def result(self):
        return self._result

    def report(self):
        return fit_report(self._result)

    @property
    def orbit(self):
        return self._orbit

    @property
    def ephem(self):
        return self._ephem

    def range_residuals(self, params, times, data):
        vals = params.valuesdict()

        if self._debug:
            print(vals)

        self._orbit = Orbit.from_classical(attractor = Earth,
                                     a=vals['a'] * u.m,
                                     ecc=vals['ecc'] * u.one,
                                     inc=vals['inc'] * u.rad,
                                     raan=vals['raan'] * u.rad,
                                     argp=vals['argp'] * u.rad,
                                     nu=vals['nu'] * u.rad,
                                     epoch = self._epoch,
                                     plane = Planes.EARTH_EQUATOR)
        self._ephem = self._orbit.to_ephem(EpochsArray(self._epoch + (times << u.s)))

        rres = []
        for ti, tv in enumerate(times):
            e = self._epoch + tv * u.s
            rv = self._ephem.rv(e)
            datum = data[ti]
            for si, sv in enumerate(self._stations):
                meas_r = datum[si]
                model_r, model_rr = sv.range_and_rate(rv, e)
                rres.append((model_r - meas_r).to_value(u.m))
        return rres

    def fit_range_data(self, times, data):
        res_func = lambda pars, offs, dats: self.range_residuals(pars, offs, dats)
        self._result = minimize(res_func, self._params, args=(times,), kws={'dats': data})

    def doppler_residuals(self, params, times, data):
        vals = params.valuesdict()

        if self._debug:
            print(vals)

        self._orbit = Orbit.from_classical(attractor = Earth,
                                     a=vals['a'] * u.m,
                                     ecc=vals['ecc'] * u.one,
                                     inc=vals['inc'] * u.rad,
                                     raan=vals['raan'] * u.rad,
                                     argp=vals['argp'] * u.rad,
                                     nu=vals['nu'] * u.rad,
                                     epoch = self._epoch,
                                     plane = Planes.EARTH_EQUATOR)
        self._ephem = self._orbit.to_ephem(EpochsArray(self._epoch + (times << u.s)))

        rres = []
        for ti, tv in enumerate(times):
            e = self._epoch + tv * u.s
            rv = self._ephem.rv(e)
            datum = data[ti]
            for si, sv in enumerate(self._stations):
                meas_rr = datum[si]
                model_r, model_rr = sv.range_and_rate(rv, e)
                rres.append((model_rr - meas_rr).to_value(u.m/u.s))
        return rres

    def fit_doppler_data(self, times, data):
        res_func = lambda pars, offs, dats: self.doppler_residuals(pars, offs, dats)
        self._result = minimize(res_func, self._params, args=(times,), kws={'dats': data})

