
#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S##############
########## https://doi.org/10.5281/zenodo.5674826 ############

## 1. Read the rainfall data for multiple years
## 2. Subset for a fixed time period
## 3. Resampling daily to monthly accumulated rainfall using xarray resampling and plot for a month
## 4. Resampling daily to monthly accumulated rainfall using pandas multi-indexing and plot for a month

#Import necessary modules
import numpy as np
import xarray as xr
import pandas as pd
import datetime as dt

#Path of input datasets
path_basep="S:/IMD_rainfall_0.25/2021_updated/*.nc"

#Read the rainfall data of multiple years using xarray
df=xr.open_mfdataset(path_basep)
df_sub=df.sel(TIME=slice('1971-01-01','2020-12-31'))

#METHOD 1 (USING XARRAY RESAMPLING)
#Resampling daily to monthly accumulated rainfall 
df_monthly=df_sub.resample(TIME='1m').sum(dim='TIME',skipna=False)          # Use while doing resample, to keep nan values
df_monthly
df_monthly.RAINFALL.sel(TIME='2000-06-30').plot()

#METHOD 2 (USING PANDAS MULTI-INDEXING)
#Resampling daily to monthly accumulated rainfall
year_month_idx = pd.MultiIndex.from_arrays([df_sub['TIME.year'].values, df_sub['TIME.month'].values])   #Define multi-index
df_sub.coords['year_month'] = ('TIME', year_month_idx)                             # Assign multi-index as coordinates to data array
df_monthly = df_sub.groupby('year_month').sum(skipna=False)                        # Resample using new index
df_monthly.RAINFALL.sel(year_month_level_0=2000,year_month_level_1=6).plot()       # Subsetting from multi index for plot