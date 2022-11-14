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
from astropy.coordinates import EarthLocation
from poliastro.bodies import Earth

from poliastro.util import norm

class Station:
    """Tracking station model, to compute range and range rate."""

    def __init__(self, name, lon, lat, height):
        self._loc = EarthLocation.from_geodetic(lon, lat, height)
        self._name = name

    @property
    def name(self):
        """Name attached to this location for reference."""
        return self._name

    def get_gcrs_posvel(self, epoch):
        """Get GCRS position and velocity vectors of this station at given epoch."""
        return self._loc.get_gcrs_posvel(obstime=epoch)

    def range_and_rate(self, rv, epoch):
        """Convert position, velocity state rv to station-relative range and range rate."""

        loc, vel = self._loc.get_gcrs_posvel(obstime=epoch)
        rvec = rv[0] - loc.xyz
        r = norm(rvec)
        vvec = rv[1] - vel.xyz
        rr = vvec.dot(rvec)/r
        return r, rr

    def range_rate_accel(self, rv, epoch):
        """Convert state rv to station-relative range, range rate and radial acceleration."""

        loc, vel = self._loc.get_gcrs_posvel(obstime=epoch)
        rvec = rv[0] - loc.xyz
        r = norm(rvec)
        vvec = rv[1] - vel.xyz
        rr = vvec.dot(rvec)/r

        n_loc, n_vel = self._loc.get_gcrs_posvel(obstime=epoch+1*u.s)
        rot_accel = ( (n_vel.xyz - vel.xyz).dot(rvec)/r )/(1*u.s)

        g_accel = (-Earth.k/(rv[0]*rv[0])).dot(rvec)/r
        #print(g_accel << (u.m/(u.s*u.s)), rot_accel << (u.m/(u.s*u.s)))

        return r, rr, g_accel + rot_accel

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

dss25 = Station("Goldstone-25", 243.124600*u.deg, 35.3375595*u.deg, 0.9623240*u.m)
dss34 = Station("Canberra-34", 148.981964*u.deg, -35.398479*u.deg, 0.6920208*u.m)

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
