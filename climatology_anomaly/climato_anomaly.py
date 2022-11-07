#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

############################READING A NETCDF4 FILE USING XARRAY######################################
##########################Import necessary Modules###################
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

##########Read the dataset using xarray##########################
filename="E:/Python_DEMO_Scripts/Sample_Data/_Clim_Pred*.nc"
da=xr.open_mfdataset(filename)
#print(da)

############Read the individual variables in the dataset########
rf=da.RAINFALL
lat=da.LATITUDE
lon=da.LONGITUDE
#print(lon)

######################Climatology and anomaly####################
da_climato=da.groupby("TIME.dayofyear").mean("TIME")
print(da_climato)

da_anom=da.groupby("TIME.dayofyear") - da.groupby("TIME.dayofyear").mean("TIME")
print(da_anom)

################Simple plotting with xarray#####################
da_anom.RAINFALL[182,:,:].plot(figsize=(12,8),levels=np.arange(-30,40,5))
plt.savefig("./climatology_anomaly/Anomaly_rainfall.png")

da_climato.RAINFALL[182,:,:].plot(figsize=(12,8),levels=np.arange(-30,40,5))
plt.savefig("./Climatology_anomaly/Climatology_rainfall.png")