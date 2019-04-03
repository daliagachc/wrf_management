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
import wrf 

# %%
path = '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/'

# %%
gl=glob.glob(path+'wrf*')
df = pd.DataFrame(gl,columns=['path'])
gl

# %%
bo = df.path.str.contains('bdy')
bdy = df[bo]['path'].iloc[0]
bdy

# %%
bdy_d = xr.open_dataset(bdy)
# bdy_d.dims
print(str(bdy_d)[:3000])


# %%
bo = df.path.str.contains('fdda')
dda = df[bo]['path'].iloc[0]

# %%
# dda_d.close()
dda_d = xr.open_dataset(dda)
print(str(dda_d)[:2000])
# dda_d.Times

# %%

