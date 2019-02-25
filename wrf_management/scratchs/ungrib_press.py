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
import wrf_management.run_utilities
import wrf_management.utilities
import wrf_management.utilities as ut
import importlib
importlib.reload(ut);
import wrf_management.project_global_constants as gc
importlib.reload(gc)
import wrf_management.geogrid as geo
import wrf_management.ungrib as un
import os
import sqlite3 as sq
import pandas as pd
import wrf_management.base_namelists.base_namelists as bn
importlib.reload(bn);
import f90nml
import tarfile

# %%
print(gc.RUN_NAME)
job = 'ungrib_press'
file_types = ['press']
real = False

LIST_S_LINKS = [
    'ungrib',
    'ungrib.exe',
    'link_grib.csh',
]

LIST_H_LINKS = [
    'Vtable',
    'env_WRFv4.bash'
]


# %%
con = sq.connect(gc.PATH_DB)

# %%
importlib.reload(un)
run_row = wrf_management.run_utilities.get_run_row()
print(run_row)

job_row = wrf_management.run_utilities.get_next_row(job=job)
print(job_row)
wrf_management.run_utilities.update_run_table(val=job_row[job] + 1,
                                              job=job,
                                              date=job_row['date']
                                              )
job_path = wrf_management.run_utilities.getmk_job_path(run_row, job_row, job)
print(job_path)

untar_path = os.path.join(job_path,'untar')

conf_path = wrf_management.run_utilities.get_conf_path(run_row)
print(conf_path)

type_rows = pd.DataFrame([un.get_type_row(ft,job_row) for ft in file_types])
print(type_rows)

name_list = un.skim_namelist_copy(
    conf_path,job_path,date =job_row.date,prefix=job
)
print(name_list)

if gc.ID=='taito_login':
    wrf_management.run_utilities.copy_hard_links(conf_path, job_path, LIST_H_LINKS)
    wrf_management.run_utilities.copy_soft_links(gc.PATH_WPS, job_path, LIST_S_LINKS)
    importlib.reload(un)
    un.untar_the_files(type_rows,joba_path)

# %%
r = type_rows.iloc[0]
type_ = r.type
source_tar_path = gc.FILE_TYPES[type_]['data_tar']
source_tar_path = os.path.join(
    gc.PATH_DATA,
    source_tar_path,
    r['name']
)


# %%
tf=tarfile.TarFile(source_tar_path)

# %%
tf.getmembers()

# %%
importlib.reload(un)
date_formated= wrf_management.utilities.date_file_format(job_row.date)

# %%
job_row

# %%
val = job_row[job]+1
print(val)
sql = """
update {tb}
set {job} = {val}
where date('{dt}')=date(date)
""".format(dt=job_row.date,tb=gc.RUN_NAME,val=val,job=job)
print(sql)

# %%
con = sq.connect(gc.PATH_DB)
try: 
    cu = con.cursor()
    cu.execute(sql)
    con.commit()
finally: 
    con.close()


# %%

