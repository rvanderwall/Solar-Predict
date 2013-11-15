from src import DataReaders as si

__author__ = 'robertv'

import numpy as np
from src.Tests.TestSupport import assert_close

def verify_cost_function_when_identical():
    station_info = si.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = std.StationTrainingData("StationTrainingTestData.csv", station_info)

    prediction = np.array([[19940101, 12384900, 11930700, 10000000],
                           [19940102, 11908500, 9778500, 12000000]])
    cost = solar_output_training_data.cost(prediction[:,1:])

    assert_close(cost, 0.0)
    print "Pass"

def verify_cost_function_when_different_station():
    station_info = si.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = std.StationTrainingData("StationTrainingTestData.csv", station_info)

    prediction = np.array([[19940101, 12384900, 11930700, 0],
                           [19940102, 11908500, 9778500, 12000000]])
    cost = solar_output_training_data.cost(prediction[:,1:])

    assert_close(cost, 1666667.0)  # 10000000 / 6
    print "Pass"

def verify_cost_function_when_different_times():
    station_info = si.StationInfo("StationInfoTestData.csv")
    solar_output_training_data = std.StationTrainingData("StationTrainingTestData.csv", station_info)

    prediction = np.array([[19940101, 12384900, 11930700, 10000000],
                           [19940102, 11908500, 0, 12000000]])
    cost = solar_output_training_data.cost(prediction[:,1:])

    assert_close(cost, 1629750) # 9778500 / 6
    print "Pass"
