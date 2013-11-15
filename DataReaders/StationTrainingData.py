__author__ = 'robertv'

import csv
import numpy as np
from src.Helpers import station_lists_are_same


field_delimiter=','
field_quote='"'

class StationTrainingData:
    """
    The training file is a list of readings with the first row as the headers
    A row consists of a date and a reading for a station, the header has the name of the station
    the first column is the date.
    """

    _data_file = ""
    _raw_data = np.array((1))

    dates = np.array((1))
    station_solar_output_data = np.array((1))
    station_info = None

    def __init__(self, data_file, station_info):
        self._data_file = data_file
        self.station_info = station_info
        self._read_data()

    def _read_data(self):
        with open(self._data_file, 'r') as training_file:
            training_file_reader = csv.reader(training_file, delimiter=field_delimiter, quotechar=field_quote)
            header = training_file_reader.next()
            stations = np.array(header[1:])
            assert station_lists_are_same(stations, self.station_info.stations)

        self._raw_data = np.loadtxt(open(self._data_file,"rb"),delimiter=",",skiprows=1)

        self.station_solar_output_data = np.array(self._raw_data[:,1:])
        self.dates = np.array(self._raw_data[:,0]).astype(np.int)


    def solar_output_for_station(self, stationIndex):
        return self.station_solar_output_data[:, stationIndex]


    def average_solar_output_for_station(self, stationIndex):
        return np.average(self.station_solar_output_data[:,stationIndex])

    def position_for_station(self, stationIndex):
        return self.station_info.station_latitudes[stationIndex], self.station_info.station_longitudes[stationIndex]

    def cost(self, prediction_data):
        """
        Cost is the MAE - mean absolute error
        sum over all stations, sum over all dates
        of absolute value of difference
        @param prediction_data:
        @return:
        """
        num_stations = self.station_solar_output_data.shape[1]
        num_dates = self.station_solar_output_data.shape[0]
        error = np.subtract(self.station_solar_output_data, prediction_data)
        error = np.abs(error)
        err_sum = np.sum(error)
        cost = 1.0 * err_sum / (num_dates * num_stations)
        return cost
