########Plotting time series of rainfall at a particular location#############

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

latbounds = [ 7 , 30 ]	#degrees north
lonbounds = [ 70.5 , 99 ] 	# degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
u10sub=u10[:,latselect,:][:,:,lonselect]
U10SUB=u10sub[istart,:,:]
print(u10sub.max())
print(u10sub.shape)
print(U10SUB.shape)

###############Plotting Resources#####################

map = Basemap(projection='merc',llcrnrlon=70.5,llcrnrlat=7.,urcrnrlon=99,urcrnrlat=15.,lat_0=10.,lon_0=85.,resolution='l')

# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)
#map.fillcontinents(color='coral',lake_color='aqua')

# draw the edge of the map projection region (the projection limb)
#map.drawmapboundary(fill_color='aqua')

# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,3),labels=[1,0,0,1], fontsize=6)
map.drawparallels(np.arange(-90,90,2),labels=[1,0,0,1], fontsize=6)

# make up some data on a regular lat/lon grid.
Lats=lats[latselect]
Lons=lons[lonselect]
xx, yy = np.meshgrid(Lons, Lats)

# contour data over the map.
map.contourf(xx,yy,U10SUB,latlon=True,cmap='jet')
plt.xlabel('Longitude', labelpad=40, fontsize=8)
plt.ylabel('Latitude', labelpad=40, fontsize=8)

plt.colorbar(shrink=0.5)
plt.title('U wind at 10m')
plt.savefig('contour_map_basemap.png', dpi=100)
