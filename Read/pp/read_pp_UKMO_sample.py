#########PYTHON CODE FOR IMD PREPARED BY LEKSHMI S############
########## https://doi.org/10.5281/zenodo.5674826 ############

######## Read a UKMO .pp file ####################### 
import iris

filepath="/mnt/S/Lekshmi/GloSea6/20210401/Tsurf_op_sfc_apd_21_19930401_001.pp"

cubes=iris.load(filepath)      # load a single file into a list of Iris cubes
print(cubes)

air_temp=cubes[0]               # Load a particular cube from the list
print(air_temp)

cube=iris.load_cube(filepath)     # Load a single cube 
# This is same as cubes[0]
lats=cube.coord('latitude')     # Gets the coordinates of cube
print(lats.points)
lons=cube.coord('longitude')
print(lons.points)
time=cube.coord('time')
print(time.points)
forecast_period=cube.coord('forecast_period')
print(forecast_period.points)
