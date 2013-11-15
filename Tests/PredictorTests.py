__author__ = 'robertv'

import numpy as np
from src.Predictor import find_fit_parameters
from src.LinearGradientDescent import derivative_of_linear_cost_function_MAE, predict_linear_value
from src.Helpers import get_daily_data_from_hourly, translate_gefs_into_station
from src.DataReaders import StationInfo, StationTrainingData
from src.Tests.TestSupport import assert_same, assert_close, get_sample_gefs_data


def test_data_averager():
    """
        the generated

    """
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = StationTrainingData.StationTrainingData("StationTrainingTestData.csv", station_info)
    num_dates = solar_output_training_data.dates.shape[0]
    gefs_data = get_sample_gefs_data(num_dates)

    relevant_data = get_daily_data_from_hourly(gefs_data)
    assert_same(relevant_data.shape, (2, 4, 6))
    assert_same(relevant_data[0,0,0], 133.0 )
    assert_same(relevant_data[0,0,1], 134.0 )
    assert_same(relevant_data[0,1,0], 139.0 )
    assert_same(relevant_data[0,2,0], 145.0 )
    assert_same(relevant_data[0,3,0], 151.0 )
    assert_same(relevant_data[0,3,5], 156.0 )
    assert_same(relevant_data[1,0,0], 421.0 )
    print "Pass"



def test_translator():
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = StationTrainingData.StationTrainingData("StationTrainingTestData.csv", station_info)

    num_dates = solar_output_training_data.dates.shape[0]
    num_stations = solar_output_training_data.station_info.stations.shape[0]
    gefs_data = get_sample_gefs_data(num_dates)
    training_data = get_daily_data_from_hourly(gefs_data)
    station_data = translate_gefs_into_station(training_data, gefs_data.latitudes, gefs_data.longitudes, solar_output_training_data.station_info, 0)

    assert_same(station_data.shape, (num_dates, ))
    print "Pass"


def test_fit_finder():
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = StationTrainingData.StationTrainingData("StationTrainingTestData.csv", station_info)
    num_dates = solar_output_training_data.dates.shape[0]
    gefs_data = get_sample_gefs_data(num_dates)

    fitted_theta = find_fit_parameters([gefs_data], solar_output_training_data)
    #print sys._getframe().f_code.co_name, fitted_theta
    print "Pass"

def test_fit_finder_for_two_in_set():
    station_info = StationInfo.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = StationTrainingData.StationTrainingData("StationTrainingTestData.csv", station_info)
    num_dates = solar_output_training_data.dates.shape[0]
    gefs_data = get_sample_gefs_data(num_dates)

    fitted_theta = find_fit_parameters([gefs_data,gefs_data], solar_output_training_data)
#    print sys._getframe().f_code.co_name, fitted_theta
    print "Pass"

def test_cost_function_MAE_when_cost_zero():
    X = np.array([[1,2],
                 [1,4],
                 [1,7]])

    theta = np.array([2.5, 4.5])
    y = np.array([11.5, 20.5, 34.0])
    gradient = derivative_of_linear_cost_function_MAE(X, theta, predict_linear_value, y)
    assert_same(gradient[0], 0)
    assert_same(gradient[1], 0)

    print "Pass"

def test_cost_function_MAE_when_cost_nonzero():
    """
        cost = MAE = |h-y| = |T0x0 + T1x1 - y|
        if T0x0 + T1x1 - y > 0
            dJ/dT0 = x0
            dJ/dT1 = x1
        if T0x0 + T1x1 -y < 0
            dJ/dT0 = -x0
            dJ/dT1 = -x1

    """
    X = np.array([[1,2],
                 [1,4],
                 [1,7]])

    theta = np.array([2.5, 4.5])
    y = np.array([10.5, 21.5, 35.0])
    gradient = derivative_of_linear_cost_function_MAE(X, theta, predict_linear_value, y)
    assert_close(gradient[0], -1.0/3.0)
    assert_close(gradient[1], -9.0/3.0)

    print "Pass"
