from src.DataReaders import GEFS_Variable
from src.Tests import verify_data_looks_ok as vd

__author__ = 'robertv'

import pickle
from src.Helpers import date_lists_are_same

data_descriptors = [
        ("dlwrf", "sfc", "Downward_Long-Wave_Rad_Flux" ),
        ("dswrf", "sfc", "Downward_Short-Wave_Rad_Flux" ),
        ("tmax", "2m", 'Maximum_temperature'),
        ("tmin", "2m", 'Minimum_temperature'),
        ("tmp", "sfc", "Temperature_surface"),
        ("tmp", "2m", "Temperature_height_above_ground"),
        ("ulwrf", "sfc", "Upward_Long-Wave_Rad_Flux_surface"),
        ("ulwrf", "tatm", 'Upward_Long-Wave_Rad_Flux'),
        ("uswrf", "sfc", "Upward_Short-Wave_Rad_Flux"),
        ("apcp", "sfc","Total_precipitation" ),
        ('pres', "msl", "Pressure"),
        ('pwat', "eatm", "Precipitable_water"),
        ('spfh', '2m', "Specific_humidity_height_above_ground"),
        ("tcdc", "eatm", "Total_cloud_cover"),
        ("tcolc", "eatm", 'Total_Column-Integrated_Condensate'),
        ]


def get_GEFS_data_from_files(solar_output_training_data, station_info):
    show_plots=False

    try:
        print "read data from pk files"
        with open('training_data_set.pk', 'rb') as input:
            training_data_set = pickle.load(input)
        with open('test_data_set.pk', 'rb') as input:
            test_data_set = pickle.load(input)

    except IOError:
        (training_data_set, test_data_set) = _get_GEFS_data(solar_output_training_data, station_info)

        print "write data to pk files"
        with open('training_data_set.pk', 'wb') as output:
            pickle.dump(training_data_set, output, pickle.HIGHEST_PROTOCOL)

        with open('test_data_set.pk', 'wb') as output:
            pickle.dump(test_data_set, output, pickle.HIGHEST_PROTOCOL)

    print "data retrieval complete"

    trimmed_data_set = trim_unwanted_data(training_data_set)
    trimmed_test_set = trim_unwanted_data(test_data_set)

    for training_data in trimmed_data_set:
        if show_plots:
            vd.show_output_vs_gefsdata(training_data, training_data.name, station_info, solar_output_training_data)

    return (trimmed_data_set, trimmed_test_set)

def trim_unwanted_data(original_dataset):
    trimmed_data_set = []
    for gefs_data in original_dataset:
        alias = gefs_data.alias
        if alias == "dswrf" or \
            alias == "uswrf" or \
            alias == "tmax" or \
            alias == "apcp" or \
            alias == "tcdc" or \
            alias == "ulwrf":
            trimmed_data_set.append(gefs_data)
    return trimmed_data_set


def threshold_data(training_data_set):
    for training_data in training_data_set:
        if training_data.alias == "tmaxX":
            training_data.data[training_data.data < 100] = 100
        elif training_data.alias == "ulwrf":
            training_data.data[training_data.data < 400] = 350
        elif training_data.alias == "apcp":
            training_data.data[training_data.data < 0.10] = 0.05
        elif training_data.alias == "tcdc":
            training_data.data[training_data.data < 0.03] = 0.01
    return training_data_set

def _get_GEFS_data(solar_output_training_data, station_info):

    # Get GEFS data and make sure it looks OK
    # apcp_values_training_data, apcp_values_test_data = GEFS_Variable.get_gefs_data("apcp", "Total_precipitation")
    # assert date_lists_are_same(apcp_values_training_data.dates, solar_output_training_data.dates)
    #

    training_data_set = []
    test_data_set = []
    #data_descriptors = []
    for (alias, type, var_name) in data_descriptors:
        print "Loading data: " + var_name
        training_data, test_data = GEFS_Variable.get_gefs_data(alias, type, var_name)
        training_data_set.append(training_data)
        test_data_set.append(test_data)
        assert date_lists_are_same(training_data.dates, solar_output_training_data.dates)

    # Add second order features
    #training_data, test_data = GEFS_Variable.get_gefs_data("uswrf", "sfc", "Upward_Short-Wave_Rad_Flux")
    #training_data_sq = training_data ^ 2
    #test_data_sq = test_data ^ 2


    print "Loaded all data"
    return (training_data_set, test_data_set)