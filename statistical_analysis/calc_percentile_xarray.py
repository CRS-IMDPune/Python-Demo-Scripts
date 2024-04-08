import xarray as xr
import numpy as np

tmean=xr.open_dataset('Tmax_1951_2021.nc')
# Find the 95th percentile and save the file
ds_group=tmean.groupby('time.dayofyear')
percentile=np.empty((366,tmean.shape[1],tmean.shape[2]),'float')
for i in range(0,366):
    ind=ds_group.groups.get(i+1)
    tsub=tmean.isel(time=ind)
    percentile[i,:,:]=np.percentile(tsub.values,q=95,axis=0)

ds = xr.Dataset(
    data_vars=dict(
        t95=(["time","lat","lon"], percentile,\
             {'units':'deg C','name':'T95'}),
    ),
    coords=dict(
        lon=(["lon"], tmean.lon.values,{'units':'degrees East'}),
        lat=(["lat"], tmean.lat.values,{'units':'degrees North'}),
        time=np.arange(1,367,1),
    ),
    attrs=dict(description="95th percentile of daily mean temperature",\
               source="IMD daily 0.5 deg gridded temperature data"),
)
    
ds.to_netcdf('IMD_Mean_Temperature_95_percentile.nc')