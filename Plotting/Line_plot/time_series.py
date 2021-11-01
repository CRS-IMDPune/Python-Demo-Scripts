########Plotting time series of rainfall at a particular location#############

###########Import necessary modules##########################

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

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
en_date=dt.datetime(2019,8,1,0,0)	# End date and hour
date=nc.num2date(time[:],units=time.units,calendar='standard')

istart=nc.date2index(st_date,time,calendar='standard',select='exact')
iend=nc.date2index(en_date,time,calendar='standard',select='exact')

############Subsetting over lat and lon##############

latselect=np.where(lats==10.5)
lonselect=np.where(lons==82.5)

u10sub=u10[istart:iend,latselect,lonselect]
print(u10sub.max())
print(u10sub.shape)

#########Creating date strings for X axis#############

date_string=[]
for n in range(0,u10sub.shape[0],96):
	dates=dt.datetime(2019,6,1,0,0,0)+n*dt.timedelta(hours=1) 
	i=int(n/24)
	date_string.append(dates.strftime('%Y%m%d'))
	del dates
x=np.arange(0,u10sub.shape[0],96)

##################Plot time series #################

fig=plt.figure(figsize=(16,7))
plt.plot(u10sub[:,0,0],linewidth=1.0,linestyle='-',color='b')	# marker='o'

plt.title(' Time Series of U wind at 10m from 01/6 to 01/8 2019')
plt.ylabel('U wind (m/s)')	#;plt.xlabel('Time')
plt.xticks(x,date_string,rotation=60)
plt.grid(True)

plt.savefig('time_series.png')
exit()
