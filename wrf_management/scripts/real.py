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
import wrf_management.project_global_constants as gc
import wrf_management.ungrib as un
import os
import pandas as pd
import subprocess as su
import wrf_management.run_utilities as ru
import wrf_management.real as re

# %%
print(gc.RUN_NAME)
job = 'real'
met_pref='metgrid'
real = False

LIST_S_LINKS = [
    'real.exe',
    #     'link_grib.csh',
#     'metgrid'
]

LIST_H_LINKS = [
    #     'Vtable',
    'env_WRFv4.bash'
]

# %%
# con = sq.connect(gc.PATH_DB)
gc.PATH_DB

# %%
importlib.reload(un)
importlib.reload(ru)
run_row = ru.get_run_row()
print(run_row)

# %%
run_path = os.path.join(gc.PATH_DATA, run_row.data_path)
print(run_path)

# %%
job_row = ru.get_next_row(job=job)
print(job_row)

# %%
if real:
    ru.update_run_table(val=job_row[job] + 1,
                        job=job,
                        date=job_row['date']
                        )

job_path = ru.getmk_job_path(run_row, job_row, job)
print(job_path)

# %%
conf_path = ru.get_conf_path(run_row)
print(conf_path)

# %%


# %%
duration_h = 24
importlib.reload(re)
re.skim_namelist_copy_real(
    conf_path, job_path, date = job_row.date, 
    duration_h=duration_h
);

# %%
importlib.reload(re)


re.link_met_files(
    job_path=job_path,
    met_pref=met_pref
)

# %%
# if gc.ID=='taito_login':
ru.copy_hard_links(conf_path, job_path, LIST_H_LINKS)
ru.copy_soft_links(
    os.path.join(gc.PATH_WPS, ''),
    job_path, LIST_S_LINKS)

# %%
run_script = \
    """#!/bin/bash
    cd {job_path}
    source ./env_WRFv4.bash 
    ./metgrid.exe
    exit $?
    """.format(job_path=job_path)
print(run_script)
bs_path = os.path.join(job_path, 'run_me.sh')
bs_file = open(bs_path, 'w')
bs_file.write(run_script)
bs_file.close()

# %%
if gc.ID == 'taito_login':
    res = su.run(['/bin/bash', bs_path], stdout=su.PIPE, stderr=su.PIPE)

if gc.ID == 'taito_login' and res.returncode == 0:
    un.update_run_table(val=100,
                        job=job,
                        date=job_row['date']
                        )

# %%


