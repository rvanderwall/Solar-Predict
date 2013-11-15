__author__ = 'robertv'
from netCDF4 import Dataset
from scipy.io import netcdf
import matplotlib.pyplot as plt

#  Sample code to read and write CDF files

def createFile():
    # create a file (Dataset object, also the root group).
    rootgrp = Dataset('gefs_elevations.nc', 'w', format='NETCDF4')
    print(rootgrp.file_format)
    rootgrp.close()


def read_netcdf4(filename):
    f = Dataset(filename)
    print f.variables
    elevation_control = f.variables['elevation_control'][:]
    elevation_perturbation = f.variables['elevation_perturbation'][:]
    latitude = f.variables['latitude'][:]
    longitude = f.variables['longitude'][:]
    f.close()
    CS = plt.contour(longitude, latitude, elevation_control)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.show()

    for i in range(0,latitude.shape[0]):
        for j in range(0,latitude.shape[1]):
            print latitude[i,j], longitude[i,j]

def read_apcp_file():
    #'time', 'intTime', 'lat','lon','ens','fhour', 'intValidTime','Total_precipitation',
    f = Dataset("Data/train/apcp_sfc_latlon_subset_19940101_20071231.nc")
    time = f.variables['time']
    intTime = f.variables['intTime']
    lat = f.variables['lat']
    lon = f.variables['lon']
    ens = f.variables['ens']
    intValidTime = f.variables['intValidTime']
    total_precipitation = f.variables['Total_precipitation']
    print "done"

def read_dlwrf_file():
    #'time', 'intTime', 'lat','lon','ens','fhour', 'intValidTime','Total_precipitation',
    f = Dataset("Data/train/dlwrf_sfc_latlon_subset_19940101_20071231.nc")
    time = f.variables['time']
    intTime = f.variables['intTime']
    lat = f.variables['lat']
    lon = f.variables['lon']
    ens = f.variables['ens']
    intValidTime = f.variables['intValidTime']
    total_precipitation = f.variables['Downward_long_wave_rad_flux']
    print "done"

def read_netcdf3(filename):
    f = netcdf.netcdf_file(filename, 'r')
    print f.variables

#read_netcdf4("Data/gefs_elevations.nc")


read_apcp_file()
read_dlwrf_file()