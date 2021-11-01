###############Reading IMD binary (GRD) data for Maximum temperature###############
###############Plotting the max temp for any one day###############

import numpy as np
import Ngl
import os

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

################Reshaping data######################

temp=np.reshape(data,(365,31,31),order='C')	# Reshaping data according to the control file
print(temp.shape)
print(temp.min())
#print(temp[50,:,:])

##############Plotting the data for one day#########

#-- start the graphics
#wks = Ngl.open_wks("png",os.path.basename(__file__).split('.')[0])	# Opening a workstation for plot
wks = Ngl.open_wks("png","contour_line")
#-- set resources
res                      =  Ngl.Resources()

res.cnFillOn             =  False	# False for line contours
res.cnLinesOn            =  True	# True for Lines
res.cnLineLabelsOn       =  True	# True for Line Labels
res.cnLevelSelectionMode = "ManualLevels"
res.cnMinLevelValF       =  20
res.cnMaxLevelValF       =  95
res.cnLevelSpacingF      =  3
res.cnFillPalette        = 'ncl_default'

#res.tiMainString         = "OLR"

res.lbLabelFontHeightF   = 0.015
res.lbOrientation        = 'horizontal'
#res.pmLabelBarOrthogonalPosF = -0.1
res.pmLabelBarHeightF    = 0.07
res.pmLabelBarWidthF     = 0.6

res.sfXArray             = lons
res.sfYArray             = lats

res.mpLimitMode          = 'LatLon'
res.mpMinLonF            =  min(lons)
res.mpMaxLonF            =  max(lons)
res.mpMinLatF            =  min(lats)
res.mpMaxLatF            =  max(lats)
res.mpGridAndLimbOn      = False
#res.mpDataBaseVersion    = "Ncarg4_1"
res.mpCountyLineThicknessF=5.0

#-- create the plot
plot = Ngl.contour_map(wks, temp[10,:,:], res)
Ngl.end()
exit()
