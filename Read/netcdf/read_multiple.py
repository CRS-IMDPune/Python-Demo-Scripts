#########PYTHON CODE FOR IMD PREPARED BY LEKSHMI S############
########## https://doi.org/10.5281/zenodo.5674826 ############

##################################READING MULTIPLE NETCDF4 FILES#######################################
###########Import necessary modules##########################

import netCDF4 as nc
import numpy as np

############ File to be read ####################
############ IMD Gridded Rainfall data ##########

file_name  = "/mnt/e/Python_Scripts/Sample_Data/RFone_imd_rf_1x1_*.nc"

########Set these values according to the data (hourly/daily/monthly)#########

nyear=2             # number of years
ntime=365           # number of days

################# open file ######################

f = nc.MFDataset(file_name)     # Read all data files together and concatenate
print(f)                        # gives us information about the variables 
                                #contained in the file and their dimensions            
for dim in f.dimensions.values():
    print(dim)          # Metadata for all dimensions
    
for var in f.variables.values():
    print(var)          # Metadata for all variables

print(f['rf'])          # Metadata of single variable

################# read variables  ################

rf   = f.variables['rf'][:]
lats = f.variables['lat'][:]
lons = f.variables['lon'][:]
time = f.variables['time'][:]
print(rf.min()," ,",rf.max())       # to print minimum and maximum of a variable

###################To reshape the variable into nyears*ndays*nlat*nlon########

RF=np.reshape(rf,(nyear,ntime,len(lats),len(lons)))
print(RF.shape)     # print shape of the variable
print(RF.min())     # print minimum of the variable
exit()

