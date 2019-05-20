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
from check_input_01_funs import * 

# %%
matplotlib.rcParams['figure.figsize'] = (9.0, 6.0)

# %%
path = '/Volumes/mbProD/Downloads/wrf_small_files'

# %%
glob.glob(path+'/wrf*')

# %%
file_path = os.path.join(path,'wrfinput_d01')

# %%
xa = xr.open_dataset(file_path).isel(Time=0)

# %%
pars = ['SST','T2','TSK','SEAICE','LAKEMASK']
for p in pars:
    plt.figure()
    xa[p].plot(x='XLONG',y='XLAT')
    ax = plt.gca()
    ax.set_title(xa[p].description)
