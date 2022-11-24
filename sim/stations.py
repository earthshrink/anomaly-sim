"""Tracking station antennas of interest.

Contains following antennas

DSN 25 (Goldstone)
DSN 34 (Canberra)

SSN Altair
SSN Millstone

DSN coordinates taken from DSN Handbook 301F (2011).

The DSN Handbook lists cartesian (Table 2), geodetic (Table 5) and geocentric
coordinates (Table 6), the geodetic in deg, min, sec form.

dss25, dss34 coords taken from Horizons query response to ensure closer comparison
"""

from astropy import units as u
from astropy import constants as const
from astropy.time import Time
from astropy.coordinates import EarthLocation, CartesianRepresentation, CartesianDifferential

from poliastro.util import norm
from poliastro.bodies import Earth

import json
import math

class Station:
    """Tracking station model, to compute range and range rate."""

    def __init__(self, name, lon, lat, height, site_code=None):
        self._loc = EarthLocation.from_geodetic(lon, lat, height)
        self._name = name
        self._site_code = site_code

    @property
    def name(self):
        """Name attached to this location for reference."""
        return self._name

    @property
    def horizons_code(self):
        """
        Site code or location encoding for Horizons query.
        The location encoding is currently blocked by astroquery for topographic query.
        """
        if self._site_code:
            return f'{self._site_code}@399'
        code = {
            'lon': self._loc.lon.to_value(u.deg),
            'lat': self._loc.lat.to_value(u.deg),
            'elevation': self._loc.height.to_value(u.km)
        }
        return json.dumps(code)

    def get_gcrs_posvel(self, epoch):
        """Get GCRS position and velocity vectors of this station at given epoch."""
        return self._loc.get_gcrs_posvel(obstime=epoch)

    def range_and_rates(self, rv, epoch):
        """Convert position, velocity state rv to station-relative range, range rate and station component."""

        loc, vel = self._loc.get_gcrs_posvel(obstime=epoch)
        rvec = rv[0] - loc.xyz
        r = norm(rvec)
        vvec = rv[1] - vel.xyz
        rr = vvec.dot(rvec)/r
        return r, rr, vel.xyz.dot(rvec)/r

    def range_and_rate(self, rv, epoch):
        """Convert position, velocity state rv to station-relative range and range rate."""
        r, rr, _ = self.range_and_rates(rv, epoch)
        return r, rr

    def range_rate_accel(self, ephem, epoch):
        """Convert state rv to station-relative range, range rate and radial accelerations."""

        r, rr, v_station = self.range_and_rates(ephem.rv(epoch), epoch)

        e1s = epoch + 1*u.s
        _, n_rr, nv_station = self.range_and_rates(ephem.rv(e1s), e1s)

        net_accel = (n_rr - rr)/(1*u.s)
        station_accel = (nv_station - v_station)/(1*u.s)

        return r, rr, net_accel, station_accel

    def range_rate_elevation(self, rv, epoch):
        """Convert position, velocity state rv to station-relative range, range rate and elevation."""

        loc, vel = self._loc.get_gcrs_posvel(obstime=epoch)

        # angle at Earth's centre
        R = norm(loc.xyz)
        r0 = norm(rv[0])
        arg = rv[0].dot(loc.xyz)/(R*r0)
        theta = math.acos(arg.to_value(u.one))

        # angle at spacecraft
        rvec = rv[0] - loc.xyz
        r = norm(rvec)
        arg = rv[0].dot(rvec)/(r0*r)
        alpha = math.acos(arg.to_value(u.one))

        # angle between Earth's centre and spacecraft, minus horizon
        elev = math.pi/2 - (theta + alpha)

        vvec = rv[1] - vel.xyz
        rr = vvec.dot(rvec)/r
        return r, rr, vel.xyz.dot(rvec)/r, elev*u.rad

    def range_rate_accel_elev(self, ephem, epoch):
        """Convert state rv to station-relative range, range rate, radial accelerations and elevation."""

        r, rr, v_station, elev = self.range_rate_elevation(ephem.rv(epoch), epoch)

        e1s = epoch + 1*u.s
        _, n_rr, nv_station = self.range_and_rates(ephem.rv(e1s), e1s)

        net_accel = (n_rr - rr)/(1*u.s)
        station_accel = (nv_station - v_station)/(1*u.s)

        return r, rr, net_accel, station_accel, elev

    def coord_range_and_rate(self, coords, epoch):
        """Convert astropy coords to station-relative range and range rate."""
        r = coords.get_xyz(xyz_axis=1)[0]
        v = coords.differentials["s"].get_d_xyz(xyz_axis=1)[0]
        return self.range_and_rate((r, v), epoch)

    def rv_with_rangelag(self, rv, epoch):
        """Add station-relative range lag to position, velocity vectors."""

        loc, vel = self._loc.get_gcrs_posvel(obstime=epoch)
        rvec = rv[0] - loc.xyz
        r = norm(rvec)

        vvec = rv[1] - vel.xyz
        rr = vvec.dot(rvec)/r

        dt = r/const.c
        dr = rr*dt
        return rv[0] + dr*rvec/r, rv[1]

    def rv_with_ratelag(self, rv, epoch):
        """Add station-relative range rate lag to position, velocity vectors."""

        loc, _ = self._loc.get_gcrs_posvel(obstime=epoch)
        rvec = rv[0] - loc.xyz
        r = norm(rvec)

        dt = r/const.c
        ra = -Earth.k/(r*r)
        drr = ra*dt
        return rv[0], rv[1] + drr*rvec/r

    def add_to_czml(self, czml, color):
        """Add station to CZML."""
        loc = self._loc
        czml.add_ground_station([loc.lon, loc.lat], self.name, color)


dss25 = Station("Goldstone-25", 243.124600*u.deg, 35.3375595*u.deg, 0.9623240*u.m, site_code=257)
dss34 = Station("Canberra-34", 148.981964*u.deg, -35.398479*u.deg, 0.6920208*u.m, site_code=-34)

ssrAltair = Station("Altair", 167.479328*u.deg, 9.395472*u.deg, 66*u.m)
ssrMillstone = Station("Millstone", -71.490967*u.deg, 42.617442*u.deg, 127*u.m)

esNewNorcia = Station("New Norcia", 116.191500*u.deg, -31.048225*u.deg, 252.2600*u.m)

Stations = {
    "none": None,
    "a": ssrAltair,
    "altair": ssrAltair,
    "Altair": ssrAltair,
    "m": ssrMillstone,
    "millstone": ssrMillstone,
    "Millstone": ssrMillstone,
    "g": dss25,
    "dss25": dss25,
    "goldstone": dss25,
    "Goldstone": dss25,
    "c": dss34,
    "dss34": dss34,
    "canberra": dss34,
    "Canberra": dss34,

    "nn": esNewNorcia,
    "newnorcia": esNewNorcia,
    "NewNorcia": esNewNorcia,
}
