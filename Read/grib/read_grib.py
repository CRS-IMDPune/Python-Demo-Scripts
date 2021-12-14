#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

#######READ A GRIB FILE###########################
#########Import necessary modules##################
import xarray as xr

#############Load the dataset######################
ds=xr.open_dataset('/mnt/e/Python_Scripts/Sample_Data/ERA5_Temperature_2020.grib',engine='cfgrib',backend_kwargs={'indexpath':''})

print(ds)		###Print summary of the file
print(ds.t)		###Print summary of the variable
print(ds.latitude)
print(ds.longitude)
print(ds.isobaricInhPa)
temp=ds.t		## Read temperature in a variable
print(temp)
exit()
