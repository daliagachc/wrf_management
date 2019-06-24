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
SOURCE_PATH = '/proj/atm/saltena/runs/run_2019_02_28_2/wrf'
ZIP_PATH = os.path.join(os.path.dirname(SOURCE_PATH), 'wrf_compressed')

self = CO.Compresser(
    source_path=SOURCE_PATH,
    zip_path=ZIP_PATH,
    db_path=os.path.join(ZIP_PATH,'zip.sqlite'),
    pattern='',
    files_table_name='files_table',
    lock_last_date=False,
    wrfout_patt='wrfout',
    compress_level_target=4,
    source_path_is_file=False
)


# %%
self.reset_locks()
while True:
    self.get_and_zip_next_row(move=True)

# %%
