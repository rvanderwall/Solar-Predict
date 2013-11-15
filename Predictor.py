__author__ = 'robertv'

import numpy as np
from numpy import linalg
from src.Helpers import get_daily_data_from_hourly, translate_gefs_into_station
from src.GradientDescentCoreHelpers import feature_normalization_constants, normalize_features, reconstruct_theta
from src.LinearGradientDescent import linear_gradient_descent


def find_fit_parameters(set_of_gefs_data, station_training_labels):
    """
    training_data.data is a 5d matrix:
        date , ensemble, timeOfDay, lat, lon

    returns weights(theta) as a 2-d where
        each row is for a given station
        each column is a weather parameter/feature (1 extra for constant)
    @todo vectorize the stations.  For now, we run through each station in a loop building up theta as we go
    @param training_data:
    @param station_training_labels:
    @return:
    """

    latitudes, longitudes = get_lat_lon_from_dataset(set_of_gefs_data)
    num_stations = station_training_labels.station_info.stations.shape[0]

    # Now get actual data from each set
    training_data_set = get_daily_dataset_from_hourlyset(set_of_gefs_data)

    num_features = len(training_data_set) + 1
    theta = np.empty(shape=(num_stations,num_features))
    for s in range(0,num_stations):
        station_training_data_set = []
        for training_data in training_data_set:
            station_training_data = translate_gefs_into_station(training_data, latitudes, longitudes, station_training_labels.station_info, s)
            station_training_data_set.append(station_training_data)

        print "Station: " + str(s)
        # theta[s,0], theta[s,1] = use_simple_average(labeled_data, station_id)
        #theta[s] = use_linear_regression(station_training_data_set, station_training_labels.solar_output_for_station(s))
        theta[s] = use_gradient_descent(station_training_data_set, station_training_labels.solar_output_for_station(s))
    return theta


def get_prediction(training_weights, set_of_gefs_data, station_info):

    """
    weights should be (S, P+1)
        S = station
        P = weather parameter features
    @param training_weights:
    @param unlabeled_gefs_data:
    @return:
    """

    latitudes, longitudes = get_lat_lon_from_dataset(set_of_gefs_data)
    prediction_dates_list = set_of_gefs_data[0].dates
    num_dates = prediction_dates_list.shape[0]

    # Now get actual data from each set
    training_data_set = get_daily_dataset_from_hourlyset(set_of_gefs_data)

    num_stations = station_info.stations.shape[0]
    predict_for_stations = None
    for s in range(0,num_stations):

        X = np.ones(shape=(num_dates,1))
        for training_data in training_data_set:
            station_training_data = translate_gefs_into_station(training_data, latitudes, longitudes, station_info, s)
            X = np.append(X, np.reshape(station_training_data, (-1,1)), axis=1)

        predict = np.dot(X, training_weights[s,:])
        if predict_for_stations == None:
            predict_for_stations = np.reshape(predict, (-1,1))
        else:
            predict_for_stations = np.append(predict_for_stations, np.reshape(predict, (-1,1)), axis=1)


    dates = np.reshape(prediction_dates_list,(-1,1))
    return np.append(dates, predict_for_stations, axis=1)


def use_simple_average(labeled_data, station_id):
    w0 = labeled_data.average_solar_influx_for_station(station_id)
    w1 = 0
    return w0, w1


def use_linear_regression(station_data_set, labeled_data):
    data_size = len(station_data_set[0])
    A = np.ones(data_size)
    for station_data in station_data_set:
        A = np.vstack((A, station_data))
    w = linalg.lstsq(A.T,labeled_data)[0] # obtaining the parameters
    return w

def use_gradient_descent(station_data_set, labeled_data):
    A = None

    for station_data in station_data_set:
        if A == None:
            A = station_data
        else:
            A = np.vstack((A, station_data))

    (mu, sigma) = feature_normalization_constants(A.T)
    X = normalize_features(A.T, mu, sigma)
    y = np.reshape(labeled_data,(-1,1))
    num_features = X.shape[1]
    initial_theta = np.zeros((num_features+1,1))
    alpha = 50000
    iterations = 2000
    (theta, J) = linear_gradient_descent(X, y, initial_theta, alpha, iterations) # obtaining the parameters
    #plotter.plot_cost_function(J, "predictor")
    print "Cost: " + str(J[iterations-1])
    w = reconstruct_theta(theta, mu, sigma)
    return np.reshape(w, (w.shape[0],))



def get_lat_lon_from_dataset(data_set):
    # Assume all gefs_data sets are similar in location data and that we have at least one in set.
    first_unlabeled_gefs_data = data_set[0]
    latitudes = first_unlabeled_gefs_data.latitudes
    longitudes = first_unlabeled_gefs_data.longitudes

    return latitudes, longitudes


def get_daily_dataset_from_hourlyset(set_of_gefs_data):
    # Now get actual data from each set
    training_data_set = []
    for unlabeled_gefs_data in set_of_gefs_data:
        training_data = get_daily_data_from_hourly(unlabeled_gefs_data)
        training_data_set.append(training_data)

    return training_data_set


