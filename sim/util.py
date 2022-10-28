#!/usr/bin/env python

from astropy import units as u
from astropy.time import Time

from poliastro.util import norm
from poliastro.frames import Planes
from poliastro.bodies import Earth
from poliastro.ephem import Ephem
from poliastro.twobody.orbit import Orbit

from scipy import signal
from itertools import pairwise
import numpy as np

def describe_orbit(orbit):
    print()
    print("::ORBIT::")
    print("Plane:", orbit.plane)
    print("Inclination:", orbit.inc << u.deg)
    print("Eccentricity:", orbit.ecc)
    print("Semilatus rectum:",orbit.p)
    print("Semimajor axix:",orbit.a)
    print("Periapse radius:", orbit.r_p, ", altitude:", orbit.r_p-orbit.attractor.R)


def compare_orbits(a, b):
    assert(a.plane == b.plane)
    print()
    print("Δ Inclination:", (b.inc - a.inc) << u.deg)
    print("Δ Eccentricity:", (b.ecc - a.ecc))
    print("Δ Semilatus rectum:", (b.p - a.p) << u.km)
    print("Δ Semimajor axix:", (b.a - a.a) << u.km)
    print("Δ Periapse radius:", (b.r_p - a.r_p) << u.km)
    print("Δ Energy:", (b.energy - a.energy) << (u.km*u.km)/(u.s*u.s))


def describe_state(rv, station, epoch):
    print()
    print(":AT:", epoch)
    r, rr = station.range_and_rate(rv, epoch)
    print("Geocentric distance:", norm(rv[0]) << u.km, "speed:", norm(rv[1]) << (u.km/u.s))
    print("From", station.name, ": range ", r << u.km, ", range rate ", rr << (u.km/u.s))


def describe_state_data(rv, station, epoch):
    print()
    print(":AT:", epoch)
    x, v = station.get_gcrs_posvel(epoch)
    print("station", x.xyz << u.km, v.xyz << (u.km/u.s))
    print("object", rv[0] << u.km, rv[1] << (u.km/u.s))


def describe_trajectory(ephem, station):
    print()
    print("::TRAJECTORY::")

    rv = [station.coord_range_and_rate(ephem.sample(e), e) for e in ephem.epochs]

    ranges = [x[0] for x in rv]
    speeds = [x[1] for x in rv]

    print("Start and end ranges:", ranges[1] << u.km, ranges[-1] << u.km)
    print("Start and end radial speeds:", speeds[0] << (u.km/u.s), speeds[-1] << (u.km/u.s))

    min_range = min(ranges)

    periapse_indices = [i for i, v in enumerate(ranges) if v == min_range]
    periapse_epoch = ephem.epochs[periapse_indices[0]]
    periapse_speed = norm(ephem.rv(periapse_epoch)[1]) << (u.km/u.s)

    print("Closest:", min_range, "speed", periapse_speed, " at ", periapse_epoch)

    initial_velocity = ephem.rv(ephem.epochs[0])[1]
    final_velocity = ephem.rv(ephem.epochs[-1])[1]
    inner = np.inner(initial_velocity, final_velocity)
    norms = norm(initial_velocity)*norm(final_velocity)
    cos = inner/norms
    print("Deflection:", np.degrees(np.arccos(cos)))


def find_swings(epochs, values):
    peaks = signal.find_peaks(values)
    troughs = signal.find_peaks(-values)

    swing = dict()
    for i, v in enumerate(peaks[0]):
        swing[v] = values[v]
    for i, v in enumerate(troughs[0]):
        swing[v] = values[v]

    swing_epochs = []
    swing_heights = []
    for i, j in pairwise(sorted(swing)):
        swing_epochs.append(epochs[j])
        swing_heights.append(abs(swing[j]-swing[i]))

    return Time(swing_epochs), swing_heights

