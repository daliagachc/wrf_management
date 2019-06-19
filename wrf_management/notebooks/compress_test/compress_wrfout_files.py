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
# path  = '/Volumes/mbProD/Downloads/wrf_test_d01/'
pc = 'taito'
# pc = 'mac'

if pc is 'taito':
    path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'
    path_out  = '/proj/atm/saltena/runs/run_2019_05_15/wrf_compressed'
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = '2017-12-0*'
    wrfout_patt = 'wrfout'
    
if pc is 'taito':
    path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-18_17-40-56_/2017-12-08'
    path_out  = os.path.join(path,'.compressed_log')
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = '*.nc'
    wrfout_patt = ''
    date_pattern = ''
    
if pc is 'taito':
    path = '/proj/atm/saltena/runs/run_2019_03_01/wrf'
    path_out  = os.path.join(path,'wrf_compressed')
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = ''
    wrfout_patt = 'wrfout'
    
if pc is 'mac':
    path = '/Volumes/mbProD/Downloads/wrf_test_d01/'
    path_out  = '/private/tmp/co_out/'
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = 'd01*'
    wrfout_patt = 'wrfout'
self = CO.Compresser(path,path_out,db_path,pattern=patt,wrfout_patt=wrfout_patt,lock_last_date=False)

# %%
# self.drop_files_table()

# %%
while True:
    self.get_and_zip_next_row(move=True)

# %%
