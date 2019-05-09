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
from useful_scit.imps import *

# %%
path = '/Users/diego/Downloads/'
gl = 'wrfout*'
glpath = os.path.join(path,gl)
files = glob.glob(glpath)

# %%
files

# %%
f1 = files[3]

# %%
d1 = xr.open_dataset(f1)

# %%
dummy = '/tmp/dummy.nc4'

# %%
d1.to_netcdf(dummy,format='NETCDF4')

# %%
s1 = os.path.getsize(f1)

# %%
os.path.getsize(dummy)

# %%
vars2keep = [
    'ZNW','ZNU','PB','P','PHB','PH','T','QVAPOR','TKE_PBL','XLAT',
    'XLONG','MAPFAC_M','PSFC','U10','V10','T2','Q2','SWDOWN','RAINNC','RAINC',
    'HFX','UST','PBLH','U','V','W',
    #'AVGFLX_RUM','AVGFLX_RVM','AVGFLX_WWM','MU','MUB','WW',
]  #32

# %%
d2 = d1[vars2keep].copy()

# %%
dm2 = '/tmp/dummy.nc4'
d2.to_netcdf(dm2,format='NETCDF4')

# %%
s2 = os.path.getsize(dm2)

# %%
s2/s1

# %%
fileF = '/Users/diego/Downloads/wrfout_d02_2010-05-18_00.nc'

# %%
df = xr.open_dataset(fileF)

# %%
df

# %%

