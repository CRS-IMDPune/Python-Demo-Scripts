#########PYTHON CODE FOR IMD PREPARED BY LEKSHMI S############
########## https://doi.org/10.5281/zenodo.5674826 ############
##############Reading Excel/csv File##############################

###############Import necessary modules##################
import pandas as pd
import xlrd
import openpyxl

############Read excel file##############################
rf=pd.read_excel('RAINFALL SERIES.xls',usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
rf
rf.info()

#################Read each column#######################
print(rf[['YEAR','JUN','JUL','AUG','SEP']][109:120])

###################Selecting a row########################
print(rf.iloc[1])

###############statistical values#######################
print(rf.describe())
mean_rf=rf.mean(axis='index')
print(mean_rf)
exit()
