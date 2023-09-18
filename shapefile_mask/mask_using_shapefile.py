#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

###################Masking a data using shapefile########################

###############Import necessary Modules#################
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
from cartopy.io.shapereader import Reader
import geopandas as gpd
import shapely.vectorized
from shapely.ops import unary_union

######################Read the data###############################
da=xr.open_dataset('/mnt/e/Python_Demo_Scripts/Sample_Data/ncum_imdaa_reanl_DY_RH-2m_20200101-20201231.nc')
print(da)

###############Subset the data for any day, lat and lon range############
rh=da.RH_2m.sel(time='2020-06-15',latitude=slice(0,40),longitude=slice(60,120))
print(rh)

###############Prepare the mask from the shapefile#######################
fname='/mnt/S/All Shape File/India outline boundary/India outline boundary.shp'           # Read the shapefile of India
shp=gpd.read_file(fname)

boundary = unary_union(shp[shp['GADMID']=='0']["geometry"])                     # Create the boundary for the Indian landmass
#print(boundary)

lats=rh.latitude.values                                       # Read the latitude and longitude of actual data to be masked
lons=rh.longitude.values
xx, yy = np.meshgrid(lons, lats)
mask = shapely.vectorized.contains(boundary, xx, yy)      # Prepare the mask by checking whether the point lies inside or outside the boundary
rh_mask=np.where(mask,rh.squeeze(),np.nan)                # Using the mask created, mask the actual data
print(rh_mask)

#####################Plot the data before and after masking####################
fig=plt.figure(figsize=(12,10))
ax=plt.subplot(2,2,1)
m=ax.contourf(lons,lats,rh.squeeze(),levels=np.arange(0,110,10))    # Before masking
ax.set_title('Without Masking')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

ax1=plt.subplot(2,2,2)
ax1.contourf(lons,lats,rh_mask,levels=np.arange(0,110,10))          # After masking
ax1.set_title('With Masking')  
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
plt.colorbar(m)
plt.tight_layout()

plt.savefig('Masking_with_shapefile.png',facecolor='white')         # Save the plot
