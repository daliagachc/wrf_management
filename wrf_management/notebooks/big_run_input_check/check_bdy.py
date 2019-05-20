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
matplotlib.rcParams['figure.figsize'] = (9.0, 6.0)

# %%
path = '/Volumes/mbProD/Downloads/wrf_small_files'

# %%
glob.glob(path+'/wrf*')

# %%
file_path = os.path.join(path,'wrfbdy_d0_short')

# %%
xa = xr.open_dataset(file_path)

# %%
xa

# %%



