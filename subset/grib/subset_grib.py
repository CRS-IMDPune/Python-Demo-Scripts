import xarray as xr
import datetime 
import numpy as np

ds=xr.open_dataset('/mnt/e/Python_Scripts/Sample_Data/ERA5_Temperature_2020.grib',engine='cfgrib',backend_kwargs={'indexpath':''})

#print(ds)		###Print summary of the file
#print(ds.t)		###Print summary of the variable
#print(ds.latitude)
#print(ds.longitude)
#print(ds.isobaricInhPa)
#print(ds.time)
temp=ds.t		## Read temperature in a variable
lats=ds.latitude[:]
lons=ds.longitude[:]
levs=ds.isobaricInhPa[:]

#################Subsetting the variable#############################

#############Subsetting over Level, Lat and Lon dimension (METHOD1)#############

temp_lev1=temp.sel(isobaricInhPa=[850])		###Subset over required level
temp_lev2=temp.sel(isobaricInhPa=[850,200])		###Subset over multiple levels
#print(temp_lev2)

temp_lat1=temp.sel(latitude=[38.0])			####Subset over single latitude 
temp_lat2=temp.sel(latitude=[38.0,28.0])		####Subset over multiple latitude 
#print(temp_lat1)

temp_lon1=temp.sel(longitude=[98.0])			####Subset over single longitude 
temp_lon2=temp.sel(longitude=[80.0,98.0])		####Subset over multiple longitude 
#print(temp_lon2)

##############Subsetting over lat and lon dimension (METHOD 2)#################

latbounds = [ -15 , 15 ]	#degrees north
lonbounds = [ 70.5 , 100.5 ] 	# degrees east 
levbounds = [500.0 , 900.0 ]
latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
levselect=np.logical_and(levs>=levbounds[0],levs<=levbounds[1])
temp_space1=temp[:,levselect,latselect,lonselect]
print(temp_space1)

##############Subsetting over time dimension (METHOD 1)###############

temp_time=temp.loc['2020-01-01T00:00:00':'2020-01-02T05:00:00',:,:,:]
print(temp_time)

##############Subsetting over time dimension (METHOD 2)###############

dt=datetime.datetime(2020,1,10,15,00,00)		## Give the required time
					
def minutes_of_year(dt):				#### Defining a function to obtain 	
	return seconds_of_year(dt)//60			##hours_of_year from the datetime provided
	
def hours_of_year(dt):
	return minutes_of_year(dt)//60
	
def seconds_of_year(dt):
	dt0=datetime.datetime(dt.year,1,1,tzinfo=dt.tzinfo)
	delta=dt-dt0
	return int(delta.total_seconds())
			
ind1=hours_of_year(dt)			###Using the function the hour is obtained which is the index
temp_time1=temp[ind1,:,:,:]		#Selecting data for a single time step
#print(temp_time1)

exit()
