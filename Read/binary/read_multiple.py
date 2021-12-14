#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

###############Reading multiple binary (GRD) data for Maximum temperature###############

import numpy as np
import glob

filename='/mnt/e/Python_Scripts/Sample_Data/Maxtemp_MaxT_20*.GRD'	##File path

nlat=31			# Obtained from the ctl file
nlon=31
ntime=365

lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
#print(lons)
lats=np.arange(7.5,38.5,1)
#print(lats)

a=0
Temp=np.empty(shape=[2,ntime,nlat,nlon])	# Create an empty 4d array to store data

for files in glob.glob(filename):
	f=open(files,'rb')
	data=np.fromfile(f,dtype="float32",count=-1)	# Opening and reading the file into a 1D array
	
	################Reshaping data######################
	
	temp=np.reshape(data,(ntime,nlat,nlon),order='C')	#Reading the variable in required shape
	#print(temp.min())
	Temp[a,:,:,:]=temp		# Storing variable in the empty array
	a=a+1

print(Temp.shape)
#print(temp.min())
#print(data, len(data))
#print(data.min())
#print(data.max())

print(Temp[0,:,:,:].min())
#print(temp[50,:,:])


exit()
