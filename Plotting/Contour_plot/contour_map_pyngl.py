from __future__ import print_function
import Ngl,Nio
import os
import numpy as np
print("")

#--  data file name
fname  = "/mnt/e/Python_Scripts/Sample_Data/olr.day.mean.float.nc"

#--  open file
f = Nio.open_file(fname, "r")
lon=f.variables["lon"][:]
lat=f.variables["lat"][:]
olr = f.variables["olr"][0,:,:]

############Subsetting over lat and lon##############

latbounds = [ -40 , 40 ]	#degrees north
lonbounds = [ 10 , 200 ] 	# degrees east 

latselect=np.logical_and(lat>=latbounds[0],lat<=latbounds[1])
lonselect=np.logical_and(lon>=lonbounds[0],lon<=lonbounds[1])
olrsub=olr[latselect,:][:,lonselect]

print(olrsub.max())
print(olrsub.shape)

######################Setting Plot Resources############
#-- start the graphics
wks = Ngl.open_wks("png",os.path.basename(__file__).split('.')[0])

#-- set resources
res                      =  Ngl.Resources()

res.cnFillOn             =  True
res.cnLinesOn            =  False
res.cnLineLabelsOn       =  False
res.cnLevelSelectionMode = "ManualLevels"
res.cnMinLevelValF       =  np.min(olr)
res.cnMaxLevelValF       =  np.max(olr)
#res.cnLevelSpacingF      =  20
res.cnFillPalette        = 'ncl_default'

#res.tiMainString         = "OLR"

res.lbLabelFontHeightF   = 0.01
res.lbOrientation        = 'horizontal'
#res.pmLabelBarOrthogonalPosF = -0.1
res.pmLabelBarHeightF    = 0.07
res.pmLabelBarWidthF     = 0.6

res.sfXArray             = lon[lonselect]
res.sfYArray             = lat[latselect]

res.mpLimitMode          = 'LatLon'
res.mpMinLonF            =  min(lon[lonselect])
res.mpMaxLonF            =  max(lon[lonselect])
res.mpMinLatF            =  min(lat[latselect])
res.mpMaxLatF            =  max(lat[latselect])
res.mpGridAndLimbOn      = False
res.mpCenterLonF	  =100


#-- create the plot
plot = Ngl.contour_map(wks, olrsub, res)
Ngl.end()

exit()
