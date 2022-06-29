
#######PYTHON CODE FOR IMD PREPARED BY LEKSHMI S#############
########## https://doi.org/10.5281/zenodo.5674826 ############

############################Read the csv file and save as text####################################
import pandas as pd
import numpy as np
data=pd.read_csv('Bihar_rain.csv')
dist_name=list(data.columns[:])
np.savetxt('Bihar_rain.txt',data,fmt='%s %6.2f %10.2f %12.2f %10.2f %10.2f %12.2f %10.2f \
             %10.2f %10.2f %10.2f %10.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f \
             %12.2f %10.2f %10.2f %12.2f %14.2f %16.2f %12.2f %14.2f %10.2f %10.2f %12.2f %16.2f \
             %12.2f %12.2f %10.2f %12.2f %10.2f %10.2f %10.2f %10.2f',header=str(list(data.columns[:])),\
             comments=' ')

#########################################Read the text file ######################################
cols=np.arange(1,39,1)
data1=np.loadtxt('Bihar_rain.txt',dtype='float64',usecols=cols,skiprows=1)  ####To read data as float numbers
dates=np.loadtxt('Bihar_rain.txt',usecols=0,dtype='str')       ##To read dates column as string
head=np.loadtxt('Bihar_rain.txt',dtype='str',max_rows=1)        ##To read headers
print(dates)
