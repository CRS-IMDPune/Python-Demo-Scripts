################Write an nc file reading data from a binary file########################
###############Reading IMD binary (GRD) data for Maximum temperature###############

import numpy as np
import datetime as dt
import netCDF4 as nc

filename='/mnt/e/Python_Scripts/Sample_Data/Maxtemp_MaxT_2018.GRD'	#File 

nlat=31			# Obtained from the ctl file
nlon=31
ntime=365

#######Method 1 to define lat-lon range################

lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
#print(lons)
lats=np.arange(7.5,38.5,1)
#print(lats)

###########Method2 to define lat-lon range#############

lat_min=7.5
lon_min=67.5
lat_max=37.5
lon_max=97.5
nlat=31
nlon=31
lat=np.linspace(lat_min, lat_max, num=nlat,endpoint=False)	
lon=np.linspace(lon_min, lon_max, num=nlon,endpoint=False)

####################Read the file#####################
f=open(filename,'rb')
data=np.fromfile(f,dtype="float32",count=-1)	# Opening and reading the file into a one dimensional array
print(data, len(data))		#length of data
print(data.min())		# minimum value
print(data.max())		# maximum value

################Reshaping data######################

temp=np.reshape(data,(365,31,31),order='C')
print(temp.shape)
print(temp.min())
#print(temp[50,:,:])

###############Subsetting lat-lon range#############

latbounds = [ 10 , 30 ]
lonbounds = [ 70.5 , 90.5 ] # degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
print(latselect)

tempsub1=temp[:,latselect,:][:,:,lonselect]		# Subsetting lat lon range
print(tempsub1.shape)
#print(tempsub1)

tempsub2=tempsub1[0:10,:,:]		# Subsetting days using day number of a year (here 2018)
print(tempsub2.shape)

#####################Write a netCDF file#####################

fn='/mnt/e/Python_DEMO_Scripts/write_files/binary/sample_subset.nc'	#Set path and name of output file
fout=nc.Dataset(fn,'w',format='NETCDF4')		#Open output file
time=fout.createDimension('time',None)			# Set all required dimensions	Time-Unlimited
Lats=fout.createDimension('lat',20)			
Lons=fout.createDimension('lon',21)
fout.title="Subset of IMD Max. Temperature Data"	#Setting some attributes
fout.subtitle="Lat, Lon and Time subset"

lat=fout.createVariable('lat',np.float32,('lat',))	# Create variables and attributes
lat.units='degrees_north'
lat.long_name='latitude'
lon=fout.createVariable('lon',np.float32,('lon',))
lon.units='degrees_east'
lon.long_name='Longitude'
time=fout.createVariable('time',np.float64,('time',))
time.units='hours since 1800-01-01 00:00:0.0'
time.long_name='time'
time.calendar='standard'

max_temp=fout.createVariable('max_temp',np.float64,('time','lat','lon'))
max_temp.units='degrees Celsius'
max_temp.standard_name='Daily Maximum Temperature'
max_temp.dataset='IMD Maximum Temperature 2018'
max_temp.long_name='Daily Data'

lat[:]=lats[latselect]		# Giving values to the dimensions and variables
lon[:]=lons[lonselect]

	######Setting time dimension and giving coordinates####################
	
dates=dt.datetime(2018,1,1)+n*dt.timedelta(hours=24) for n in range(temp.shape[0])
time[:]=nc.date2num(dates,units=time.units,calendar=time.calendar)
max_temp[:,:,:]=tempsub1

print(max_temp)
exit()
