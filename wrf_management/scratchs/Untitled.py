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
import wrf_management.utilities as ut
import importlib
importlib.reload(ut);
import wrf_management.project_global_constants as gc
importlib.reload(gc)
import wrf_management.geogrid as geo
import os
import sqlite3 as sq
import pandas as pd

# %%
gc.PATH_DB

# %%
con = sq.connect(gc.PATH_DB)

# %%
pd.read_sql('select * from sqlite_master',con)

# %%
df = pd.DataFrame(
    [{
        'run_name':gc.RUN_NAME,
        'unique_id':'2019-02-21T15-04-27_476148_geogrid',
        'pogram':'geogrid',
        'comments':'exploring geogrid',
     }]
)
df

# %%
df.to_sql(gc.RUNS_TB_NAME,con)

# %%
run_path = ut.get_run_data_path()
os.makedirs(run_path)

# %%
import datetime as dt 

# %%
unique_id = ut.get_unique_id()

# %%
unique_id

# %%
ut.list_table_names()

# %%


# %%

