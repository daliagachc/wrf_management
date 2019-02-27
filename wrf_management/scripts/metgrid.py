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
import importlib
import wrf_management.project_global_constants as gc
import wrf_management.ungrib as un
import os
import pandas as pd
import subprocess as su
import wrf_management.run_utilities as ru
import wrf_management.metgrid as me

# %%
print(gc.RUN_NAME)
job = 'metgrid'
ungrib_source_dirs = ['ungrib_surf', 'ungrib_press']
avg_pref = 'ungrib_avgtsfc'
real = True
hours=24
LIST_S_LINKS = [
    'metgrid.exe',
    #     'link_grib.csh',
    'metgrid'
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
importlib.reload(me)
name_list = me.skim_namelist_copy_metgrid(
    conf_path, job_path, date=job_row.date, prefix=job, hours=hours
)
pd.DataFrame(name_list)

# %%

importlib.reload(un)
un.link_grub_files(ungrib_prefixes=ungrib_source_dirs, job_path=job_path)

# %%
importlib.reload(me)
me.get_geo_files(
    run_path=run_path,
    geo_rel_path=run_row.geogrid_path)
me.link_geo_files(
    geo_rel_path=run_row.geogrid_path,
    run_path=run_path,
    job_path=job_path
)

# %%
importlib.reload(me)
me.link_avg_file(prefix=avg_pref, job_path=job_path)

# %%
# if gc.ID=='taito_login':
ru.copy_hard_links(conf_path, job_path, LIST_H_LINKS)
ru.copy_soft_links(
    os.path.join(gc.PATH_WPS, ''),
    job_path, LIST_S_LINKS)

# %%

# %%
run_script = \
   """#!/bin/bash
   source ./env_WRFv4.bash
   srun -n1 -t10 ./metgrid.exe""".format(job_path=job_path)
print(run_script)
bs_path = os.path.join(job_path, 'run_me.sh')
bs_file = open(bs_path, 'w')
bs_file.write(run_script)
bs_file.close()


# %%
if gc.ID == 'taito_login':
    res = su.run(['/bin/bash','run_me.sh'], stdout=su.PIPE, stderr=su.PIPE,cwd=job_path)

# %%
print(res.stdout)
print(res.stderr)
if gc.ID == 'taito_login' and res.returncode == 0:
    un.update_run_table(val=100,
                        job=job,
                        date=job_row['date']
                        )

# %%
