__author__ = 'robertv'

from netCDF4 import Dataset
import numpy as np

def get_gefs_data(var_alias, var_type, var_name):
    gefs_training_file = "Data/train/" + var_alias + "_" + var_type + "_latlon_subset_19940101_20071231.nc"
    gefs_test_file = "Data/test/" + var_alias + "_" + var_type + "_latlon_subset_20080101_20121130.nc"
    values_training_data = GEFS_Variable(gefs_training_file, var_name, var_alias)
    values_test_data = GEFS_Variable(gefs_test_file, var_name, var_alias)
    return values_training_data, values_test_data

class GEFS_Variable:

    dates = np.array((1))
    data = np.array((1))
    latitudes = np.array((1))
    longitudes = np.array((1))
    alias = ""
    name = ""

    def __init__(self, datafile, name, alias):
        self.name = name
        self.alias = alias

        if datafile != None:
            self.read_netcdf4(datafile, name)

    def read_netcdf4(self, filename, variable_name):
        """
            intTime: array of timestamps intTime[0]=yyyymmdd00   shape=(5113,)
            intValidTime: array of list of timestamps intValitTime[0]=[yyyymmdd12 yyyymmdd15 *18 *21 *00] shape=(5113,5)
            time: array of hours since epoch   time[0]=1700568.0 shape=(5113,)
            ens: ensemble number shape=(11,)
            lat: latitude lat[0]=31.0 shape=(9,)
            lon: longitude lon[0]=254 shape=(16,)
            variable: measurement  shape=(5113, 11, 5, 9, 16)
                 for each time(day) , ensemble, timeOfDay, lat, lon
        @param filename:
        @param variable_name:
        """
        f = Dataset(filename, 'r')
        ens = f.variables['ens']
        fHour = f.variables['fhour']
        intTime = f.variables['intTime']
        intValidTime = f.variables['intValidTime']
        time = f.variables['time']

        self.latitudes = f.variables['lat'][:]
        self.longitudes = f.variables['lon'][:] - 360 # These are degrees from Prime Meridian in file, convert to long
        gefs_variable = f.variables[variable_name]

        self.data = gefs_variable[:]
        #self.dates = intTime[:].astype('|S8')
        # only want yyyymmdd, so divide by 100 to get rid of hour
        self.dates = np.divide(intTime[:], 100)
        f.close()

