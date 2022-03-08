###################Calculating area-weighted cumulative rainfall for districts at any month in a year and plotting it##################
import geopandas as gpd
import regionmask 
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import datetime as dt
import pandas as pd
import xarray as xr
import matplotlib.patheffects as pe

###################################Specify year and seaon needed##############################
year =2018                             # Give the year
f1_name='/mnt/rc/IMD_rainfall_0.25/_Clim_Pred_LRF_New_RF25_IMD0p252018.nc'    #Give the year filename
month_no=7                                                    # Give the month number 1-January etc.. to calculate total monthly rainfall

fname='/mnt/rc/All Shape File/Kerala district shape file/Kerala districtshape file.shp'           # District shapefile of kerala
data = pd.read_csv('Grid_District_Contribution.csv')                                              # Load the percent mask file

####Label Bar Settings
label_cbar= "Area-weighted monthly district rainfall (mm)"               # Give the label for colorbar

img_name='dist_cumulative_areaweighted_mnthly_rf.png'                # Give the name for saving the image

####Annotation Color
annot_color='yellow'                                                   # Color for annotation of district name in plot

#####Colorbar for plot
cmap='tab20b_r'                                                          # Specify the colorbar for plot

#######################No need to edit below##################################################
#####################read the rainfall data file needed to plot###############################
f1 = nc.Dataset(f1_name)
rf_fill=f1.variables['RAINFALL']

ds = xr.open_dataset(f1_name)
lats=ds.LATITUDE[:]
lons=ds.LONGITUDE[:]

######################Resample the daily data into monthly mean data##########################
monthly_data=ds.resample(TIME='M').sum()
rf_month=monthly_data.RAINFALL[:]               #Read the rainfall variable from monthly data
                                     
rf_mon=rf_month[month_no-1,:,:]     # Reading for required month (numbering starts from 0, so month_no-1)

#########################Read the shape file and create masks###############################
shp=gpd.read_file(fname)

dist_name=list(shp['DISTRICT_1'])
dist_1=list(shp['DISTRICT_1'])
indexes=[dist_name.index(x) for x in dist_1]                             # Obtain district indexes

dist1=regionmask.Regions(outlines=list(shp.geometry.values[i] for i in range(0, shp.shape[0])), names=shp.DISTRICT_1[indexes],abbrevs=shp.DISTRICT_1[indexes],name='district', )   # Obtaining region boundaries
dist1_mask=dist1.mask(lons,lats)                                           # State mask variable

#######################Read the percentage mask file#################################
district=data['District'][:]
lat=data['Grid Lat'][:]
lon=data['Grid Lon'][:]
percent=data['Percent contribution'][:]

#######################Calculate the district area averaged rainfall for a day########
lats=np.reshape(ds.LATITUDE.values, (1, -1))
lons=np.reshape(ds.LONGITUDE.values, (1, -1))

Dist_avg_rf=np.full(len(dist_1),rf_fill._FillValue, order='C')

for i in range(0,len(dist_1)):
    lat_percent=(lat[dist_name[i] == district]).tolist()
    lon_percent=(lon[dist_name[i] == district]).tolist()
    percent_mask=(percent[dist_name[i] == district]).tolist()
    
    Total=0.0
    Total_weight=0.0
    #print(dist_name[i])
    for j in range (0, len(lat_percent)):
        ind_lat_rf=np.where(lats == lat_percent[j])
        ind_lon_rf=np.where(lons == lon_percent[j])
        Total=Total+rf_mon[ind_lat_rf,ind_lon_rf]*percent_mask[j]
        Total_weight= Total_weight+ percent_mask[j]
        #print(Total, "   ",percent_mask[j])
        
    Dist_avg_rf[i]=Total/Total_weight
    del Total
    del lat_percent
    del lon_percent
    del percent_mask
    
print(Dist_avg_rf)

#################Create a merged geodataframe with values and geometry#########################    
d={'ID':list(shp['ID']),'Rainfall':Dist_avg_rf}     #Create a rainfall datatframe
data_f=pd.DataFrame(data=d)

df_merged = shp.merge(data_f, left_on='ID', right_on='ID') #Merge it with shapefile to create geodataframe to plot

####################################Plot Settings#############################################
min_cbar=Dist_avg_rf.min()                                                         # Minimum for colorbar
max_cbar=Dist_avg_rf.max()                                                        # Maximum for colorbar
level_cbar=40                                                        # No. of levels for colorbar

months=["January","February","March","April","May","June","July","August","September","October","November","December"]
fig, ax = plt.subplots(1, figsize=(10,12))
df_merged.plot(column='Rainfall',cmap=cmap, linewidth=1, ax=ax, edgecolor='0.9', legend = False) 
ax.axis('off')
fig.suptitle('Rainfall(mm)',fontsize=25)
ax.set_title(months[month_no-1]+" "+ str(year), fontsize=18, loc='Left')

#####################Giving labels to each district##########################################
df_merged['coords'] = df_merged['geometry'].apply(lambda x: x.representative_point().coords[:])
df_merged['coords'] = [coords[0] for coords in df_merged['coords']]
for idx, row in df_merged.iterrows():
    plt.annotate(text=row['DISTRICT_1'], xy=row['coords'],horizontalalignment='center',color=annot_color)     # To give name of district
    #plt.annotate(s=row['Rainfall'], xy=row['coords'],horizontalalignment='center')       # To give value of district average rainfall

plt.colorbar(ax.collections[0],ticks=np.linspace(min_cbar,max_cbar,num=level_cbar), label= label_cbar)

text_kws = dict(bbox=dict(color="none"),path_effects=[pe.withStroke(linewidth=0, foreground="w")], color="#67000d",fontsize=0,)
dist1.plot_regions(ax=ax,text_kws=text_kws)

#################################Save the figure############################################
plt.savefig(img_name)