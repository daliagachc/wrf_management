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
def imp():
    import importlib as imp
    import os

    try:
        from . import init as it
    except:
        from wrf_management.config_dir.run_2019_02_27.run_scripts import init as it
    imp.reload(it)

    import di_python.ya_esta as ye
    import wrf_management.run_wrf as rw
    import wrf_management.project_global_constants as gc

    imlist = [ye,it,rw,gc,]
    for i in imlist: imp.reload(i)
imp()


# %%
df = rw.get_date_range(it.init_date, it.end_date)
imp.reload(ye)
print(rw.get_input_file_path(it.run_name))

input_path = rw.get_input_file_path(it.run_name)

input_dic = rw.get_input_dic(input_path)

new_input_dic = rw.modify_dt_input_dic(it.init_date, it.end_date, input_dic)

run_type_dir = rw.create_run_type_dir(gc.PATH_DATA, it.run_name, it.run_type)

rw.write_input_dic(run_type_dir=run_type_dir,new_input_dic=new_input_dic)


# %%
it.parent_run

# %%
run_type_dir

# %%
parent_run_dir = os.path.join(gc.PATH_DATA,'runs',it.parent_run)
parent_run_dir

# %%
dates = list(df.dt)
dates[0]

# %%
met_path = rw.get_metgrid_path(parent_run_path=parent_run_dir,
                   date=date)

# %%
imp()
rw.link_metgrids(parent_run_path=parent_run_dir,dates=dates,
                      dest_path= run_type_dir)

# %%
imp()
rw.link_real(dest_path=run_type_dir)

# %%
'/tmp/wrf_management/app_folder/WRF4/WRF/main/real.exe'
