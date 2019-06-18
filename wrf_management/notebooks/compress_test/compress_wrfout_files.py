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
# %load_ext autoreload
# %autoreload 2

# %%
from useful_scit.imps import * 
import useful_scit.util.zarray as za

# %%
import wrf_management.modules.CompressOut as CO
import sqlite3


# %%
# path  = '/Volumes/mbProD/Downloads/wrf_test_d01/wrfout_d01_2017-12-25_00:00:00'
# path_out = '/tmp/wrfout_d01_2017-12-25_00:00:00'
# self = CO.CompressOut(path,path_out)

# %%
# path  = '/Volumes/mbProD/Downloads/wrf_test_d01/'

path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'
path_out  = '/proj/atm/saltena/runs/run_2019_05_15/wrf_compressed'
db_path = os.path.join(path_out,'zip.sqlite')
# patt = 'd01*'
patt = '2017-12-0*'
self = CO.Compresser(path,path_out,db_path,pattern=patt)

# %%
self.merge_update_dfs()
while True:
    self.get_and_zip_next_row()


# %%
