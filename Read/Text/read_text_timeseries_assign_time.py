#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#############
########## https://doi.org/10.5281/zenodo.5674826 ############

###############Reading time series from a text file and assigning a time dimension#######
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

######################################Read the Nino 3.4 index as a dataframe###############################################
f=pd.read_csv('E:/NINO_CNN_MODEL/Data/Nino_3.4_monthly_anomaly_NOAA ERSST V5.txt',delimiter='  ',header= None,engine='python')
print(f.shape)
################################################Read the index into a time series##########################################
data=[]
for i in range(0,f.shape[0]):
    for j in range(1,f.shape[1]):   # Skip first column to remove year info
        data.append(f[j][i])

year=[]                             # Read year information from file
for i in range(0,f.shape[0]):
    for j in range(0,f.shape[1],13):    # Skip every 12 columns to read only year
        year.append(f[j][i])
#print(year)
#######################################Store time series as a numpy array##################################################
data_array=np.array(data)            
print(data_array.shape)

###################Define a time series using pandas######################
st_year=str(year[0])                # Get starting and ending year from file
en_year=str(year[len(year)-1])
Time=pd.date_range(start=st_year+'-01-01',end=en_year+'-12-31',freq='M')
print(Time.shape)

#####################Create an xarray dataset file for Nino3.4 anomaly with time dimension#####
NINO34 = xr.Dataset(
    data_vars=dict(
        Nino34=(["time"], data_array),
    ),
    coords=dict(
        time=(["time"], Time),
        reference_time=Time[0],
    ),
    attrs=dict(description="Monthly Nino3.4 SST Anomaly"),
)
print(NINO34)

NINO34.to_netcdf('Nino34_SST_Anomaly.nc')        # Save the variable as a dataset in a netCDF file
####################Try plotting Nino34 time series#####################
fig=plt.figure(figsize=(12,8))
NINO34.sel(time=slice('2010-01-01','2020-12-31')).Nino34.plot(marker='o')
plt.title('Nino3.4 Time series',fontsize=15)
plt.tick_params(axis="both", labelsize=15)
plt.xlabel('Time',fontsize=15)
plt.ylabel('Nino3.4 SST Anomaly',fontsize=15)
plt.savefig('Timeseries_Nino34.png',facecolor='white')    # Save the plot
