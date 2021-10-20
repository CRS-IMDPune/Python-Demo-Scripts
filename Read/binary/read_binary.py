###############Reading IMD binary (GRD) data for Maximum temperature###############

import numpy as np

filename='/mnt/e/Python_Scripts/Sample_Data/Maxtemp_MaxT_2018.GRD'

nlat=31			# Obtained from the ctl file
nlon=31
ntime=365

lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
print(lons)
lats=np.arange(7.5,38.5,1)
print(lats)

f=open(filename,'rb')
data=np.fromfile(f,dtype="float32",count=-1)	# Opening and reading the file into a one dimensional array
print(data, len(data))
print(data.min())
print(data.max())

################Reshaping data######################

temp=np.reshape(data,(365,31,31),order='C')
print(temp.shape)
print(temp.min())
#print(temp[50,:,:])


exit()
