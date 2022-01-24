###############Reading IMD binary (GRD) data for Maximum temperature###############

import numpy as np
import glob
import matplotlib.pyplot as plt
import datetime as dt
import netCDF4 as nc
import geopandas as gpd
import regionmask
import pandas as pd

filename1='/mnt/rc/IMD_Temp_0.5/meant/MEANT2018_0.5.GRD'	##File path
year=2018
st_date=dt.datetime(year,8,15,0,0)                                   #Give necessary day to be plotted here (year,month,day)

###############Have to set according to data format from CTL##############################
lons=np.arange(67.5,98.0,0.5)	# Define latitude and longitude as obtained from ctl file
lats=np.arange(7.5,38.0,0.5)
nlat=len(lats)
nlon=len(lons)

####################Read the file for temperature mentioned above#########################
f=open(filename1,'rb')
tmp=np.fromfile(f,dtype="float32",count=-1)
tmp_re=np.reshape(tmp,(int(len(tmp)/(nlat*nlon)),nlat,nlon),order='C')

#######################To create time values for the above year data######################
dates=[]
time_unit="days since 1900-01-01"
for n in range(0,tmp_re.shape[0],1):
    dates.append(dt.datetime(year,1,1,0,0,0)+n*dt.timedelta(hours=24) )
    
date_num=nc.date2num(dates,time_unit)

###################Find the index of the required date to be plotted######################
iday=[i for i in range(len(dates)) if dates[i] == st_date]

########################Read temperature for the required day#############################
temp=tmp_re[iday,:,:].squeeze()
print(temp.shape)

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
dist_temp_all=np.empty(len(dist_1))
for i in range(0,shp.shape[0]):              
    result=np.where(dist1_mask==i)
    lat_ind=result[0]
    lon_ind=result[1]
    temp_dist=np.mean((temp[lat_ind,:][:,lon_ind]),axis=(0,1))
    #temp_dist=temp[lat_ind,:][:,lon_ind]
    dist_temp_all[i]=temp_dist
    del temp_dist
print(dist_temp_all)

#################Create a merged geodataframe with values and geometry#########################    
d={'ID':list(shp['ID']),'Temperature':dist_temp_all}     #Create a rainfall datatframe
data_f=pd.DataFrame(data=d)

df_merged = shp.merge(data_f, left_on='ID', right_on='ID') #Merge it with shapefile to create geodataframe to plot

####################################Plot Settings#############################################
date_string=st_date.strftime("%d/%m/%Y")
fig, ax = plt.subplots(1, figsize=(10,12))
df_merged.plot(column='Temperature',cmap='tab20b_r', linewidth=1, ax=ax, edgecolor='0.9', legend = True) 
ax.axis('off')
fig.suptitle('Temperature(deg C)',fontsize=25)
ax.set_title(date_string, fontsize=18, loc='Left')

#####################Giving labels to each district##########################################
df_merged['coords'] = df_merged['geometry'].apply(lambda x: x.representative_point().coords[:])
df_merged['coords'] = [coords[0] for coords in df_merged['coords']]
for idx, row in df_merged.iterrows():
    plt.annotate(s=row['DISTRICT_1'], xy=row['coords'],horizontalalignment='center')     # To give name of district
    #plt.annotate(s=row['Temperature'], xy=row['coords'],horizontalalignment='center')       # To give value of district average temperature
    
#################################Save the figure############################################
plt.savefig('district_avg_temperature_daily.png')
