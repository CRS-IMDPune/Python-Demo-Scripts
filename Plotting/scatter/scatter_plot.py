###############Reading IMD binary (GRD) data for Maximum temperature###############

import numpy as np
import matplotlib.pyplot as plt

filename1='/mnt/d/DATA/IMD_MaxTemp/Maxtemp_MaxT_2020.GRD'	##File path
filename2='/mnt/d/DATA/IMD_MinTemp/Mintemp_MinT_2020.GRD'	##File path

###############Have to set according to data format##############################

nlat=31			# Obtained from the ctl file
nlon=31
ndays=366
lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
#print(lons)
lats=np.arange(7.5,38.5,1)
#print(lats)

#########################Read Maximum Temperature################################

f=open(filename1,'rb')
data=np.fromfile(f,dtype="float32",count=-1)	# Opening and reading the file into a one dimensional array
print(data, len(data))
print(data.min())
print(data.max())

################Reshaping data######################

maxtemp=np.reshape(data,(ndays,nlat,nlon),order='C')
#print(maxtemp.shape)
#print(maxtemp.min())
#print(temp[50,:,:])
del f
del data
##########################Read Minimum Temperature##############################

f=open(filename2,'rb')
data=np.fromfile(f,dtype="float32",count=-1)	# Opening and reading the file into a one dimensional array
print(data, len(data))
#print(data.min())
#print(data.max())

################Reshaping data######################

mintemp=np.reshape(data,(ndays,nlat,nlon),order='C')
print(mintemp.shape)
print(mintemp.min())
#print(temp[50,:,:])

###############Mask the fill values##############################################

maxtemp_mask=np.ma.masked_where(maxtemp>99.0, maxtemp)
mintemp_mask=np.ma.masked_where(mintemp>99.0, mintemp)

####################Scatter Plot for JJAS and NDJF##############################

fig=plt.figure(figsize=(18,10))
plt.scatter(maxtemp_mask,mintemp_mask,s=1)
plt.title('2020')
plt.xlabel("Maximum Temperature (degC)")
plt.ylabel("Minimum Temperature (degC)")
plt.savefig("scatter_plot.png")
exit()
