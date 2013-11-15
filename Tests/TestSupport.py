__author__ = 'robertv'

import math
import numpy as np
from src.DataReaders import GEFS_Variable

def assert_same(v1, v2):
    if v1 != v2:
        print "FAIL: v1=" + str(v1) + " v2=" + str(v2)
        assert False
    return

def assert_close(v1, v2):
    error_value = math.fabs(v1 - v2)
    if v1 == 0.0:
        error_percent = error_value
    else:
        error_percent = error_value / v1
    if error_percent > 0.001:
        print "FAIL: v1=" + str(v1) + " v2=" + str(v2)
        assert False
    return


def get_sample_lat_lon():
    lats = np.array([32.0, 34.0, 36.0, 38.0])         # 31 .. 39
    longs = np.array([250.0, 255.0, 260.0, 265.0, 270.0, 275.0])  # 254 .. 269
    return lats, longs - 360                    # GEFS_Variable does this adjustment


def get_sample_gefs_data(num_dates):
    """
        the generated data t=0:
            1 2 3 4
            5 6 7 8
            9
            13
            17
            21     24

        t=1
            25
                    48
        t=2
            49
                    72
        t=3
            73
                    96
        For the next ensemble:
            97
                    120
            121
                    144
            145
                    168
            169
                    192
        Third ensemble:
            193     216
            217     240
            241     264
            265     288

    Average over time
            37      60
            133     156
            229     252
    Average over ensembles
            133     156
    """
    num_ensembles = 3
    num_times = 4
    lats, longs = get_sample_lat_lon()
    gefs_data = GEFS_Variable.GEFS_Variable(None, None, None)
    gefs_data.latitudes = lats
    gefs_data.longitudes = longs
    gefs_data.data = np.zeros(shape=(num_dates, num_ensembles, num_times, lats.shape[0], longs.shape[0]))
    val = 1.0
    for date in range(0, num_dates):
        for ens in range(0, num_ensembles):
            for time in range(0, num_times):
                for lat in range(0, lats.shape[0]):
                    for long in range(0, longs.shape[0]):
                        gefs_data.data[date, ens, time, lat, long] = val
                        val += 1.0

    return gefs_data