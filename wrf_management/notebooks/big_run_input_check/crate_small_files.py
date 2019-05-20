# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.0.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *

# %%
path = '/proj/atm/saltena/runs/run_2019_05_15/wrf/'

# %%
files = glob.glob(path+'wrf*_*')

# %%
files

# %%
ffdda = '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfbdy_d01'

# %%
xa = xr.open_dataset(ffdda)

# %%
xa1=xa.isel(Time=slice(0,None,50))

# %%
xa1.to_netcdf('/proj/atm/wrfbdy_d0_short')

# %%
