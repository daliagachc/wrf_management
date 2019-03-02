# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import wrf_management.plot.plot as wp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import xarray as xa
import os
import importlib as ilib
import glob
import cartopy as ct

import matplotlib.pyplot as plt

import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import cartopy.io.img_tiles as cimgt




# %%
path_data = '/tmp/wrf_management/data_folder/runs/run_2019_02_28_1/wrf/'
path_data = '/tmp/wrf_management/data_folder/runs/run_2019_02_27/wrf'
file_df=wp.get_df_list(path=path_data)
file_df.sample(3)

# %%
ilib.reload(wp)
fdf2 = wp.get_subdf_in_multin(file_df, 'd', 2)
fdf2.sample()

# %%
row =fdf2.iloc[1]
row

# %%
xd = xr.open_dataset(row.p)

# %%
wp.print_var_starting_with(row.p,'')

# %%
ilib.reload(wp)
lam, laM = -17, -15
lom, loM = -70.1, -68.4
ll_dic = dict(lam=lam,laM=laM,lom=lom,loM=loM)
wesn_dic = wp.get_coords_from_la_lo(xd,ll_dic)
wesn_dic

# %%
fig,ax = plt.subplots()
xd['T2'].isel(Time=1).plot(
    x='XLONG',y='XLAT',
    ax=ax)
rect = matplotlib.patches.Rectangle(
    (
        ll_dic['lom'],
        ll_dic['lam'],
    ),
    ll_dic['loM']-ll_dic['lom'],
    ll_dic['laM']-ll_dic['lam'],
    facecolor='none', edgecolor='k'
)
ax.add_patch(rect)

# %%
extent = [lom, loM, lam, laM]
zzoom = 8
request = cimgt.OSM()

fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection=request.crs)
gl = ax.gridlines(draw_labels=True, alpha=0.2)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

ax.set_extent(extent)

ax.add_image(request, zzoom, interpolation='spline36')

plt.show()

# %%
par = ['T2','LAKEMASK','TSK','LANDMASK']
patchs = {}
for d,r in fdf2[:].iterrows():
#     print(d[0])
    xd = xr.open_dataset(r.p)[par]
    xd = xd.isel({
        'west_east':  slice(wesn_dic['wem'],wesn_dic['weM']),
        'south_north':slice(wesn_dic['snm'],wesn_dic['snM']),
    })
    patchs[d]=xd.swap_dims({'Time':'XTIME'})


# %%
dl = list(patchs.values())
xc = xr.concat(dl[:],dim='XTIME')

# %%
ddf = xc.to_dataframe().reset_index()

# %%
ddf = xc.to_dataframe().reset_index()
ppar = ['T2','TSK']
fig,axs = plt.subplots(2,1,sharey=True,sharex=True)
axf = np.ndarray.flatten(axs)
for p,ax in zip(ppar,axf ):
#     fig,ax = plt.subplots()
    ax = sns.lineplot(x='XTIME', y = p, data = ddf,ax=ax)
    ax.figure.autofmt_xdate()
    ax.grid()

# %%
xc1 = xc.where(xc.LAKEMASK>.08)
ddf = xc1.to_dataframe().reset_index()
ppar = ['T2','TSK']
fig,axs = plt.subplots(2,1,sharey=True,sharex=True)
axf = np.ndarray.flatten(axs)
for p,ax in zip(ppar,axf ):
#     fig,ax = plt.subplots()
    ax = sns.lineplot(x='XTIME', y = p, data = ddf,ax=ax)
    ax.figure.autofmt_xdate()
    ax.set_title(p)
    ax.grid()

# %%
xc1 = xc.where(xc.LAKEMASK==0)
ddf = xc1.to_dataframe().reset_index()
ppar = ['T2','TSK']
fig,axs = plt.subplots(2,1,sharey=True,sharex=True)
axf = np.ndarray.flatten(axs)
for p,ax in zip(ppar,axf ):
#     fig,ax = plt.subplots()
    ax = sns.lineplot(x='XTIME', y = p, data = ddf,ax=ax)
    ax.figure.autofmt_xdate()
    ax.set_title(p)
    ax.grid()

# %%
xc1 = xc.where(xc.LAKEMASK>=0)
ddf = xc1.to_dataframe().reset_index()
ppar = ['T2','TSK']
fig,axs = plt.subplots(2,1,sharey=True,sharex=True)
axf = np.ndarray.flatten(axs)
for p,ax in zip(ppar,axf ):
#     fig,ax = plt.subplots()
    ax = sns.lineplot(x='XTIME', y = p, data = ddf,ax=ax)
    ax.figure.autofmt_xdate()
    ax.set_title(p)
    ax.grid()

# %%
xcA = xc.where(xc.LAKEMASK>=0)
xcL = xc.where(xc.LAKEMASK==1)
xcT = xc.where(xc.LAKEMASK==0)
ppar = ['T2','TSK']
for p in ppar:
    xx=xcA[p]-xcL[p]

# %%
p='T2'
xcA[p].median(['south_north','west_east']).plot(color='red',label='All')
xcL[p].median(['south_north','west_east']).plot(color='blue',label='Lake')
xcT[p].median(['south_north','west_east']).plot(color='black',label='Land')
plt.gca().grid()
f = plt.gcf()
plt.gca().legend()


# %%
p='TSK'
xcA[p].median(['south_north','west_east']).plot(color='red',label='All')
xcL[p].median(['south_north','west_east']).plot(color='blue',label='Lake')
xcT[p].median(['south_north','west_east']).plot(color='black',label='Land')
plt.gca().grid()
f = plt.gcf()
plt.gca().legend()


# %%
xc1['T2'][0].plot()

# %%
for p in ['LAKEMASK','LANDMASK']:
    plt.subplots()
    xc[p][0].plot(x='XLONG',y='XLAT')

# %%



# %%



