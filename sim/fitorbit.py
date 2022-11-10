"""Least square fit of orbital elements under a perturbation"""

from astropy import units as u

from poliastro.bodies import Earth
from poliastro.frames import Planes
from poliastro.util import norm
from poliastro.twobody.orbit import Orbit
from poliastro.twobody.sampling import EpochsArray

from lmfit import Parameters, minimize, fit_report

import numpy as np

from sim.util import describe_orbit, describe_state, describe_trajectory

class OrbitFitter:

    def __init__(self, orbit, stations, var=0.01, max_iter=None, trace=False, debug=False, epoch=None):
        """Reference orbit and tracking stations to which the perturbations must be minimized."""

        self._debug = debug
        self._trace = trace

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

        if debug:
            print("Range constraints:")
            print("a:", amin, amax)
            print("ecc:", emin, emax)
            print("inc:", imin, imax)
            if max_iter:
                print("max iter:", max_iter)

        params = Parameters()
        params.add('a', min = amin, max = amax, value = aref)
        params.add('ecc', min = emin, max = emax, value = eref)
        params.add('inc', min = imin, max = imax, value = iref)
        params.add('nu', min = -np.pi, max = np.pi, value = orbit.nu.to_value(u.rad))
        params.add('raan', min = 0, max = 2*np.pi, value = orbit.raan.to_value(u.rad))
        params.add('argp', min = 0, max = 2*np.pi, value = orbit.argp.to_value(u.rad))

        if epoch is None:
            epoch = orbit.epoch

        self._ref_params = params
        self._stations = stations
        self._epoch = epoch
        self._maxiter = max_iter

        # computed by fitting
        self._orbit = None
        self._ephem = None
        self._result = None
        self._params = []
        self._resid = []

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


    def iter_trace(self, iternum, params, resid):

        if self._trace:
            self._params.append(params)
            self._resid.append(resid)

        if self._debug:
            print('{}. {:f} {}'.format(iternum, norm(resid*u.one), params.valuesdict()))

        if self._maxiter:
            return self._maxiter <= iternum


    def compute_trajectory(self, params, times):
        vals = params.valuesdict()

        self._orbit = Orbit.from_classical(attractor = Earth,
                                     a=vals['a'] * u.m,
                                     ecc=vals['ecc'] * u.one,
                                     inc=vals['inc'] * u.rad,
                                     raan=vals['raan'] * u.rad,
                                     argp=vals['argp'] * u.rad,
                                     nu=vals['nu'] * u.rad,
                                     epoch = min(self._epoch, times[0]),
                                     plane = Planes.EARTH_EQUATOR)
        self._ephem = self._orbit.to_ephem(EpochsArray(times))


    def range_residuals(self, params, times, data, wts=None):
        self.compute_trajectory(params, times)
        rres = []
        for i, e in enumerate(times):
            rv = self._ephem.rv(e)
            datum = data[i]
            if wts is None or i >= len(wts):
                wt = 1
            else:
                wt = wts[i]
            for si, sv in enumerate(self._stations):
                meas_r = datum[si]
                model_r, model_rr = sv.range_and_rate(rv, e)
                rres.append((model_r - meas_r).to_value(u.m)*wt)
        return rres

    def fit_range_data(self, times, data, weights=None):
        res_func = lambda pars, times, dats, wts: self.range_residuals(pars, times, dats, wts)
        tr_func = lambda pars, iternum, resid, *args, **kws: self.iter_trace(iternum, pars, resid)
        self._result = minimize(res_func, self._ref_params, args=(times,), kws={'dats': data, 'wts': weights}, iter_cb=tr_func)


    def doppler_residuals(self, params, times, data, wts=None):
        self.compute_trajectory(params, times)
        rres = []
        for i, e in enumerate(times):
            rv = self._ephem.rv(e)
            datum = data[i]
            if wts is None or i >= len(wts):
                wt = 1
            else:
                wt = wts[i]
            for si, sv in enumerate(self._stations):
                meas_rr = datum[si]
                model_r, model_rr = sv.range_and_rate(rv, e)
                rres.append((model_rr - meas_rr).to_value(u.m/u.s)*wt)
        return rres

    def fit_doppler_data(self, times, data, weights=None):
        res_func = lambda pars, offs, dats, wts: self.doppler_residuals(pars, offs, dats, wts)
        tr_func = lambda pars, iternum, resid, *args, **kws: self.iter_trace(iternum, pars, resid)
        self._result = minimize(res_func, self._ref_params, args=(times,), kws={'dats': data, 'wts': weights}, iter_cb=tr_func)

