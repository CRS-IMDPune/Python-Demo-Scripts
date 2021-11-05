###########Import necessary modules##########################

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

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
lonbounds = [ 66.5 , 99 ] 	# degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
u10sub=u10[:,latselect,:][:,:,lonselect]
U10SUB=u10sub[istart,:,:]

#############Plot Resources#######################

Lats=lats[latselect]
Lons=lons[lonselect]

m = plt.axes(projection=ccrs.PlateCarree())
m.set_extent([lonbounds[0], lonbounds[1], latbounds[0], latbounds[1]], crs=ccrs.PlateCarree())
m.coastlines(resolution='110m')
m.add_feature(cartopy.feature.COASTLINE, edgecolor='black')

gl=m.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,color='gray',linewidth=1.0)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

c= m.contourf(Lons, Lats, U10SUB, transform=ccrs.PlateCarree(),cmap='jet')
plt.suptitle('U Wind at 10 m from ERA5 on 01/06/2019')
plt.title('Wind (m/s)', loc='right')
plt.colorbar(c,shrink=0.75)
plt.savefig('contour_map_cartopy.png')

exit()
