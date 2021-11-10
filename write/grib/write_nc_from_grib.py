import xarray as xr
import datetime as Dt
import numpy as np
import netCDF4 as nc

ds=xr.open_dataset('/mnt/e/Python_Scripts/Sample_Data/ERA5_Temperature_2020.grib',engine='cfgrib',backend_kwargs={'indexpath':''})

#print(ds)		###Print summary of the file
#print(ds.t)		###Print summary of the variable
#print(ds.latitude)
#print(ds.longitude)
#print(ds.isobaricInhPa)
#print(ds.time)

temp=ds.t[:].values		## Read temperature in a variable
lats=ds.latitude[:].values
lons=ds.longitude[:].values
levs=ds.isobaricInhPa[:].values
time=ds.time[:].values

#################Subsetting the variable#############################

##############Subsetting over lat and lon dimension #################

latbounds = [ -15 , 15 ]	#degrees north
lonbounds = [ 70.5 , 100.5 ] 	# degrees east 
levbounds = [500.0 , 900.0 ]

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
levselect=np.logical_and(levs>=levbounds[0],levs<=levbounds[1])
temp_space1=temp[:,levselect,:,:][:,:,latselect,:][:,:,:,lonselect]
print(temp_space1)

##############Subsetting over time dimension ###############

dt1=Dt.datetime(2020,1,10,15,00,00)			## Give the required time
dt2=Dt.datetime(2020,1,11,15,00,00)				
def minutes_of_year(dt):				#### Defining a function to obtain 	
	return seconds_of_year(dt)//60			##hours_of_year from the datetime provided
	
def hours_of_year(dt):
	return minutes_of_year(dt)//60
	
def seconds_of_year(dt):
	dt0=Dt.datetime(dt.year,1,1,tzinfo=dt.tzinfo)
	delta=dt-dt0
	return int(delta.total_seconds())
			
ind1=hours_of_year(dt1)	###Using the function the hour is obtained which is the index
ind2=hours_of_year(dt2)
temp_time=temp[ind1:ind2+1,:,:,:][:,levselect,:,:][:,:,latselect,:][:,:,:,lonselect]		#Selecting data for a single time step
print(temp_time)

#####################Write a netCDF file#####################

fn='/mnt/e/Python_Demo_Scripts/write_files/grib/Sample_output1.nc'#Set path and name of output file
fout=nc.Dataset(fn,'w',format='NETCDF4')		#Open output file
time=fout.createDimension('time',None)			# Set all required dimensions	Time-Unlimited
Lats=fout.createDimension('lat',33)			#Choose size according to variable 
Lons=fout.createDimension('lon',115)
Levs=fout.createDimension('levels',2)
fout.subtitle="Level,Lat, Lon and Time subset"		#Setting some attributes
#fout.title=

lat=fout.createVariable('lat',np.float32,('lat',))	# Create variables and attributes
lat.units='degrees_north'
lat.long_name='latitude'
lon=fout.createVariable('lon',np.float32,('lon',))
lon.units='degrees_east'
lon.long_name='Longitude'
levels=fout.createVariable('levels',np.float32,('levels',))	# Create variables and attributes
levels.units='hPa'
levels.long_name='isobaricInhPa'
time=fout.createVariable('time',np.float32,('time',))
time.units='hours since 1800-01-01 00:00:0.0'
time.long_name='time'
time.calendar='standard'

t=fout.createVariable('t',np.float64,('time','levels','lat','lon'))
t.units='K'
t.standard_name='Air temperature at four levels'
t.dataset='ERA5 Reanalysis Air Temperature'
t.long_name='Hourly Air Temperature'

levels=levs[levselect]
lat[:]=lats[latselect]			# Giving values to the dimensions and variables
lon[:]=lons[lonselect]

######Setting time dimension and giving coordinates####################
	
dates=[Dt.datetime(2020,1,10,15,00,00)+n*Dt.timedelta(hours=1) for n in range(temp_time.shape[0])]
time[:]=nc.date2num(dates,units=time.units,calendar=time.calendar)	# Giving time coordinates

t[:,:,:,:]=temp_time		# Saving the variable in new file

print(t)
exit()
