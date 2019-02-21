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
import wrf_management.base_namelists.base_namelists as bn
importlib.reload(bn);
import f90nml

# %%
con = sq.connect(gc.PATH_DB)

# %%
importlib.reload(ut)
program = 'ungrib'
unique_id = ut.get_unique_id(program)
print(unique_id)
unique_id = '2019-02-21T17-29-01_753696_ungrib'

# %%
importlib.reload(ut)
new_path = ut.get_new_unique_path_for_program(unique_id=unique_id)
print(new_path)
new_path = '/tmp/wrf_management/data_folder/runs/2018_02_19/2019-02-21T17-29-01_753696_ungrib'

# %%
ut.get_tb_from_name(tb_name='run_unique_id')

# %%
date_to_ungrib = '2017-12-15'

# %%
rows = {}
for tb in gc.FILE_TYPES.keys():
#     print(tb)
    sql = """
    select * from {tb} where date(date)=date('{dt}')
    """.format(tb=tb,dt=date_to_ungrib)
    rows[tb]=pd.read_sql(sql,con)
    rows[tb]['tb']=tb
df = pd.concat(list(rows.values()))
if df.downloaded.all()!=True: print('not all downloaded')
df


# %%
df['tar_path']=df.apply(lambda r: os.path.join(ut.get_tar_path(r.tb),r['name']),
         axis = 1)
df['untar_path']=df.apply(lambda r: new_path,
         axis = 1)
row = df.iloc[0]
df


# %%
import tarfile
tfile = tarfile.TarFile(row.tar_path)

# %%
tfile.extractall(row.untar_path)

# %%



