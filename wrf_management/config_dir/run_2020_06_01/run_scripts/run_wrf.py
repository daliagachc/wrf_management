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
import importlib
import os

import init as it

print(it.run_name)

# import di_python.ya_esta as ye
import wrf_management.run_wrf as rw
import wrf_management.project_global_constants as gc

importlib.reload(rw)

# %%
df = rw.get_date_range(it.init_date, it.end_date)
print(rw.get_input_file_path(it.run_name))

input_path = rw.get_input_file_path(it.run_name)

input_dic = rw.get_input_dic(input_path)

new_input_dic = rw.modify_dt_input_dic(it.init_date, it.end_date, input_dic)
it.run_type = 'wrf'
run_type_dir = rw.create_run_type_dir(gc.PATH_DATA, it.run_name, it.run_type)

rw.write_input_dic(run_type_dir=run_type_dir, new_input_dic=new_input_dic)

# %%
it.parent_run

# %%
run_type_dir

# %%
parent_run_dir = os.path.join(gc.PATH_DATA, 'runs', it.parent_run)
parent_run_dir

# %%
dates = list(df.dt)
dates[0]

# %%
importlib.reload(rw)
real_path = rw.create_run_type_dir(gc.PATH_DATA, it.run_name, 'real')
print(real_path)
rw.link_wrfs(real_path=real_path, dest_path=run_type_dir)

# %%
importlib.reload(rw)
rw.link_wrf(dest_path=run_type_dir)

# %%
rw.cp_sbatch(source_dir='../', target_dir=run_type_dir, pat='*wrf*.sh')

# %%


