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

# %%
df = ut.get_tb_from_name(tb_name='press')
df[df.downloaded==1]

# %%
importlib.reload(ut);

# %%
ut.get_untarred_path('press')

# %%
importlib.reload(ut);
importlib.reload(gc);
tb_name = 'press'
row=ut.get_untarred_row(tb_name=tb_name,date='2018-01-01',comparator = '=')
print(row)
row_name = row['name']

# %%
import os
tar_path = ut.get_tar_path(tb_name=tb_name)
tar_file_path = os.path.join(tar_path,row_name)
tar_file_path

# %%
import tarfile
tar_file = tarfile.open(tar_file_path) 

# %%
file_names = tar_file.getnames()
print(file_names[::5])

# %%
untar_path = ut.get_untarred_path(tb_name)
untar_path_dir = os.path.join(untar_path,row_name)
print(untar_path,untar_path_dir)

# %%
os.makedirs(untar_path_dir,exist_ok=True)

# %%
try:
    tar_file.extractall(untar_path_dir,)
except: 
    os.remove(untar_path_dir)

# %%
    os.remove(untar_path_dir)

# %%
import wrf_management

# %%
os.path.dirname(wrf_management.__file__)

# %%
importlib.reload(gc)

# %%
os.makedirs(gc.RUN_CONFIG_DIR)

# %%
import shutil

# %%
shutil.copyfile('../base_namelists/Vtable.CFSR',gc.RUN_CONFIG_DIR+'/Vtable.CFSR')

# %%


