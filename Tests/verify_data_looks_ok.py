from src import plotter

__author__ = 'robertv'

from src.Predictor import translate_gefs_into_station, get_lat_lon_from_dataset, get_daily_data_from_hourly
from src.Predictor import get_prediction

def show_output_vs_elevation(station_info, solar_output_training_data):
    elevations = station_info.elevations
    solar_output = []
    stationIndex = 0
    for station in station_info.stations:
        solar_output.append(solar_output_training_data.average_solar_output_for_station(stationIndex))
        stationIndex += 1

    plotter.plot_xy_data(elevations, "elevation", solar_output, "Solar output")

def show_output_vs_gefsdata(gefs_data, gefs_name, station_info, solar_output_training_data):
    stationID = 0
    latitudes, longitudes = get_lat_lon_from_dataset([gefs_data])
    training_data = get_daily_data_from_hourly(gefs_data)
    station_training_data = translate_gefs_into_station(training_data, latitudes, longitudes, station_info, stationID)

    solar_output = solar_output_training_data.station_solar_output_data[:,stationID]

    plotter.plot_xy_data(station_training_data, gefs_name, solar_output, "Solar output vs gefs")

def show_data_and_fit(gefs_data_set, gefs_name, station_info, solar_output_training_data, theta):
    prediction_of_training_data = get_prediction(theta, gefs_data_set, station_info)

    for stationID in range(0, 10):
        solar_output = solar_output_training_data.station_solar_output_data[:,stationID]
        plotter.plot_xy_data_with_fit(prediction_of_training_data[:,0], prediction_of_training_data[:,stationID+1], solar_output, gefs_name, "Solar with fit")