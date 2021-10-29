import xarray as xr

ds=xr.open_mfdataset('/mnt/e/Python_Scripts/Sample_Data/ERA5_Temperature_*.grib',engine='cfgrib',backend_kwargs={'indexpath':''})

ds1=xr.open_mfdataset('/mnt/e/Python_Scripts/Sample_Data/ERA5_Temperature_*.grib',engine='cfgrib',backend_kwargs={'indexpath':''})
print(ds)		###Print summary of the file
#print(ds.t)		###Print summary of the variable
#print(ds.latitude)
#print(ds.longitude)
#print(ds.isobaricInhPa)
temp=ds.t		## Read temperature in a variable
print(temp)
exit()
