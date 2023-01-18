#!/usr/bin/env python
"""Utility functions used in the notebooks"""

from itertools import pairwise

from astropy import visualization
from astropy import units as u
from astropy.time import Time

from poliastro.util import norm
from poliastro.frames import Planes
from poliastro.ephem import Ephem
from poliastro.bodies import Earth

from poliastro.twobody.orbit import Orbit
from astroquery.jplhorizons import Horizons

from scipy import signal
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def orbit_from_horizons(spacecraft, epoch):
    """Compute orbital elements for flyby with initial coordinates from JPL Horizons."""

    ephem = Ephem.from_horizons(spacecraft, epoch, attractor=Earth, plane=Planes.EARTH_EQUATOR)
    rv = ephem.rv(epoch)
    return Orbit.from_vectors(Earth, rv[0], rv[1], epoch)


def make_epochs(start, end, interval):
    """Compile epochs array for simulation."""

    offsets = np.arange(0, (end-start)/(1*u.s), interval.to_value(u.s))
    return start + (offsets << u.s)


def horizons_range_rate_accel(spacecraft, station, epoch):
    """Topocentric range, range rate and radial acceleration from JPL Horizons."""

    loc = station.horizons_code
    epochs = make_epochs(epoch, epoch+1*u.s, 0.5*u.s)

    query = Horizons(id=spacecraft, location=loc, epochs=epochs.jd, id_type=None)
    obj = query.vectors(refplane="earth")
    r = obj["range"].quantity[0]
    rr = obj["range_rate"].quantity[0]
    n_rr = obj["range_rate"].quantity[1]

    return r, rr, (n_rr - rr)/(0.5*u.s)


def describe_orbit(orbit):
    """Summary of orbital elements."""

    print()
    print("::ORBIT::")
    print("Plane:", orbit.plane)
    print("Inclination:", orbit.inc << u.deg)
    print("Eccentricity:", orbit.ecc)
    print("Semilatus rectum:",orbit.p)
    print("Semimajor axix:",orbit.a)
    print("Periapse radius:", orbit.r_p, ", altitude:", orbit.r_p-orbit.attractor.R)


def compare_orbits(a, b):
    """Compare orbital elements."""

    assert a.plane == b.plane
    print()
    print("Δ Inclination:", (b.inc - a.inc) << u.deg)
    print("Δ Eccentricity:", (b.ecc - a.ecc))
    print("Δ Semilatus rectum:", (b.p - a.p) << u.km)
    print("Δ Semimajor axix:", (b.a - a.a) << u.km)
    print("Δ Periapse radius:", (b.r_p - a.r_p) << u.km)
    print("Δ Energy:", (b.energy - a.energy) << (u.km*u.km)/(u.s*u.s))


def describe_state(rv, station, epoch):
    """Position, velocity coordinates in relation to a tracking station."""

    print()
    print(":AT:", epoch)
    r, rr = station.range_and_rate(rv, epoch)
    print("Geocentric distance:", norm(rv[0]) << u.km, "speed:", norm(rv[1]) << (u.km/u.s))
    print("From", station.name, ": range ", r << u.km, ", range rate ", rr << (u.km/u.s))


def describe_trajectory(ephem, station):
    """Summary of a trajectory segment, and relation to a tracking station."""

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
    """Find swings in an oscillating time sequency."""

    peaks = signal.find_peaks(values)
    troughs = signal.find_peaks(np.multiply(-1, values))

    swing = {}
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


def find_rates(times, residual):
    """Compute rates in residual."""

    rate = []
    for i, e in enumerate(times[1:]):
        dr = residual[i] - residual[i-1]
        dt = (e - times[i-1]).to_value(u.s)
        rate.append(dr/dt)

    return rate


def plot_residual(times, residual, title, ylab, ylim=None, ax=None):
    """Plot trajectory residual from a least square fit."""

    visualization.time_support()
    newplot = ax is None

    if newplot:
        _, ax = plt.subplots()
        plt.xlabel(None)
        plt.ylabel(ylab)
        plt.grid(axis='x')
        plt.gcf().autofmt_xdate()

        if ylim:
            ax.set_ylim(ylim)

        if title:
            plt.title(title)

        if times[-1] - times[0] > 10*u.day:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))

        elif times[-1] - times[0] > 1*u.day:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

        elif times[-1] - times[0] > 3*u.hour:
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

        elif times[-1] - times[0] > 20*u.minute:
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))

        else:
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))

    if isinstance(residual, dict):
        for v in residual:
            ax.plot(times, [v * 1e3 for v in residual[v]], label = f'{v.name}')
        plt.legend(loc="best")
    else:
        ax.plot(times, [v * 1e3 for v in residual])

    return plt

def plot_swings(times, residual, title, ylab, minmax=False):
    """Plot the swings in an oscillating residual."""

    peak_epochs, peak_swings = find_swings(times, residual)
    visualization.time_support()
    _, ax = plt.subplots()
    plt.xlabel(None)
    plt.ylabel(ylab)
    plt.grid(axis='x')
    plt.scatter(peak_epochs, peak_swings)

    if times[-1] - times[0] > 5*u.day:
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))

    elif times[-1] - times[0] > 1*u.day:
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

    elif times[-1] - times[0] > 20*u.minute:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))

    if title:
        plt.title(title)
    plt.gcf().autofmt_xdate()

    if minmax:
        print(min(peak_swings), max(peak_swings))
    else:
        print(peak_swings[-4:])

    return peak_epochs, peak_swings
