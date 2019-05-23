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
# %load_ext autoreload

# %%
# %autoreload 2

# %%
from useful_scit.imps import *
import check_input_01_funs as pp
from check_input_01_funs import *

# %%
# path = '/Volumes/mbProD/Downloads/wrf_small_files'
path = '/proj/atm/saltena/runs/run_2019_05_15/real/'

# %%
glob.glob(path+'/wrf*')

# %%
file_path = os.path.join(path,'wrflowinp_d04')
file_input = os.path.join(path,'wrfinput_d04')

# %%
xa = xr.open_dataset(file_path)

# %%
plot_lowinp_pars(xa)

# %% [markdown]
# SST show issues:
# - min<220 K 
# - max>320 K

# %%
xa_low = import_lowinp(file_path,file_input)


# %%
p = 'SST'
p_c = p+'_clus'
nc = 7
cols = 2
plot_clus_sig(xa_low,p,p_c,nc,cols=2)


# %%
p = 'SEAICE'
p_c = p+'_clus'
nc = 2
cols = 2
plot_clus_sig(xa_low,p,p_c,nc,cols=2)

# %%
p = 'VEGFRA'
p_c = p+'_clus'
nc = 5
cols = 2
plot_clus_sig(xa_low,p,p_c,nc,cols=2)

# %%
p = 'LAI'
p_c = p+'_clus'
nc = 6
cols = 2
plot_clus_sig(xa_low,p,p_c,nc,cols=2)

# %%
x1 = xa_low.where(xa_low.LAKEMASK==1)
p = 'SST'
nc = 6
p_c = p+'_clus_lake'
cols = 2
plot_clus_sig(x1,p,p_c,nc,cols=2)

# %%
x1 = xa_low.where(xa_low.LAKEMASK==1)
p = 'SEAICE'
nc = 2
p_c = p+'_clus_lake'
cols = 2
plot_clus_sig(x1,p,p_c,nc,cols=2)

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



