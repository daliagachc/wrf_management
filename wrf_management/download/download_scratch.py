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
importlib.reload(ut);

# %%
df = ut.create_date_db(gc.INIT_DATE, gc.END_DATE, gc.PATH_DB, override=True)

# %%
df

# %%

