###########Plotting a filled and line contour#########################
###########Import necessary modules##########################

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

############ File to be read ####################

file_name ='/mnt/d/DATA/ERA5/Wind/ERA5_Wind_2019.nc'

################# open file ######################

f = nc.Dataset(file_name)
print(f)                # gives us information about the variables 
                        #contained in the file and their dimensions
                      
for var in f.variables.values():
    print(var)          # Metadata for all variables

print(f['u10'])          # Metadata of single variable

################# read variables  ################

u10   = f.variables['u10'][:]
lats = f.variables['latitude'][:]
lons = f.variables['longitude'][:]
time = f.variables['time']		

#print(lons.min()," ,",lons.max())
#print(lats)
##############Subscripting over lat, lon and time###############

############Subsetting over time##############

st_date=dt.datetime(2019,6,1,0,0)	# Start date and hour
date=nc.num2date(time[:],units=time.units,calendar='standard')
istart=nc.date2index(st_date,time,calendar='standard',select='exact')


############Subsetting over lat and lon##############

latbounds = [ 7 , 15 ]	#degrees north
lonbounds = [ 70.5 , 100.5 ] 	# degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
u10sub=u10[:,latselect,:][:,:,lonselect]
U10SUB=u10sub[istart,:,:]
print(u10sub.max())
print(u10sub.shape)

###################Plotting ############################

ylist=lats[latselect]
xlist=lons[lonselect]
X,Y=np.meshgrid(xlist,ylist)

fig,ax=plt.subplots(1,1)
cp=ax.contourf(X,Y,U10SUB)	#cp=ax.contour(X,Y,U10SUB)	for Line contours
fig.colorbar(cp)
ax.set_title('U wind at 10m contour plot')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.savefig('contour1.png')	#plt.savefig('contour1_line.png')	
