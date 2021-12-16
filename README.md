# Python-Demo-Scripts
https://doi.org/10.5281/zenodo.5674826

This project is meant to give a basic idea of how to access different types of data such as to read them, subset them
for particular location, level and time and writing a variable in a new file using Python Programming language.
Here we have used Python3.6.7 compiler for compiling the scripts. This includes some introductory scripts which will 
be useful for the analysis of meorological gridded datasets. It is to be noted that this project mainly focus on 
the data types such as NetCDF4, BINARY and GRIB format which are some of the most common datasets available for 
weather and climate related research studies. Here we have used sample data of the aforementioned types which is 
provided in the folder 'CRS-IMDPune/Python-Demo-Scripts/Sample_Data/'.

The structure of this repository is that sub-folders for reading, subsetting and writing the files have been created
with each of them containing seperate folders for each data types used. A sub-folder with some of the most common 
plotting techniques used for the analysis of meteorological datasets are also included. Here we have used the NetCDF4 
and BINARY data from dataset provided by India Meteorology Department, GRIB files from fifth generation ECMWF Reanalysis 
data (ERA5) and also NETCDF4 data for NOAA interpolated OLR. 

An introduction to the netCDF4 dataset can be obtained from:
https://www.unidata.ucar.edu/software/netcdf/

For more details about the GRIB dataset and their structure, visit
https://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/

Information about gridded binary data can be obtained from the below sites:
https://climatedataguide.ucar.edu/climate-data-tools-and-analysis/binary
http://cola.gmu.edu/grads/gadoc/aboutgriddeddata.html#formats

One can download the sample datasets used here from the following web portals:

https://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html		- IMD Gridded Data
https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5		- ERA5 Reanalysis Data
https://psl.noaa.gov/data/gridded/data.interp_OLR.html			        - NOAA interpolated OLR

The Python routines used in the scripts include os, netCDF4, numpy, pyngl, xarray, cfgrib, datetime, cartopy, basemap, 
geopandas, regionmask etc. It is to be noted that there are multiple ways available in Python to perform these 
operations and here we try to depict only few of them.

The path for obtaining the scripts and sample data are listed below:

1. Read scripts
	CRS-IMDPune/Python-DEMO-Scripts/Read/
2. Subsetting scripts
	CRS-IMDPune/Python-DEMO-Scripts/subset/
3. Writing Scripts 
	CRS-IMDPune/Python-DEMO-Scripts/write/
4. Plotting Scripts
	CRS-IMDPune/Python-DEMO-Scripts/Plotting/
5. Sample Datasets
	CRS-IMDPune/Python-DEMO-Scripts/Sample_Data/
	
STRUCTURE OF REPOSITORY

The example scripts for each of the operations performed are kept in seperate folders inside the main directory. The
operations included are reading, subsetting, writing and plotting the datasets. The 'Read' directory contains seperate 
sub-folders for netcdf, binary and grib format. Each of these sub-folders include scripts for reading single and multiple 
files using Python. 

Similar subfolders are also placed in the 'subset' directory for each data types. This operation handles subsetting of the 
data for required time steps, spatial extent and vertical levels.The scripts for writing subset of a dataset in a new file 
of netCDF4 format are included in the sub-folders of 'write' folder.  

In the 'plotting' directory sub-folders are given for different kinds of plotting techniques that can be used for analysis.
It includes time series, line and filled contours, including maps, overlaying plots, vector plots and usage of shapefiles.
Shapefile has been used to give administrative boundaries (Eg: state or district) in the map and also has been used for 
obtaining zonal statistics (such as state average) and to plot them.

The sample datasets used in this project has been included in the 'Sample_Data' directory.
	
Due to size restrictions for uploading data files some files are not included in '/CRS-IMDPune/Python-DEMO-Scripts/Sample_Data',
one can get it from the web portals mentioned above.

A detailed description of the Python packages and modules used and a study conducted using IMD gridded temperature data with
the help of Python plotting techniques has been provided in the document '/CRS-IMDPune/Python-DEMO-Scripts/Application.pdf'.

Disclaimer: The codes, plots and every other content added here are meant for academic and research purposes. In no event shall the code developers or India meteorological department be liable to any party for direct, indirect, special, incidental or consequential damages including lost profits, arising out of the use of these codes and its documentation. The data, codes, shapefiles, maps and plots included in here does not define any administration areas or boundaries and the code developers or India meteorological department by no means claim the legal or scientific authenticity of these contents added here. All the codes are obtained, modified or developed from open source resources.
