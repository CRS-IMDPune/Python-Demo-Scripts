#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############


import xarray as xr
data="S:/IMD_rainfall_0.25/_Clim_Pred_LRF_New_RF25_IMD0p252020.nc"

############Open the dataset##################
da=xr.open_dataset(data)
print(da)

##############Subset the whole dataset for the required time, lat and lon###############
date='2020-06-15'
lat=18.0
lon=75.0

#METHOD 1
########Using sel function in xarray######################
#########Give the actual coordinate required##############
da_sub=da.sel(TIME=date,LATITUDE=lat,LONGITUDE=lon)       #TIME,LATITUDE,LONGITUDE are the dimension names in file
print(da_sub)

#METHOD 2
##################Using isel function in xarray######################
#########Give the index of the actual coordinate required##############
da_sub1=da.isel(TIME=166,LATITUDE=46,LONGITUDE=34)       #TIME,LATITUDE,LONGITUDE are the dimension names in file
print(da_sub1)