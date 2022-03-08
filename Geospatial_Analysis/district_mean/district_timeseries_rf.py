##########################Import necessary modules#############################################
import netCDF4 as nc
import datetime as dt
import pandas as pd
import geopandas as gpd
import regionmask
import numpy as np
import matplotlib.pyplot as plt

################Specify the data files to be read#############################################
f1_name='/mnt/rc/IMD_rainfall_0.25/_Clim_Pred_LRF_New_RF25_IMD0p2520*.nc'    #File names 2000-2020
st_year=2000                                      #Start Year

fname='/mnt/rc/All Shape File/Kerala district shape file/Kerala districtshape file.shp'           # District shapefile of kerala

#####################Read the rainfall data file needed to plot###############################
f1 = nc.MFDataset(f1_name)     # Read all data files together and concatenate
rf_fill=f1.variables['RAINFALL']

rf   = f1.variables['RAINFALL'][:]                   # Read Rainfall time series of 21 years                                
lats = f1.variables['LATITUDE'][:]
lons = f1.variables['LONGITUDE'][:]
time = f1.variables['TIME']

lat_size=len(lats)
lon_size=len(lons)
time_size=len(time[:])

#########################Read the shape file and create masks###############################
shp=gpd.read_file(fname)
print(shp['DISTRICT_1'])
dist_name=list(shp['DISTRICT_1'])
dist_1=list(shp['DISTRICT_1'])
indexes=[dist_name.index(x) for x in dist_1]                             # Obtain district indexes

dist1=regionmask.Regions(outlines=list(shp.geometry.values[i] for i in range(0, shp.shape[0])), names=shp.DISTRICT_1[indexes],abbrevs=shp.DISTRICT_1[indexes],name='district', )   # Obtaining region boundaries
dist1_mask=dist1.mask(lons,lats) 

#######################Read the percentage mask file#################################
data = pd.read_csv('Grid_District_Contribution.csv')                                              # Load the percent mask file
district=data['District'][:]
lat=data['Grid Lat'][:]
lon=data['Grid Lon'][:]
percent=data['Percent contribution'][:]

#######################Calculate the district area averaged rainfall for a day########
Dist_avg_rf=np.full([len(dist_1),time_size],rf_fill._FillValue, order='C')

for i in range(0,len(dist_1)):
    
    lat_percent=(lat[dist_name[i] == district]).tolist()
    lon_percent=(lon[dist_name[i] == district]).tolist()
    percent_mask=((percent[dist_name[i] == district]).tolist())
        
    for k in range (0,time_size):
        Total=0.0
        Total_weight=0.0
        
        for j in range (0, len(lat_percent)):
            ind_lat_rf=np.where(lats == lat_percent[j])
            ind_lon_rf=np.where(lons == lon_percent[j])
            Total= Total+ rf[k,ind_lat_rf,ind_lon_rf] * percent_mask[j]
            Total_weight= Total_weight+ percent_mask[j]
        
        Dist_avg_rf[i,k]=Total/Total_weight                 #Area-weighted district rainfall
        del Total
        del Total_weight
    del lat_percent
    del lon_percent
    del percent_mask
    
    
print(Dist_avg_rf)

###########################Creating X axis strings for plot###################################
date_string=[]
for n in range(0,Dist_avg_rf.shape[1],365):
    dates=dt.datetime(st_year,1,1,0,0,0)+n*dt.timedelta(hours=24) 
    date_string.append(dates.strftime('%Y%m%d'))
    del dates
x=np.arange(0,Dist_avg_rf.shape[1],365)

####################################Plotting time series of each districts#####################
resolution=75
for i in range(0,Dist_avg_rf.shape[0]):
    fig=plt.figure(figsize=(8,5))
    plt.plot(Dist_avg_rf[i,:],linewidth=1.0,linestyle='-',color='b')	# marker='o'
    plt.title(dist_name[i])
    plt.ylim(0,Dist_avg_rf.max())
    plt.xlim(0,time_size)
    plt.ylabel('daily rainfall(mm)')	#;plt.xlabel('Time')
    plt.xticks(x,date_string,rotation=60)
    plt.grid(True)

    plt.savefig(dist_name[i]+'.png',dpi=resolution)