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
import os
import pandas as pd
from importlib import reload 
reload(wp)

# %%
path = '/tmp/wrf_management/data_folder/runs/run_2019_02_20/2017_12_02/wrf/'
df = wp.get_df_list(path=path)

# %%
df.sample()

# %%
_d4 = df.index.get_level_values('d')==4
df4 = df[_d4]

# %%



# %%



# %%
for d in [1,2,3,4]:
    _d4 = df.index.get_level_values('d')==d
    df4 = df[_d4]
    plist =['T','T2','TSLB', 'SST','TSK',]
    skim = ['T','TSLB']
    adjust=['T']
    vm,vM = 260,310
    lv = round((vM-vm)/5.)+1
    columns = [0,3,6,9,12,15,18,21]
    nn = 6
    fig = plt.figure(1,figsize=(1.3*nn*len(columns),nn*len(plist)))
    ll = 1 
    for l in plist:
        for c in columns:
            row = df4.iloc[c]
            ar = xr.open_dataset(row.p)
            ax = fig.add_subplot(len(plist),len(columns),ll)
            ar1 = ar[l]
            desc = ar1.description
            ar1 = ar1.isel(Time=0)
            if l in skim: ar1 = ar1[0]
            if l in adjust: ar1 = ar1+290
            ar1.plot(ax=ax,levels=lv, vmin =vm,vmax=vM)
            ax.set_title(ax.get_title()+
                         '\n'+
                         desc)
            ax.set_aspect('equal')
            ll = ll+1
    # fig.tight_layout()
    fig.savefig('./plot_temps'+str(d)'.jpg',dpi=300)

# %%
list(ar.variables)

# %%
reload(wp)
wp.print_var_starting_with(row.p,'')


# %%
ar.isel(Time=0)['T00']

# %%



# %%
ar = xr.open_dataset(row.p)
plist =['LAKEMASK','LANDMASK']
skim = ['T','TSLB']
adjust=['T']
vm,vM = 260,310
lv = round((vM-vm)/5.)+1
for l in plist:
    fig, ax = plt.subplots()
    ar1 = ar[l]
    desc = ar1.description
    ar1 = ar1.isel(Time=0)
    if l in skim: ar1 = ar1[0]
    if l in adjust: ar1 = ar1+290
    ar1.plot(ax=ax,
             levels=4, 
#              vmin =vm,vmax=vM
            )
    ax.set_title(ax.get_title()+
                 '\n'+
                 desc)
    ax.set_aspect('equal')

# %%


