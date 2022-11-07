#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

############################READING A NETCDF4 FILE USING XARRAY######################################
##########################Import necessary Modules###################
import xarray as xr

##########Read the dataset using xarray##########################
filename="E:/Python_DEMO_Scripts/Sample_Data/_Clim_Pred*.nc"
da=xr.open_mfdataset(filename)
print(da)

############Read the individual variables in the dataset########
rf=da.RAINFALL
lat=da.LATITUDE
lon=da.LONGITUDE
print(lon)