###################Calculating state average of a variable and plotting using shape file#######
import geopandas as gpd
import regionmask 
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import datetime as dt
import pandas as pd
import matplotlib.patheffects as pe

#####################read the rainfall data file needed to plot###############################
year=2018                          #Give the year of which file is read
season='JJAS'                        #Give a season from JF,MAM,JJAS,OND

f1_name='/mnt/rc/IMD_rainfall_0.25/_Clim_Pred_LRF_New_RF25_IMD0p252018.nc'   #Filename of year to be read

fname='/mnt/rc/All Shape File/Kerala district shape file/Kerala districtshape file.shp'           # District shapefile of kerala
data = pd.read_csv('Grid_District_Contribution.csv')                                              # Load the percent mask file

####Label Bar Settings
label_cbar= "District Cumulative Rainfall (mm)"               # Give the label for colorbar

img_name='district_cumulative_rf_seasonal_percent_mask.png'                # Give the name for saving the image

####Annotation Color
annot_color='cyan'                                                   # Color for annotation of district name in plot

#####Colorbar for plot
cmap='tab20b_r'    

#######################No editing required below##############################################
f1 = nc.Dataset(f1_name)
rf_fill=f1.variables['RAINFALL']

f1 = nc.Dataset(f1_name)
for var in f1.variables.values():
    print(var)                                                       # Print Metadata for all variables

lats = f1.variables['LATITUDE'][:]
lons = f1.variables['LONGITUDE'][:]
time = f1.variables['TIME']

lat_size=len(lats)
lon_size=len(lons)

####################################Subsetting over time#####################################
if (season=='JF'):
    st_date=dt.datetime(year,1,1,0,0)                                   #Season start
    en_date=dt.datetime(year,3,1,0,0)                                   #Season end
elif (season=='MAM'):
    st_date=dt.datetime(year,3,1,0,0)                                   #Season start
    en_date=dt.datetime(year,5,31,0,0)                                   #Season end
elif (season=='JJAS'):
    st_date=dt.datetime(year,6,1,0,0)                                   #Season start
    en_date=dt.datetime(year,9,30,0,0)                                   #Season end
elif (season=='OND'):
    st_date=dt.datetime(year,10,1,0,0)                                   #Season start
    en_date=dt.datetime(year,12,31,0,0)                                   #Season end
else:
    print('Season not defined')

sday=nc.date2index(st_date,time,calendar='standard',select='exact')  #Gives us index of necessary day
eday=nc.date2index(en_date,time,calendar='standard',select='exact') 
rf_season=(f1.variables['RAINFALL'][sday:eday,:,:]).sum(axis=0)     # Reading for required days and finding total seasonal rainfall 

#########################Read the shape file and create masks###############################
shp=gpd.read_file(fname)
print(shp['DISTRICT_1'])
dist_name=list(shp['DISTRICT_1'])
dist_1=list(shp['DISTRICT_1'])
indexes=[dist_name.index(x) for x in dist_1]                             # Obtain district indexes

dist1=regionmask.Regions(outlines=list(shp.geometry.values[i] for i in range(0, shp.shape[0])), names=shp.DISTRICT_1[indexes],abbrevs=shp.DISTRICT_1[indexes],name='district', )   # Obtaining region boundaries
dist1_mask=dist1.mask(lons,lats)     

#######################Read the percentage mask file#################################
district=data['District'][:]
lat=data['Grid Lat'][:]
lon=data['Grid Lon'][:]
percent=data['Percent contribution'][:]

#######################Calculate the district area averaged rainfall for a day########
Dist_avg_rf=np.full(len(dist_1),rf_fill._FillValue, order='C')

for i in range(0,len(dist_1)):
    lat_percent=(lat[dist_name[i] == district]).tolist()
    lon_percent=(lon[dist_name[i] == district]).tolist()
    percent_mask=((percent[dist_name[i] == district]).tolist())
    
    Total=0.0
    Total_weight=0.0
    print(dist_name[i])
    for j in range (0, len(lat_percent)):
        
        ind_lat_rf=np.where(lats == lat_percent[j])
        ind_lon_rf=np.where(lons == lon_percent[j])
     
        Total= Total+ rf_season[ind_lat_rf,ind_lon_rf] * percent_mask[j]
        Total_weight= Total_weight+ percent_mask[j]
        
        #print(Total, "   ",percent_mask[j])
        
    Dist_avg_rf[i]=Total/Total_weight                 #Area-weighted district rainfall 
 
    del Total
    del lat_percent
    del lon_percent
    del percent_mask
    del Total_weight
    
print(Dist_avg_rf)

#################Create a merged geodataframe with values and geometry#########################    
d={'ID':list(shp['ID']),'Rainfall':Dist_avg_rf}     #Create a rainfall datatframe
data_f=pd.DataFrame(data=d)

df_merged = shp.merge(data_f, left_on='ID', right_on='ID') #Merge it with shapefile to create geodataframe to plot

####################################Plot Settings#############################################
min_cbar=Dist_avg_rf.min()                                                         # Minimum for colorbar
max_cbar=Dist_avg_rf.max()                                                        # Maximum for colorbar
level_cbar=40                                                                     # No of levels in cbar

fig, ax = plt.subplots(1, figsize=(10,12))
df_merged.plot(column='Rainfall',cmap=cmap, linewidth=1, ax=ax, edgecolor='0.9', legend = False) 
ax.axis('off')
fig.suptitle('Rainfall(mm)',fontsize=25)
ax.set_title(season+" "+str(year), fontsize=18, loc='Left')

#####################Giving labels to each district##########################################
df_merged['coords'] = df_merged['geometry'].apply(lambda x: x.representative_point().coords[:])
df_merged['coords'] = [coords[0] for coords in df_merged['coords']]
for idx, row in df_merged.iterrows():
    plt.annotate(text=row['DISTRICT_1'], xy=row['coords'],horizontalalignment='center',color=annot_color)     # To give name of district
    #plt.annotate(text=row['Rainfall'], xy=row['coords'],horizontalalignment='center')       # To give value of district average rainfall

plt.colorbar(ax.collections[0],ticks=np.linspace(min_cbar,max_cbar,num=level_cbar), label= label_cbar)

text_kws = dict(bbox=dict(color="none"),path_effects=[pe.withStroke(linewidth=0, foreground="w")], color="#67000d",fontsize=0,)
dist1.plot_regions(ax=ax,text_kws=text_kws)
#################################Save the figure############################################
plt.savefig(img_name)