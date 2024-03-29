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
import pathlib
# %%
print(gc.RUN_NAME)
job = 'ungrib_avgtsfc'
ungrib_source_dirs = ['ungrib_surf', 'ungrib_press']

real = True
hours = 24

LIST_S_LINKS = [
    'avg_tsfc.exe',
#     'link_grib.csh',
#     'ungrib'
]

LIST_H_LINKS = [
#     'Vtable',
    'env_WRFv4.bash'
]


# %%
#con = sq.connect(gc.PATH_DB)
gc.PATH_DB

# %%
importlib.reload(un)
run_row = wrf_management.run_utilities.get_run_row()
print(run_row)

# %%
job_row = wrf_management.run_utilities.get_next_row(job=job, i_max=10)
print(job_row)

# %%
if real:
    wrf_management.run_utilities.update_run_table(val=job_row[job] + 1,
                                                  job=job,
                                                  date=job_row['date']
                                                  )

job_path = wrf_management.run_utilities.getmk_job_path(run_row, job_row, job)
print(job_path)

wrf_management.run_utilities.rm_if_path_exists(
    os.path.join(job_path, 'avg_tsfc.log')
)

# %%
conf_path = wrf_management.run_utilities.get_conf_path(run_row)
print(conf_path)

# %%
importlib.reload(un)
name_list = un.skim_namelist_copy_avgtsfc(
    conf_path, job_path, date=job_row.date, prefix=job, hours=24
)
pd.DataFrame(name_list)

# %%

importlib.reload(un)
un.link_grub_files(ungrib_prefixes=ungrib_source_dirs, job_path=job_path)

# %%
# if gc.ID=='taito_login':
wrf_management.run_utilities.copy_hard_links(conf_path, job_path, LIST_H_LINKS)
wrf_management.run_utilities.copy_soft_links(
    os.path.join(gc.PATH_WPS,'util'),
    job_path,LIST_S_LINKS)
    


# %%
run_script = \
    """#!/bin/bash
        
cd {job_path}
source ./env_WRFv4.bash 
srun -t10 -p serial --mem 1000 -J'a{date}' ./avg_tsfc.exe > avg_tsfc.log
exit $?
    """.format(job_path=job_path, date = job_row.date)
print(run_script)
bs_path = os.path.join(job_path, 'run_me.sh')
bs_file = open(bs_path, 'w')
bs_file.write(run_script)
bs_file.close()

# %%
if gc.ID == 'taito_login':
    res = su.run(['/bin/bash', bs_path], stdout=su.PIPE, stderr=su.PIPE)

print(res.stdout)
print(res.stderr)
if gc.ID == 'taito_login' and res.returncode == 0:
    wrf_management.run_utilities.update_run_table(val=100,
                                                  job=job,
                                                  date=job_row['date']
                                                  )

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%



