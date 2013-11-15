__author__ = 'robertv'

__author__ = 'robertv'

import csv
import numpy as np

field_delimiter=','
field_quote='"'

class StationInfo:
    """
    The Station Info file is a list of locations with the first row as the headers
    A row consists of a stid,nlat,elon,elev.
    """

    stations = np.array((1))
    elevations = np.array((1))
    station_latitudes = np.array((1))
    station_longitudes = np.array((1))

    def __init__(self, data_file):
        dt=np.dtype({'names':['station','lat','long', 'elevation'],'formats':['S100',np.float,np.float,np.float]})
        self.data = np.loadtxt(open(data_file,"rb"),
                               dtype=dt,
                               delimiter=",",skiprows=1)
        self.stations = np.array(self.data['station'])
        self.elevations = np.array(self.data['elevation'])
        self.station_latitudes = np.array(self.data['lat'])
        self.station_longitudes = np.array(self.data['long'])


    def get_translation(self, station_index, latitudes, longitudes):
        latitude = self.station_latitudes[station_index]
        longitude = self.station_longitudes[station_index]

        l,r,b,t = self.get_lat_lon_indexes(latitude, longitude, latitudes, longitudes)
        gap_u_l = latitudes[r] - latitudes[l]
        P_l = (latitude - latitudes[l])/gap_u_l
        P_r = 1 - P_l

        gap_t_b = longitudes[t] - longitudes[b]
        P_b = (longitude - longitudes[b])/gap_t_b
        P_t = 1 - P_b

        return ((l,b), (l,t), (r,b), (r,t)), \
               (P_l*P_b, P_l*P_t, P_r*P_b, P_r*P_t)

    def get_lat_lon_indexes(self, latitude_to_find, longitude_to_find, latitudes, longitudes):
        """
            Find the bounding indexes for a given position
        @param data:
        @param lat:
        @param long:
        """
        assert latitude_to_find > latitudes[0]
        assert latitude_to_find < latitudes[-1]
        assert longitude_to_find > longitudes[0]
        assert longitude_to_find < longitudes[-1]

        left_lat_index = 0
        right_lat_index = 0
        for lat_index in range(0, latitudes.shape[0]):
            if latitudes[lat_index] >= latitude_to_find:
                right_lat_index = lat_index
                left_lat_index = lat_index - 1
                break

        # Longitudes are around -90, so loop the other way.
        top_long_index = 0
        bottom_long_index = 0
        for long_index in range(0, longitudes.shape[0]):
            if longitudes[long_index] >= longitude_to_find:
                bottom_long_index = long_index
                top_long_index = long_index - 1
                break

        return left_lat_index, right_lat_index, top_long_index, bottom_long_index
