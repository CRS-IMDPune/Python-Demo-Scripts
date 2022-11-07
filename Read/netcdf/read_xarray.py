#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

############################READING A NETCDF4 FILE USING XARRAY######################################
##########################Import necessary Modules###################
import xarray as xr

##########Read the dataset using xarray##########################
filename="E:/Python_DEMO_Scripts/Sample_Data/2020_1x1_rain.nc"
da=xr.open_dataset(filename)
print(da)

############Read the individual variables in the dataset########
rf=da.rf
lat=da.lat
lon=da.lon
print(lon)