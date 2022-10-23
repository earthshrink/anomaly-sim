"""Track epochs of several Earth flybys"""


from astropy.time import Time
from enum import Enum 


class Tracking(Enum):

    """NEAR: from Antreasian & Guinn, 1998"""

    NEAR_PERIGEE                = Time("1998-01-23 07:22:55")

    NEAR_SSN_START              = Time("1998-01-23 06:12:00", scale="tdb")
    NEAR_SSN_END                = Time("1998-01-23 06:54:00", scale="tdb")

    NEAR_GOLDSTONE_START        = Time("1998-01-13 12:00:00", scale="tdb")      # AG: ~10 days
    NEAR_GOLDSTONE_END          = Time("1998-01-23 06:14:55.6", scale="tdb")

    NEAR_CANBERRA_START         = Time("1998-01-23 09:53:55.6", scale="tdb")    # AG: +2h 31m
    NEAR_CANBERRA_END           = Time("1998-02-23 12:00:00", scale="tdb")      # AG: ~30 days


    """Rosetta 2005: Morley & Budnik, 2006 states perigee at 22:10:18.3"""

    ROSETTA05_PERIGEE           = Time("2005-03-04 22:09:14")       # JPL/Horizons min alt


    """Rosetta later flybys: T Morley (pvt.)""" 

    ROSETTA07_PERIGEE           = Time("2007-11-13 20:57:00")

    ROSETTA07_NEWNORCIA_END     = Time("2007-11-13 19:59:00")       # -58m
    ROSETTA07_GOLDSTONE24_START = Time("2007-11-13 21:21:00")       # +24m


    ROSETTA09_PERIGEE           = Time("2009-11-13 07:45:40")

    ROSETTA09_KOUROU_END        = Time("2009-11-12 20:57:21")

    ROSETTA09_NEWNORCIA_START   = Time("2009-11-13 07:29:25")       # perigee was tracked
    ROSETTA09_NEWNORCIA_END     = Time("2009-11-13 07:40:25")       # perigee was tracked

    ROSETTA09_MASPALOMAS_START  = Time("2009-11-13 08:06:07")
    ROSETTA09_MASPALOMAS_END    = Time("2009-11-13 10:10:07")

