__author__ = 'robertv'

from src.DataReaders import StationInfo
from src.Tests.TestSupport import assert_close, assert_same, get_sample_lat_lon

def test_construct():
    """
ST01, 34.808330, -98.023250, 397
ST02, 33.798510, -86.669090, 295
    """
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")
    assert_same(station_info.stations.shape, (3,))
    assert_same(station_info.stations[0], "ST01")
    assert_same(station_info.stations[1], "ST02")
    assert_same(station_info.stations[2], "ST03")

    assert_same(station_info.station_latitudes.shape, (3,))
    assert_close(station_info.station_latitudes[0], 34.808)
    assert_close(station_info.station_latitudes[1], 33.798)
    assert_close(station_info.station_latitudes[2], 32.5)
    assert_close(station_info.station_longitudes[0], -98.023)
    assert_close(station_info.station_longitudes[1], -86.669)
    assert_close(station_info.station_longitudes[2], -88.000)
    print "Pass"


def test_find_lat_lon():
    lats, longs = get_sample_lat_lon()
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")

    left, right, top, bottom = station_info.get_lat_lon_indexes(34.5, -98.0, lats, longs)
    assert_same(left, 1)
    assert_same(right, 2)
    assert_same(top, 2)
    assert_same(bottom, 3)
    print "Pass"

def test_translate():
    lats, longs = get_sample_lat_lon()
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")

    (position, weight) = station_info.get_translation(1, lats, longs)
    assert_same(position, ((0,4), (0,5), (1,4), (1,5)))
    assert_close(weight[0], 0.599)
    assert_close(weight[1], 0.300)
    assert_close(weight[2], 0.0671)
    assert_close(weight[3], 0.0336)
    print "Pass"
