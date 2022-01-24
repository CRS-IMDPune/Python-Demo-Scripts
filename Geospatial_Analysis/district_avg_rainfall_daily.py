###################Calculating state average of a variable and plotting using shape file#######
import geopandas as gpd
import regionmask 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import netCDF4 as nc
import datetime as dt
import pandas as pd

#####################read the rainfall data file needed to plot###############################
f1_name='/mnt/rc/IMD_rainfall_0.25/_Clim_Pred_LRF_New_RF25_IMD0p252020.nc'
f1 = nc.Dataset(f1_name)
for var in f1.variables.values():
    print(var)                                                       # Print Metadata for all variables

lats = f1.variables['LATITUDE'][:]
lons = f1.variables['LONGITUDE'][:]
time = f1.variables['TIME']

lat_size=len(lats)
lon_size=len(lons)

####################################Subsetting over time#####################################
st_date=dt.datetime(2020,7,15,0,0)                                   #Give necessary day here
iday=nc.date2index(st_date,time,calendar='standard',select='exact')  #Gives us index of necessary day

rf_day=f1.variables['RAINFALL'][iday,:,:]     # Reading for required day and lat lon range

#########################Read the shape file and create masks###############################
fname='/mnt/rc/All Shape File/Kerala district shape file/Kerala districtshape file.shp'           # District shapefile of kerala
shp=gpd.read_file(fname)
print(shp['DISTRICT_1'])
dist_name=list(shp['DISTRICT_1'])
dist_1=list(shp['DISTRICT_1'])
indexes=[dist_name.index(x) for x in dist_1]                             # Obtain district indexes

dist1=regionmask.Regions(outlines=list(shp.geometry.values[i] for i in range(0, shp.shape[0])), names=shp.DISTRICT_1[indexes],abbrevs=shp.DISTRICT_1[indexes],name='district', )   # Obtaining region boundaries
dist1_mask=dist1.mask(lons,lats)                                           # State mask variable

##########################Create an array and store all district average values################
dist_rf_all=np.empty(dist_1.shape[0])
for i in range(0,shp.shape[0]):              
    result=np.where(dist1_mask==i)
    lat_ind=result[0]
    lon_ind=result[1]
    rf_dist=np.mean((rf_day[lat_ind,:][:,lon_ind]),axis=(0,1))
    dist_rf_all[i]=rf_dist
    del rf_dist
print(dist_rf_all)

#################Create a merged geodataframe with values and geometry#########################    
d={'ID':list(shp['ID']),'Rainfall':dist_rf_all}     #Create a rainfall datatframe
data_f=pd.DataFrame(data=d)

df_merged = shp.merge(data_f, left_on='ID', right_on='ID') #Merge it with shapefile to create geodataframe to plot

####################################Plot Settings#############################################
date_string=st_date.strftime("%d/%m/%y")
fig, ax = plt.subplots(1, figsize=(10,12))
df_merged.plot(column='Rainfall',cmap='tab20b_r', linewidth=1, ax=ax, edgecolor='0.9', legend = True) 
ax.axis('off')
fig.suptitle('Rainfall(mm)',fontsize=25)
ax.set_title(date_string, fontsize=18, loc='Left')

#####################Giving labels to each district##########################################
df_merged['coords'] = df_merged['geometry'].apply(lambda x: x.representative_point().coords[:])
df_merged['coords'] = [coords[0] for coords in df_merged['coords']]
for idx, row in df_merged.iterrows():
    plt.annotate(s=row['DISTRICT_1'], xy=row['coords'],horizontalalignment='center')     # To give name of district
    #plt.annotate(s=row['Rainfall'], xy=row['coords'],horizontalalignment='center')       # To give value of district average rainfall
    
#################################Save the figure############################################
plt.savefig('district_avg_rainfall_daily.png')
