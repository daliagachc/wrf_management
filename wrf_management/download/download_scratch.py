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
# imports
import pandas as pd
from wrf_management import project_global_constants as gc
import importlib
importlib.reload(gc)

# %%
date_index = pd.date_range(
    start = gc.INIT_DATE ,
    end   = gc.END_DATE
)

df = pd.DataFrame(date_index, columns=['date'])
df = df.reset_index()
df = df.set_index('date')
df = df.rename(columns={'index':'i'})
df['downloaded'    ] = False
df['ungribed'    ] = False
df['metgrided'    ] = False
df.sample(5)

# %%
tmp_path = '/tmp/path.csv'
df.to_csv(tmp_path)
df_readed = pd.read_csv(tmp_path)


# %%
gc.PATH_DATA

# %%
import os
os.makedirs(gc.PATH_DATA,exist_ok=True)

# %%
import wrf_management.utilities as ut
importlib.reload(gc);
importlib.reload(ut);

# %%
ut.create_date_db(override=True)

# %%
ut.get_date_tb().sample()

# %%
ut.create_download_db(db_name='borrar')

# %%
down_dbs = {}
for k in gc.FILE_TYPES:
    print(k)
    down_dbs[k]=ut.create_download_db(db_name=k,override=True)
    

# %%
con = sq.connect(gc.PATH_DB)


# %%
pd.read_sql('select * from sqlite_master',con)

# %%
ut.get_tb_from_name(tb_name='press')

# %%
row = down_dbs['press'].iloc[0]

# %%
for f in gc.FILE_TYPES:
    row = down_dbs[f].iloc[-1]
    string = ut.get_down_string_from_row(row=row,ftype=f)
    print(string)

# %%
import wrf_management.utilities as ut
importlib.reload(gc);
importlib.reload(ut);

# %%
row=ut.get_next_row_to_down(tb_name='press')

# %%
row.date

# %%
ut.get_down_string_from_row(row=row, ftype='press')

# %%
ut.update_sucess_down(row=row,tb_name='press')

# %%


# %%
ut.get_tb_from_name(tb_name='press')

# %%
import wrf_management.utilities as ut
importlib.reload(gc);
importlib.reload(ut);

# %%
ut.down_file('')

# %%
!ls -la


# %%

