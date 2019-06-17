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
import wrf_management.modules.blayer_wind as bw
from useful_scit.imps import *

# %%

glob_pat = '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfout_d04*'
path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/slices_chc_lapaz'

bw.read_and_spit(glob_pat,path_out)


# %%
import xarray.core.indexing