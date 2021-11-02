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

##################Vector Plot Resources################

Lats=lats[latselect]
Lons=lons[lonselect]

plt.figure()
m = plt.axes(projection=ccrs.PlateCarree())
m.add_feature(cartopy.feature.BORDERS, edgecolor='black')
m.set_extent([lonbounds[0], lonbounds[1], latbounds[0], latbounds[1]], crs=ccrs.PlateCarree())
m.coastlines(resolution='110m')

gl=m.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,color='gray',linewidth=1.0)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

plt.suptitle('Wind Vector at 10 m from ERA5 (01/06/2019)')
plt.title('Wind (m/s)', loc='left')

q=m.quiver(Lons, Lats, U10SUB, V10SUB, width=0.003, scale_units='xy',scale=5, transform=ccrs.PlateCarree(),regrid_shape=20)
qk=plt.quiverkey (q,0.95, 1.02, 20, '20m/s', labelpos='N')
plt.savefig('vector_cartopy.png')

