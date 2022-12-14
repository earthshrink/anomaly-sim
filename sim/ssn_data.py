"""SSN reference data from Antreasian & Guinn's graph"""


from enum import Enum
from astropy.time import Time

class SSNdata(Enum):
    """
    See https://github.com/earthshrink/flyby-analysis/blob/refine_estimates/near/near_ssn.tex
    for the deconstruction and source of data below.
    """

    MILLSTONE   = {
                Time("1998-01-23 06:25.20"): -730 ,
                Time("1998-01-23 06:36.80"): -605 ,
                Time("1998-01-23 06:44.80"): -505
                }

    ALTAIR = {
                Time("1998-01-23 06:14.50"): -929 ,
                Time("1998-01-23 06:15.90"): -929 ,
                Time("1998-01-23 06:16.34"): -908 ,
                Time("1998-01-23 06:17.25"): -894 ,
                Time("1998-01-23 06:17.75"): -881 ,
                Time("1998-01-23 06:18.67"): -867 ,
                Time("1998-01-23 06:20.50"): -853 ,
                Time("1998-01-23 06:21.45"): -847 ,
                Time("1998-01-23 06:22.90"): -832 ,
                Time("1998-01-23 06:23.45"): -818 ,
                Time("1998-01-23 06:23.94"): -825 ,
                Time("1998-01-23 06:24.18"): -805 ,
                Time("1998-01-23 06:24.90"): -804 ,
                Time("1998-01-23 06:27.22"): -779 ,
                Time("1998-01-23 06:31.40"): -717 ,
                Time("1998-01-23 06:34.02"): -695 ,
                Time("1998-01-23 06:35.42"): -666 ,
                Time("1998-01-23 06:35.93"): -671 ,
                Time("1998-01-23 06:37.36"): -658 ,
                Time("1998-01-23 06:38.65"): -614 ,
                Time("1998-01-23 06:39.15"): -598 ,
                Time("1998-01-23 06:40.35"): -597 ,
                Time("1998-01-23 06:40.64"): -588 ,
                Time("1998-01-23 06:42.00"): -575 ,
                Time("1998-01-23 06:42.35"): -567 ,
                Time("1998-01-23 06:43.10"): -553 ,
                Time("1998-01-23 06:43.35"): -556 ,
                Time("1998-01-23 06:43.58"): -544 ,
                Time("1998-01-23 06:43.85"): -533 ,
                Time("1998-01-23 06:44.89"): -520 ,
                Time("1998-01-23 06:45.85"): -512 ,
                Time("1998-01-23 06:46.10"): -501 ,
                Time("1998-01-23 06:47.63"): -482 ,
                Time("1998-01-23 06:48.85"): -467 ,
                Time("1998-01-23 06:49.15"): -472 ,
                Time("1998-01-23 06:50.20"): -450 ,
                Time("1998-01-23 06:50.58"): -446 ,
                Time("1998-01-23 06:51.05"): -444 ,
                Time("1998-01-23 06:51.54"): -454
                }
