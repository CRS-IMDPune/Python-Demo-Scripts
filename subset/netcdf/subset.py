##################Read a netcdf file#########################

###########Import necessary modules##########################

import netCDF4 as nc
import datetime as dt
import numpy as np

############ File to be read ####################
############ IMD Gridded Rainfall data ##########

file_name  = "/mnt/e/Python_Scripts/Sample_Data/RFone_imd_rf_1x1_2019.nc"

################# open file ######################

f = nc.Dataset(file_name)
print(f)                # gives us information about the variables 
                        #contained in the file and their dimensions
                        
for dim in f.dimensions.values():
    print(dim)          # Metadata for all dimensions
    
for var in f.variables.values():
    print(var)          # Metadata for all variables

print(f['rf'])          # Metadata of single variable

################# read variables  ################

rf   = f.variables['rf'][:]
lats = f.variables['lat'][:]
lons = f.variables['lon'][:]
time = f.variables['time']		# In the file for the time dimension year has been set as 2010 in all year files

print(lons.min()," ,",lons.max())

################Subscripting over lat, lon and time####################

############Subsetting over time##############

st_date=dt.datetime(2010,1,10,0,0)	#Giving 2010 as year only applicable for IMD rainfall files
					#Give the required time step here
en_date=dt.datetime(2010,2,10,0,0)	# End date and hour
date=nc.num2date(time[:],units=time.units,calendar='standard')

istart=nc.date2index(st_date,time,calendar='standard',select='exact')
iend=nc.date2index(en_date,time,calendar='standard',select='exact')

############Subsetting over lat and lon##############

latbounds = [ 10 , 20 ]
lonbounds = [ 70.5 , 90.5 ] # degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])

rfsub1=f.variables['rf'][istart:iend,latselect,lonselect]
print(rfsub1.max())
print(rfsub1.shape)

exit()

