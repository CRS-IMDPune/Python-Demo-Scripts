# Python-Demo-Scripts

This project is meant to give a basic idea of how to access different types of data such as to read them, subset them
for particular location, level and time and writing a variable in a new file using Python Programming language.
Here we have used Python3 compiler for compiling the scripts. This includes some introductory scripts which will 
be further updated in due course by including plotting techniques also. It is to be noted that this project mainly
focus on the data types such as NetCDF4, BINARY and GRIB format which are the most common datasets available for 
weather and climate related research studies. Here we have used sample data of the aforementioned types which is 
provided in the folder 'CAUI-IMDPune/Python-Demo-Scripts/Sample_Data/'.

The structure of this repository is that sub-folders for read, subset and write files have been created with each 
of them containing seperate folders for each data types used. Here we have used the NetCDF4 and BINARY data from dataset provided by 
India Meteorology Department, GRIB files from fifth generation ECMWF Reanalysis data (ERA5) and also NETCDF4 data
from NCEP reanalysis datasets. 

One can download these datasets from the following web portals:

https://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html		- IMD Gridded Data
https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5		  - ERA5 Reanalysis Data
https://psl.noaa.gov/data/gridded/data.ncep.reanalysis2.html			        - NCEP Reanalysis 2 Data

The Python routines used in the scripts include netCDF4, numpy, pyngl and datetime. It is to be noted that there are 
multiple ways available in Python to perform these operations and here we try to depict only some methods.

The path for obtaining the scripts are listed below:

1. Read scripts
	CAUI-IMDPune/Python-DEMO-Scripts/Read/
2. Subsetting scripts
	CAUI-IMDPune/Python-DEMO-Scripts/subset/
3. Writing Scripts 
	CAUI-IMDPune/Python-DEMO-Scripts/write/
4. Sample Datasets
	CAUI-IMDPune/Python-DEMO-Scripts/Sample_Data/
