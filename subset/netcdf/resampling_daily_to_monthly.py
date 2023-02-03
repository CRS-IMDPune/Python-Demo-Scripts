#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S##############
########## https://doi.org/10.5281/zenodo.5674826 ############

# 1. Read NetCDF file using xarray. 
# 2. Convert daily data to monthly averaged data
# 3. Calculating monthly climatology and anomaly
# 4. Subsetting data for the required time and lat/lon range.
# 5. Saving the data in a new nc file

import xarray as xr
import numpy as np
import pandas as pd

#######################Conversion of longitudes to 0-360 range######################
######################Since the data is in this range of longitudes#################
def lon_range(lon):
    if lon < 0:
        lon = lon+360
        return (lon)
    else:
        return (lon)

######################Define the required lat-lon range ##########################
lat1=-30.0
lat2=30.0
lon1=120.0
lon2=-90.0 

data=xr.open_dataset('Skin_Temp_Pacific_daily.nc')
data_sub=data.sel(time=slice('1950-01-01','2021-12-01'),lat=slice(lat2,lat1),lon=slice(lon_range(lon1),lon_range(lon2)))
#################Converting daily data to monthly mean##########################
monthly_data=data_sub.resample(time='M').mean()

###################Removing climatological mean#################################
data_anom=monthly_data.groupby('time.month')-data_sub.groupby('time.month').mean(dim='time')
data_anom

sst_range=data_anom.skt.sel(time=slice('1950-07-01','2020-12-31'),lat=slice(10,-10),lon=slice(200,250)).mean(dim=("lat","lon"))

#############################Write the averaged data over a band in an nc file##########################
sst_range.to_netcdf('Skin_Temp_anomaly_monthly_pacific.nc',mode='w')