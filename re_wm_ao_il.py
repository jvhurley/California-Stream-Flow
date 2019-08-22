import numpy as np
import matplotlib.pyplot as plt
#import arcpy
#from arcpy import env
from netCDF4 import Dataset
from matplotlib.path import Path
from scipy import interpolate
from mpl_toolkits.basemap import Basemap
from datetime import datetime
import wget
import os

ncfix=(r"C:\Users\JHurley\Mangoes\NOAA_NWM\nwm-v1.2-channel_spatial_index.nc")
ncfdix=Dataset(ncfix,'r')
cvr=0
for v in ncfdix.variables:
    print(ncfdix.variables[v].long_name)
    cvr=cvr+1
    print(cvr)
    print(ncfdix.variables[v])
    
lon=ncfdix.variables['longitude'][:]
lat=ncfdix.variables['latitude'][:]

htpfo=(r"https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/nwm.")
ftpfo=(r"ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/nwm.")
ftpfo_ii=(r"/medium_range_mem1/")  ### ENSEMBLE MEMBER 1-ONE as mem1
tada=datetime.today().strftime('%Y%m%d')
dafo=(ftpfo+tada+ftpfo_ii)
dafoh=(htpfo+tada+ftpfo_ii)

ncf_i=(r"nwm.t00z.medium_range.channel_rt_1.f")  ### ENSEMBLE MEMBER 1-ONE as rt_1
ncf_e=(r".conus.nc")
oufo=(r"C:\Users\JHurley\Mangoes\NOAA_NWM\data")

os.system('del '+oufo+'\*.nc')
os.system(r'del C:\Users\JHurley\Mangoes\NOAA_NWM\CAQ_figs\*.png')

ejn=43
ejs=32
ejw=-125
eje=-114

def CAQmap(sfl_sortd,thisday,projhr,sfl_sizes):
    cmp=plt.get_cmap('gist_ncar_r')#('gist_ncar_r')
    fig=plt.figure(figsize=(10,8))
    m=Basemap(projection='cyl',\
          #lon_0=(lon_g[-1]+lon_g[0])/2,\
          #lat_0=(lat_g[-1]+lat_g[0])/2,\
          llcrnrlon=ejw,llcrnrlat=ejs,\
          urcrnrlon=eje,urcrnrlat=ejn,\
          resolution='i')
    srvc=('World_Shaded_Relief')
    m.arcgisimage(service=srvc,xpixels = 1000,ypixels=None, verbose= False)
    m.drawcoastlines()
    m.drawcountries(linewidth=2.0,color='black')
    m.drawstates(linewidth=2.0,color='dimgray')
    m.drawrivers(linewidth=0.3,color='black')
    parallels=np.arange(-90.,90.,1.)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    meridians=np.arange(0.,360.,2.)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    m.scatter(sfl_sort[:,0],sfl_sort[:,1],c=sfl_sort[:,2],vmin=0,vmax=400,s=sfl_sizes,alpha=0.9,cmap=cmp,marker='o')
    #m.scatter(np.flipud(lon),np.flipud(lat),c=np.flipud(sfl),vmin=0,vmax=30,s=0.05,alpha=0.9,cmap=cmp,marker='o')
    m.colorbar()
    plt.title('Stream Discharge (m'+r'$^3$'+' s'+r'$^-$'+r'$^s$'+'), '+thisday+': '+ina)
    plt.tight_layout()
    plt.savefig('C:/Users/JHurley/Mangoes/NOAA_NWM/CAQ_figs/CAQ_'+thisday+'_'+projhr+'.png')
    plt.close()


import urllib.request

hrstp=6

fistr=""
ncstr=""
for i in np.arange(hrstp,(24*10)+hrstp,hrstp):
    if i<10:
        ina=('00'+str(i))
    if (i>9) and (i<100):
        ina=('0'+str(i))
    if i>=100:
        ina=str(i)
    ncf=(ncf_i+ina+ncf_e)
    taget=(dafo+ncf)
    tageth=(dafoh+ncf)
    ncstr=(ncstr+' '+taget)
    oufi=('C:/Users/JHurley/Mangoes/NOAA_NWM/data/'+ncf)
    ncfnp=(oufo+"\\"+ncf)
    if (os.path.isfile(ncfnp))==0:
        #wget.download(taget,oufo)
        wget.download(tageth,oufo)
    #urllib.request.urlopen(dafo,[60])
    #urllib.request.urlretrieve(taget,oufi)
    #ncfnp=(oufo+"\\"+ncf)
    ncfd=Dataset(ncfnp,'r')
    sfl=ncfd.variables['streamflow'][:]
    sfl_sort=np.zeros((sfl.shape[0],3))
    sfl_sort[:,0]=lon
    sfl_sort[:,1]=lat
    sfl_sort[:,2]=sfl
    sfl_sort[sfl_sort<-1000]=np.nan
    sfl_sort=sfl_sort[sfl_sort[:,2].argsort()]
    sfl_sort[:,2][sfl_sort[:,2]<=2]=np.nan
    sfl_size=np.zeros((sfl_sort.shape[0]))
    sfl_size[np.isnan(sfl_sort[:,2])==1]=np.nan
    sfl_size[sfl_sort[:,2]<=2]=np.nan
    smlixa=np.where((sfl_sort[:,2]>2))
    smlixb=np.where((sfl_sort[:,2]<20))
    smlix=np.intersect1d(smlixa,smlixb)
    sfl_size[smlix]=.5
    sfl_size[sfl_sort[:,2]>=20]=4
    nestr=('C:/Users/JHurley/Mangoes/NOAA_NWM/CAQ_figs/CAQ_'+tada+'_'+ina+'.png ')
    if (os.path.isfile(nestr))==0:
        CAQmap(sfl_sort,tada,ina,sfl_size)
    fistr=(fistr+nestr)
    print(i)
    print(ncf)
    print(taget)

gifcmd=('magick convert -delay 60 -loop 0 '+fistr+' C:/Users/JHurley/Mangoes/NOAA_NWM/CAQ_gifs/CAQ_'+tada+'.gif')
os.system(gifcmd)
    



















    



    
