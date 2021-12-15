#########PYTHON CODE FOR IMD PREPARED BY LEKSHMI S############
########## https://doi.org/10.5281/zenodo.5674826 ############

################SUBSETTING A BINARY FILE######################
###############Import necessary Module########################
import numpy as np
###############Reading IMD binary (GRD) data for Maximum temperature###############
filename='/mnt/e/Python_Scripts/Sample_Data/Maxtemp_MaxT_2018.GRD'

nlat=31			# Obtained from the ctl file
nlon=31
ntime=365

lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
#print(lons)
lats=np.arange(7.5,38.5,1)
#print(lats)

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

###############Subsetting lat-lon range#############

latbounds = [ 10 , 30 ]
lonbounds = [ 70.5 , 90.5 ] # degrees east 

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
print(latselect)

tempsub1=temp[:,latselect,:][:,:,lonselect]		# Subsetting lat lon range
print(tempsub1.shape)
#print(tempsub1)

tempsub2=tempsub1[0:10,:,:]		# Subsetting days using day number of a year (here 2018)
print(tempsub2.shape)
exit()
