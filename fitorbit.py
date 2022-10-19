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

    def __init__(self, orbit, station, epoch=None):
        """Reference orbit and tracking station on which to base the perturbation."""

        # compute min/max for critical parameters
        aref = orbit.a.to_value(u.m)
        amin = 0.9 * orbit.a.to_value(u.m)
        amax = 1.1 * orbit.a.to_value(u.m)

        eref = orbit.ecc.to_value(u.one)
        emin = 0.9 * orbit.ecc.to_value(u.one)
        emax = 1.1 * orbit.ecc.to_value(u.one)

        params = Parameters()
        params.add('a', min = amin, max = amax, value = aref)
        params.add('ecc', min = emin, max = emax, value = eref)

        params.add('nu', min = -np.pi, max = np.pi, value = orbit.nu.to_value(u.rad))
        params.add('inc', min = 0, max = np.pi, value = orbit.inc.to_value(u.rad))
        params.add('raan', min = 0, max = 2*np.pi, value = orbit.raan.to_value(u.rad))
        params.add('argp', min = 0, max = 2*np.pi, value = orbit.argp.to_value(u.rad))

        if epoch is None:
            epoch = orbit.epoch

        self._params = params
        self._station = station
        self._epoch = epoch

        self._debug = False

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

    def set_debug(self):
        self._debug = True

    def range_residuals(self, params, offsets, data):
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
        self._ephem = self._orbit.to_ephem(EpochsArray(self._epoch + (offsets << u.s)))

        rres = []
        for i, v in enumerate(offsets):
            e = self._epoch + v * u.s
            rv = self._ephem.rv(e)
            meas_r = data[i]
            model_r, model_rr = self._station.range_and_rate(rv, e)
            rres.append((model_r - meas_r).to_value(u.m))
        return rres

    def fit_range_data(self, offsets, data):
        res_func = lambda pars, offs, dats: self.range_residuals(pars, offs, dats)
        self._result = minimize(res_func, self._params, args=(offsets,), kws={'dats': data})

    def doppler_residuals(self, params, offsets, data):
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
        self._ephem = self._orbit.to_ephem(EpochsArray(self._epoch + (offsets << u.s)))

        rres = []
        for i, v in enumerate(offsets):
            e = self._epoch + v * u.s
            rv = self._ephem.rv(e)
            meas_rr = data[i]
            model_r, model_rr = self._station.range_and_rate(rv, e)
            rres.append((model_rr - meas_rr).to_value(u.m/u.s))
        return rres

    def fit_doppler_data(self, offsets, data):
        res_func = lambda pars, offs, dats: self.doppler_residuals(pars, offs, dats)
        self._result = minimize(res_func, self._params, args=(offsets,), kws={'dats': data})

