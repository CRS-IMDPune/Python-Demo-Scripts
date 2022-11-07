#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

############################READING A NETCDF4 FILE USING XARRAY######################################
##########################Import necessary Modules###################
import xarray as xr

##########Read the dataset using xarray##########################
filename="E:/Python_DEMO_Scripts/Sample_Data/_Clim_Pred*.nc"
da=xr.open_mfdataset(filename)
#print(da)

############Read the individual variables in the dataset########
rf=da.RAINFALL
lat=da.LATITUDE
lon=da.LONGITUDE
#print(lon)

################ Subsetting in all dimensions###################
da1=da.sel(TIME=slice('2019-11-01','2020-03-31'),LATITUDE=slice(7.5,20.5),LONGITUDE=slice(68.0,90.5))
#print(da1)

#####################Choosing a few months######################
mamj = da.TIME.dt.month.isin(range(3, 7))       #Reading March-June
da2=da.sel(TIME=mamj)
#print(da2)

##########Choosing pre-defined seasons in xarray using groupby#########
da3=da.groupby("TIME.season")["MAM"]        #Choosing MAM
#print(da3)

da4=da.groupby("TIME.season")["MAM"].mean(dim="TIME")   #Calculating Seasonal Mean
print(da4)
