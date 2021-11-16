###############Reading IMD binary (GRD) data for Maximum temperature###############
###############Plotting the max temp for any one day###############

import numpy as np
import os
import matplotlib.pyplot as plt

filename='/mnt/e/Python_Scripts/Sample_Data/Maxtemp_MaxT_2018.GRD'

nlat=31			# Obtained from the ctl file
nlon=31
ntime=365

lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
print(len(lons))
lats=np.arange(7.5,38.5,1)
print(len(lats))

f=open(filename,'rb')		# Opening and reading the file into a one dimensional array
data=np.fromfile(f,dtype="float32",count=-1)
print(data, len(data))
print(data.min())
print(data.max())
data_mask=np.ma.masked_where(data==99.9, data)	# Mask where there is missing value

################Reshaping data######################

temp=np.reshape(data_mask,(365,31,31),order='C')	# Reshaping data according to the control file
print(temp.shape)
print(temp.min())
#print(temp[50,:,:])

###################Plotting ############################
minlev=20
maxlev=temp.max()
levels=np.linspace(minlev,maxlev,20)

X,Y=np.meshgrid(lats,lons)
fig,ax=plt.subplots(1,1)
cp=ax.contourf(X,Y,temp[121,:,:],levels=levels,alpha=0.8)	#	for Fill contours
cp1=ax.contour(X,Y,temp[121,:,:],levels=levels)
fig.colorbar(cp)
ax.set_title('Maximum Temperature in 2018')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.savefig('contour_imd_fill_line.png')		
exit()
