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
#print(time)
print(olr.min()," ,",olr.max())

################Subscripting over lat, lon and time####################
############Subsetting over time##############

st_date=dt.datetime(2010,1,10,0,0)		#Give the required time step here-Start
en_date=dt.datetime(2010,2,10,0,0)		# End date and hour
date=nc.num2date(time[:],units=time.units,calendar='standard')

istart=nc.date2index(st_date,time,calendar='standard',select='exact')
iend=nc.date2index(en_date,time,calendar='standard',select='exact')


latbounds = [ -15 , 15 ]
lonbounds = [ 70.5 , 100.5 ] # degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])

olrsub1=f.variables['olr'][istart:iend,latselect,lonselect]
print(olrsub1.max())
print(olrsub1.shape)


ind_lat = [i for i, val in enumerate(latselect) if val]	;To find the index of true values
ind_lon = [i for i, val in enumerate(lonselect) if val]

olrsub2=f.variables['olr'][istart:iend,ind_lat,ind_lon]
print(olrsub2.max())
print(olrsub2.shape)
exit()
