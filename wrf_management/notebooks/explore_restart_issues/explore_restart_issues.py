# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *
import pprint
import funs

# %%


# %%

# %%
class Dummy:
    def __init__(self):
        pass
path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'
df = funs.get_files_df(path)

# %%
_df = df[(df[funs.DOM]==1)&(df[funs.KIND]==funs.wrfrst)]
_df['2018-04-08':'2018-04-09']

# %%
_df = df[(df[funs.DOM]==1)&(df[funs.KIND]==funs.wrfout)]
_df = _df['2018-04-08':'2018-04-09']
_paths = _df[funs.PATH].values

# %%
ds = xr.open_mfdataset(_paths)

# %%
XLAT = 'XLAT'
XLONG = 'XLONG'
try:
    ds[XLAT]= ds[XLAT].mean(TIME)
    ds[XLONG]= ds[XLONG].mean(TIME)
except: pass

# %%
# ds

# %%
_boo = \
    (ds[XLAT] < -23) &(ds[XLAT] > -24)  & \
    (ds[XLONG]< -61) &(ds[XLONG]> -62)  


# %%
_va = funs.U10

for _va in funs.VARS2D[:]:
#     print(_va)
    _da = ds[_va].where(_boo)
    if funs.TIME in _da.dims:
        _da1=_da.dropna(south_north,how='all').dropna(west_east,how='all')

        _da2 = _da1.swap_dims({funs.TIME:funs.XTIME})

        _fg = _da2.plot.line(col=west_east,row=south_north,figsize=[15,5])
        axs=_fg.axes.flatten()
        for ax in axs:
            ax.axvline(pd.Timestamp('2018-04-08 15'),color='k');
        ax.figure.suptitle(_da2.description,y=1.01,fontsize=16)
        ax.figure.tight_layout()

# %%
funs.VARS3D

# %%
bottom_top = 'bottom_top'
bottom_top_stag = 'bottom_top_stag'
cm = plt.get_cmap('Reds')
for _va in funs.VARS3D[:]:
#     print(_va)
    _da = ds[_va].where(_boo)
    if funs.TIME in _da.dims:
        _da1=_da.dropna(south_north,how='all').dropna(west_east,how='all').load()
        try:_da1 = _da1.isel(**{bottom_top:slice(0,10)})
        except: _da1 = _da1.isel(**{bottom_top_stag:slice(0,10)})

        _da2 = _da1.swap_dims({funs.TIME:funs.XTIME})
        
        _das = _da2.median(funs.XTIME)
        
        _da3:xr.DataArray = _da2/_das


        _fg = _da3.plot(x=funs.XTIME,col=west_east,row=south_north,figsize=[15,5],cmap=cm)
        axs=_fg.axes.flatten()
        for ax in axs:
            ax.axvline(pd.Timestamp('2018-04-08 15'),color='k');
        ax.figure.suptitle(_da2.description,y=1.01,fontsize=16)
#         ax.figure.tight_layout()

# %% [markdown]
# ds

# %%
ds

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
_da[XLAT].plot()

# %%
_boo = \
    (_da[XLAT]< -23) &(_da[XLAT]> -24)  & \
    (_da[XLONG]< -61)&(_da[XLONG]> -62) & \


# %%
_da1 = _da.where(_boo)

# %%
_da2=_da1.dropna(south_north,how='all').dropna(west_east,how='all')

# %%
XTIME = 'XTIME'
_ , ax = plt.subplots()
_da2.mean([south_north,west_east]).plot(x=XTIME,ax=ax)
ax.axvline(pd.Timestamp('2018-04-08 15'),color='k');


# %%
ax.axvline

# %%
_df = _da.to_dataframe()
TIME = 'Time'
_df = _df.unstack(TIME)[[PBLH]]

# %%
_dfv= _df.values

# %%
from sklearn.cluster import KMeans

# %%
_nc = 15
km = KMeans(_nc)

# %%
FLAGS = 'FLAGS'
_df[FLAGS]=km.fit_predict(_dfv)

# %%
_df[FLAGS].value_counts().plot.bar()

# %%

# %%

# %%
# for ii in range(_nc):
#     _,ax = plt.subplots(figsize=(20,3))
#     _df1 = _df[_df[FLAGS]==ii].drop(FLAGS,axis=1)
#     _df1.boxplot(rot=90,ax=ax)
#     _t = ax.get_xticks()[::5]
#     _l = ax.get_xticklabels()[::5]
#     ax.set_xticks(_t)
#     ax.set_xticklabels(_l)

# %%
_nds = _df[FLAGS].to_xarray()

# %%
ds[FLAGS]=_nds

# %%

# %%
# from matplotlib.colors import LinearSegmentedColormap
# cm = LinearSegmentedColormap.from_list('', ucp.cc[:_nc], N=_nc)
# import cartopy.crs as ccrs
# _,ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree()),figsize=(20,10))
# ds[FLAGS].plot(
#     x=XLONG,y=XLAT,levels=_nc+1,vmin=-.5,vmax = _nc-.5,ax=ax, transform=ccrs.PlateCarree(),cmap=cm,
#     cbar_kwargs={'ticks':range(_nc)}
# )
# ax.coastlines()
# gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                   linewidth=2, color='k', alpha=0.5, linestyle='--')


# %%
