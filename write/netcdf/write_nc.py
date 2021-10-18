##################Read a netcdf file#########################

###########Import necessary modules##########################

import netCDF4 as nc
import numpy as np
import datetime as dt

############ File to be read ####################
############ IMD Gridded Rainfall data ##########

file_name  = "/mnt/e/Python_Scripts/Sample_Data/olr.day.mean.nc"

################# open file ######################

f = nc.Dataset(file_name)
print(f)                # gives us information about the variables 
                        #contained in the file and their dimensions
                        
for dim in f.dimensions.values():
    print(dim)          # Metadata for all dimensions
    
for var in f.variables.values():
    print(var)          # Metadata for all variables

print(f['olr'])          # Metadata of single variable

################# read variables  ################

olr   = f.variables['olr'][:]
lats = f.variables['lat'][:]
lons = f.variables['lon'][:]
time = f.variables['time']
Time = f.variables['time'][:]
#print(time)
print(olr.min()," ,",olr.max())

################Subsetting over lat, lon and time####################
############Subsetting over time##############

st_date=dt.datetime(2010,1,10,0,0)		#Give the required time step here-Start
en_date=dt.datetime(2010,2,10,0,0)		# End date and hour
date=nc.num2date(time[:],units=time.units,calendar='standard')

istart=nc.date2index(st_date,time,calendar='standard',select='exact')
iend=nc.date2index(en_date,time,calendar='standard',select='exact')

###########Subsetting over lat and lon##########

latbounds = [ -15 , 15 ]
lonbounds = [ 70.5 , 100.5 ] # degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])

olrsub1=f.variables['olr'][istart:iend+1,latselect,lonselect]	#End date+1 gives upto the required date

print(olrsub1.max())
print(olrsub1.shape)
del olr

#####################Write a netCDF file#####################

fn='/mnt/e/Python_Scripts/DEMO/olr_subsets.nc'		#Set path and name of output file
fout=nc.Dataset(fn,'w',format='NETCDF4')		#Open output file
time=fout.createDimension('time',None)			# Set all required dimensions	Time-Unlimited
Lats=fout.createDimension('lat',13)			
Lons=fout.createDimension('lon',12)
fout.title="Subset of NOAA OLR Data"			#Setting some attributes
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

olr=fout.createVariable('olr',np.float64,('time','lat','lon'))
olr.units='W/m^2'
olr.standard_name='Outgoing Longwave Radiation'
olr.dataset='NOAA Interpolated OLR'
olr.long_name='Daily OLR'

lat[:]=lats[latselect]			# Giving values to the dimensions and variables
lon[:]=lons[lonselect]
time[:]=Time[istart:iend+1]
olr[:,:,:]=olrsub1

print(olr)

exit()
