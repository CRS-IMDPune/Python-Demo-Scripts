###########Import necessary modules##########################

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from mpl_toolkits.basemap import Basemap

############ File to be read ####################
############ IMD Gridded Rainfall data ##########

file_name  = filename='/mnt/d/DATA/ERA5/Wind/ERA5_Wind_2019.nc'

################# open file ######################

f = nc.Dataset(file_name)
print(f)                # gives us information about the variables 
                        #contained in the file and their dimensions
                      
for var in f.variables.values():
    print(var)          # Metadata for all variables

print(f['u10'])          # Metadata of single variable

################# read variables  ################

u10   = f.variables['u10'][:]
v10   = f.variables['v10'][:]
lats = f.variables['latitude'][:]
lons = f.variables['longitude'][:]
time = f.variables['time']		# In the file for the time dimension year has been set as 2010 in all year files

#print(lons.min()," ,",lons.max())
#print(lats)
##############Subscripting over lat, lon and time###############

############Subsetting over time##############

st_date=dt.datetime(2019,6,1,0,0)	# Start date and hour
date=nc.num2date(time[:],units=time.units,calendar='standard')
istart=nc.date2index(st_date,time,calendar='standard',select='exact')


############Subsetting over lat and lon##############

latbounds = [ 7 , 25 ]	#degrees north
lonbounds = [ 70.5 , 90.5 ] 	# degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])

u10sub=u10[:,latselect,:][:,:,lonselect]
U10SUB=u10sub[istart,:,:]

v10sub=u10[:,latselect,:][:,:,lonselect]
V10SUB=u10sub[istart,:,:]

print(u10sub.max())
print(u10sub.shape)

#############Start Plot###########################################

##Create the basemap instance and define basemap plot attributes

map = Basemap(projection = 'cyl',llcrnrlat=latbounds[0],urcrnrlat=latbounds[1],\
llcrnrlon=lonbounds[0],urcrnrlon=lonbounds[1],lat_0=15.,lon_0=80.,resolution='l')
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)

# draw lat/lon grid lines every 3 and 2 degrees.
map.drawmeridians(np.arange(0,360,3),labels=[1,0,0,1], fontsize=6)
map.drawparallels(np.arange(-90,90,2),labels=[1,0,0,1], fontsize=6)

# make up some data on a regular lat/lon grid.
Lats=lats[latselect]
Lons=lons[lonselect]
xx, yy = np.meshgrid(Lons, Lats)
x,y=map(xx,yy)

### Plot contourfills###############################################

c= map.contourf(x, y, U10SUB,latlon=True,)

##Now overlay Plot vector

skip=(slice(None,None,4),slice(None,None,4))	##Since data is high reslution plotting vector every fourth point in grid
q=map.quiver(x[skip], y[skip], U10SUB[skip], V10SUB[skip], width=0.003, scale_units='xy',scale=5)  
qk= plt.quiverkey (q,0.95, 1.02, 20, '20m/s', labelpos='N')

####Define the plot properties#######################################

plt.colorbar(c)
plt.suptitle('ERA5 Wind Vector over U wind at 10 m (01/06/2019)')
plt.title('Wind (m/s)', loc='left')
#plt.xlabel('Lon')
#plt.ylabel('Lat')
plt.savefig('vector_overlay_basemap.png')
exit()
