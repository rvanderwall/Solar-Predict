__author__ = 'robertv'

import numpy as np

def station_lists_are_same(station_list1, station_list2):
    return lists_are_same(station_list1, station_list2)


def date_lists_are_same(date_list1, date_list2):
    return lists_are_same(date_list1, date_list2)


def lists_are_same(l1, l2):
    assert l1.shape == l2.shape
    index = 0
    for item1 in l1:
        assert l2[index] == item1
        index += 1

    return True


def get_daily_data_from_hourly(full_data):
    """
        Average out over time and ensembles
        returns (date, lat, long)
    @param full_data:
    @return:
    """
    ensemble_average = np.average(full_data.data, axis=1)
    hourly_average = np.average(ensemble_average, axis=1)
    return hourly_average


def translate_gefs_into_station(training_data, latitudes, longitudes, station_info, station_index):
    """
        Accepts GEFS data, GEFS locations and station locations
        interpolates the GEFS data and returns approximated station data
    @param latitudes:
    @param longitudes:
    @param station_info:
    @param station_index:
    @return:
    """
    (positions, weights) = station_info.get_translation(station_index, latitudes, longitudes)
    data = np.zeros(shape=training_data.shape[0])
    for index in range(0, len(positions)):
        data += weights[index] * training_data[:, positions[index][0], positions[index][1]]

    return data
