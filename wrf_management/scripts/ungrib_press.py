# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.0.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import wrf_management.run_utilities
import wrf_management.utilities as ut
import importlib
importlib.reload(ut);
import wrf_management.project_global_constants as gc
importlib.reload(gc)
import wrf_management.geogrid as geo
import wrf_management.ungrib as un
importlib.reload(un)
import os
import sqlite3 as sq
import pandas as pd
import wrf_management.base_namelists.base_namelists as bn
importlib.reload(bn);
import f90nml
import subprocess as su
# %%
print(gc.RUN_NAME)
job = 'ungrib_press'
file_types=['press']

real = True
hours = 24

LIST_S_LINKS = [
    'ungrib.exe',
    'link_grib.csh',
    'ungrib'
]

LIST_H_LINKS = [
    'Vtable',
    'env_WRFv4.bash'
]


# %%
#con = sq.connect(gc.PATH_DB)
gc.PATH_DB

# %%
importlib.reload(un)
run_row = wrf_management.run_utilities.get_run_row()
print(run_row)

job_row = wrf_management.run_utilities.get_next_row(job=job,i_max=10)
print(job_row)



job_path = wrf_management.run_utilities.getmk_job_path(run_row, job_row, job)
print(job_path)

wrf_management.run_utilities.rm_if_path_exists(
    os.path.join(job_path, 'ungrib.log')
)

wrf_management.run_utilities.update_run_table(val=job_row[job] + 1,
                                              job=job,
                                              date=job_row['date']
                                              )

conf_path = wrf_management.run_utilities.get_conf_path(run_row)
print(conf_path)

type_rows = pd.DataFrame([un.get_type_row(ft, job_row) for ft in file_types])
print(type_rows)

name_list = un.skim_namelist_copy(
    conf_path, job_path, date=job_row.date, prefix=job, hours=hours
)
print(name_list)

# %%
if gc.ID=='taito_login':
    wrf_management.run_utilities.copy_hard_links(conf_path, job_path, LIST_H_LINKS)
    wrf_management.run_utilities.copy_soft_links(gc.PATH_WPS, job_path, LIST_S_LINKS)
    importlib.reload(un)
    un.untar_the_files(type_rows, job_path, job_row=job_row)
    
    # in case we need to download the day before
    if job == 'ungrib_press':
        pre_row = wrf_management.run_utilities.get_prev_row(job=job, job_row=job_row)
        trs = pd.DataFrame([un.get_type_row(ft, pre_row) for ft in file_types])
        un.untar_the_files_prev(trs, job_path, job_row=pre_row)

# %%
str(job_row.date)

# %%
run_script = \
    """#!/bin/bash
        
cd {job_path}
./link_grib.csh ./untar/*/*
source ./env_WRFv4.bash 
srun -t20 -p serial --mem 1000 -n1 -J'p{date}' ./ungrib.exe
exit $?
    """.format(job_path=job_path, date=str(job_row.date))
print(run_script)
bs_path = os.path.join(job_path, 'run_me.sh')
bs_file = open(bs_path, 'w')
bs_file.write(run_script)
bs_file.close()

# %%
if gc.ID == 'taito_login':
    res = su.run(['/bin/bash', bs_path], stdout=su.PIPE, stderr=su.PIPE)

# %%
print(res.stdout)
print(res.stderr)

# %%
print(res.returncode)

# %%
if gc.ID == 'taito_login' and res.returncode == 0:
    wrf_management.run_utilities.update_run_table(val=100,
                                                  job=job,
                                                  date=job_row['date']
                                                  )

# %%
job

# %%
