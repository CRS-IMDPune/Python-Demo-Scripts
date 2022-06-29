#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#############
########## https://doi.org/10.5281/zenodo.5674826 ############

#####################Conversion of longitude values from 0 - 360 range to -180 -180 range and vice versa##########################
import xarray as xr
import numpy as np

#######################Defining a function for conversion of longitudes to 0-360 range given a longitude######################
def lon_range(lon):
    if lon < 0:
        lon = lon+360
        return (lon)
    else:
        return (lon)

test_lon=-90.0
print('After conversion '+str(test_lon)+'='+str(lon_range(test_lon)))

####################################Converting a dataset to  -180 to 180 longitude range#####################################
data=xr.open_dataset('S:/NOAA-COBE-SST/sst.mon.mean.nc')
print(data)

data.coords['lon'] = (data.coords['lon'] + 180) % 360 - 180
data = data.sortby(data.lon)
print('After conversion of whole data')
print(data)
