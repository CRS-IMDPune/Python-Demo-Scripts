###############Reading IMD binary (GRD) data for Maximum temperature###############

import numpy as np

filename='/mnt/e/Python_Scripts/Sample_Data/Maxtemp_MaxT_2018.GRD'

nlat=31
nlon=31
ntime=365

lons=np.arange(67.5,99.5,1)
print(lons)
lats=np.arange(7.5,39.5,1)
print(len(lats))

f=open(filename,'rb')
data=np.fromfile(f,dtype="float32",count=-1)
print(data, len(data))
print(data.min())
print(data.max())

################Reshaping data######################

temp=np.reshape(data,(365,31,31),order='C')
print(temp.shape)
print(temp.min())
#print(temp[50,:,:])


exit()
