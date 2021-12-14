#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#########
########## https://doi.org/10.5281/zenodo.5674826 ############

##################################READING A NETCDF4 FILE######################################
###########Import necessary modules##########################
import netCDF4 as nc

############ File to be read ####################
############ IMD Gridded Rainfall data ##########

file_name  = "/mnt/e/Python_Scripts/Sample_Data/RFone_imd_rf_1x1_2019.nc"

################# open file ######################

f = nc.Dataset(file_name)
print(f)                # gives us information about the variables 
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

print(rf.min()," ,",rf.max())
exit()

