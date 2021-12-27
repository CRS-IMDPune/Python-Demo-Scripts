###############Reading IMD binary (GRD) data for Maximum temperature###############

import numpy as np
import glob
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq

filename1='/mnt/d/DATA/IMD_MaxTemp/Maxtemp_MaxT_20*.GRD'	##File path

###############Have to set according to data format##############################

nlat=31				# Obtained from the ctl file
nlon=31
nyear=21
years=np.arange(2000,2021,1)
lons=np.arange(67.5,98.5,1)	# Define latitude and longitude as obtained from ctl file
#print(lons)
lats=np.arange(7.5,38.5,1)
#print(lats)

latbounds = [ 18.0 , 29.0 ]	#Lat-lon bound for Heat Wave (MZI)
lonbounds = [ 65.0 , 89.0 ] 	# degrees east 

######################Fixed for the looping#######################################

npos=59
jjas_days=122
lp=0
nlp=0
lpdays=366
nlpdays=365
fill=99.9
a=0

MaxTemp=np.full([nyear,lpdays,nlat,nlon],fill,order='C')	# Create an empty 4d array to store data
na=np.full([nlat,nlon],fill,order='C')				# Array to be given for leap year day in non-leap years

####################Looping for reading maxtemp data#############################

for files in glob.glob(filename1):
	f=open(files,'rb')
	maxdata=np.fromfile(f,dtype="float32",count=-1)				#  Reading the file into a 1D array
	y=years[a]
	if (y%4==0):
		maxtemp=np.reshape(maxdata,(lpdays,nlat,nlon),order='C')	#Reading variable in required shape
		MaxTemp[a,:,:,:]=maxtemp					# Storing variable in the empty array
	else:
		maxtemp=np.reshape(maxdata,(nlpdays,nlat,nlon),order='C')
		maxtemp=np.insert(maxtemp,npos,na,axis=0)
		MaxTemp[a,:,:,:]=maxtemp					# Storing variable in the empty array
	a=a+1
#print(MaxTemp.shape)
del files
del f

##############Extract season data and lat-lon range for each year####################

latselect=np.logical_and(lats>=latbounds[0],lats<=latbounds[1])
lonselect=np.logical_and(lons>=lonbounds[0],lons<=lonbounds[1])
maxtemp_jjas=MaxTemp[:,152:274,:,:][:,:,latselect,:][:,:,:,lonselect]         # For JJAS


tmax_mask=np.ma.masked_where(maxtemp_jjas>99.0, maxtemp_jjas)                              #Mask the fill values
tmax_anom=np.empty([nyear,jjas_days,tmax_mask.shape[2],tmax_mask.shape[3]],order='C')      #Create empty array to store anomaly
tmax_anom_mask=np.ma.masked_where(maxtemp_jjas>99.0,tmax_anom)                     #Mask anomaly array where maxtemp_jjas has fill values

for i in range(0,tmax_mask.shape[0]):
    tmax_anom_mask[i,:,:,:]=tmax_mask[i,:,:,:]-(np.mean(tmax_mask,axis=0))    #Calculate anomaly for each year

tmax=np.mean(tmax_anom_mask,axis=(2,3))                          #Averaging over MZI

##############Calculate power spectrum for each year#################################

fft_vals=np.empty([nyear,jjas_days],order='C',dtype='complex_')		#To store Fourier transform
ps=np.empty([nyear,jjas_days],order='C')        #To store power spectrum
freqs=fftfreq(jjas_days)                        # Calculate frequency
mask=freqs>0                                    # mask where frequency is negative

for i in range(0,tmax.shape[0]):
    fft_vals[i,:]=fft(tmax[i,:])            #calculate Fourier transform for each year
    ps[i,:]=2.0*((np.abs(fft_vals[i,:])/jjas_days)**2.0)  #Calculate power spectrum for each year
    mean_=np.mean(tmax[i,:]) 
    std_=np.std(tmax[i,:])
    var_=std_**2
    print(var_)
    print(np.sum(ps[i,mask]))	# Sum of all power spectral density should be equal to variance of data

#print(np.sum(fft_vals[1,mask]))

ps_avg=np.mean(ps[:,mask],axis=0)			# Averaging power spectrum over all years

freq_mask=freqs[mask]
####################################Plotting Resources###############################

x=np.arange(min(np.log(freqs[mask])),max(np.log(freqs[mask])),10)
x_label=[round(1/a,2) for a in x]

fig =plt.figure(figsize=(20,7))
ax=fig.add_subplot(1,1,1)
ax.plot(freq_mask[:],ps_avg[:],linewidth=1.0,linestyle='-',color='r',label='Frequency vs Spectra',marker='o')
ax.set_title(' Maximum Temperature (JJAS)', color='blue',fontsize=16)
ax.set_ylabel('Power',fontsize=16);   ax.set_xlabel('log Frequency',fontsize=16)
ax.set_xscale('log')
ax.set_xlim(0.01,0.5)
ax.set_ylim(0.0,0.4)
ax.tick_params(axis='both', which='major', labelsize=16)
#plt.xticks(x,x_label,rotation=60)
plt.grid(True)
#leg=ax.legend()

plt.savefig('ps_tmax_jjas_power_frequency.png')

fig1 =plt.figure(figsize=(20,7))
ax1=fig1.add_subplot(1,1,1)
ax1.plot(freqs[mask],ps_avg*freqs[mask],linewidth=2.0,linestyle='-',color='r',label='Frequency vs Spectra',marker='o')	# marker='o'
#ax.plot(freqs[mask],ci[:,0],linewidth=1.0,linestyle='--',color='black')
#ax.plot(freqs[mask],ci[:,1],linewidth=1.0,linestyle='--',color='black')

ax1.set_title(' Maximum Temperature (JJAS)', color='blue',fontsize=16)
ax1.set_ylabel('Power * Frequency',fontsize=16);   ax1.set_xlabel('log Frequency',fontsize=16)
ax1.set_xscale('log')
ax1.set_xlim(0.01,0.5)
ax1.set_ylim(0.0,0.011)
ax1.tick_params(axis='both', which='major', labelsize=16)
#ax.xticks(x,x_label,rotation=60)
plt.grid(True)
#leg=ax.legend()

plt.savefig('ps_tmax_jjas_power_frequency1.png')
exit()



