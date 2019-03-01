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
import wrf_management.project_global_constants as gc

# %%
from wrf_management.run_utilities import get_1_df, is_log_success_from_row, update_rows

# %%
import importlib
import wrf_management.run_utilities as ru
importlib.reload(ru)
from wrf_management.run_utilities import get_1_df, is_log_success_from_row, update_rows


# %%
tb_name = gc.RUN_NAME
run_name = gc.RUN_NAME
ungrib_type = 'ungrib_surf'
ungrib_type = 'ungrib_press'
log_name = 'ungrib.log'
succes_str = '*** Successful completion of program ungrib.exe ***'

# ungrib_type = 'ungrib_avgtsfc'
# log_name = 'avg_tsfc.log'
# succes_str = '*** Successful completion of program avg_tsfc.exe ***'

# ungrib_type = 'metgrid'
# log_name = 'metgrid.log'
# succes_str = '*** Successful completion of program metgrid.exe ***'
# %%
df = get_1_df(tb_name, ungrib_type,lim=150)
# %%
print(len(df))
df.sample()

# %%
row = df.iloc[2]
success = is_log_success_from_row(log_name, row, run_name, succes_str, ungrib_type)
success

# %%
res = df.apply(
    lambda row: is_log_success_from_row(log_name, row, run_name, succes_str, ungrib_type),
    axis=1
)

df['success'] = res
df

# %%
res = df.apply(
    lambda row: update_rows(row, tb_name=tb_name, ungrib_type=ungrib_type, true_val=200) ,
    axis=1
)

# %%


row = df.iloc[20]

# %%

