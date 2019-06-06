# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *
import wrf 
from netCDF4 import Dataset
from sklearn.cluster import KMeans
from out_put_check_funs import *

# %%
path = '/Volumes/mbProD/Downloads/wrf_out_sample/wrfout_d04*'
clus_num = 6 
var = 'tc'
var_name = 'temp'

# %%
ds = cluster_ds(path,clus_num,var,var_name)

# %%
i=0
plt.subplots()
dsi = ds.temp.where(ds.new_lab==i)
dsi.mean(dim=['Time','bottom_top']).plot(cmap = cmBuRd,
                                        vmin=-20,vmax=20)
plt.subplots()
dsc = dsi.count(dim=['Time','bottom_top'])
dsc.name = 'counts'
dsc.plot()
plt.subplots()
dsi = ds[['temp']].where(ds.new_lab==i)
dsi = dsi.count(dim=['Time','south_north'])
dsi = dsi.assign_coords(height=ds.height.mean(dim=['Time','south_north']))

dsi.temp.plot(x='west_east',y='height')

# %%
ds1 = ds.where(ds.new_lab==0,drop=True)

# %%
ds2 = cluster_ds_raw(ds1,6,var, var_name)['ds']

# %%
i=5
plt.subplots()
dsi = ds2.temp.where(ds2.clus_lab==i)
dsi.mean(dim=['Time','bottom_top']).plot()
plt.subplots()
dsc = dsi.count(dim=['Time','bottom_top'])
dsc.name = 'counts'
dsc.plot()
plt.subplots()
dsi = ds2[['temp']].where(ds2.clus_lab==i)
dsi = dsi.count(dim=['Time','south_north'])
dsi = dsi.assign_coords(height=ds.height.mean(dim=['Time','south_north']))

dsi.temp.plot(x='west_east',y='height')

# %%
matplotlib.colors.ListedColormap(sns.color_palette('Greys',18))

# %%
sns.choose_colorbrewer_palette('s')

# %%

# %%
