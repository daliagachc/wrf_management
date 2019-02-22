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
job = 'ungrib_surf'
file_types = ['surf_0', 'surf_1']
# job = 'ungrib_press'
# file_types = ['press']
real = False

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
# con = sq.connect(gc.PATH_DB)
gc.PATH_DB

# %%
importlib.reload(un)
run_row = un.get_run_row()
print(run_row)

job_row = un.get_next_row(job=job)
print(job_row)

un.update_run_table(val=job_row[job] + 1,
                    job=job,
                    date=job_row['date']
                    )

job_path = un.getmk_job_path(run_row, job_row, job)
print(job_path)

conf_path = un.get_conf_path(run_row)
print(conf_path)

type_rows = pd.DataFrame([un.get_type_row(ft, job_row) for ft in file_types])
print(type_rows)

name_list = un.skim_namelist_copy(
    conf_path, job_path, date=job_row.date, prefix=job
)
print(name_list)

if gc.ID == 'taito_login':
    un.copy_hard_links(conf_path, job_path, LIST_H_LINKS)
    un.copy_soft_links(gc.PATH_WPS, job_path, LIST_S_LINKS)
    importlib.reload(un)
    un.untar_the_files(type_rows, job_path)
    
    # in case we need to download the day before
    if job == 'ungrib_surf':
        pre_row = un.get_prev_row(jon,job_row)
        trs = pd.DataFrame([un.get_type_row(ft, pre_row) for ft in file_types])
        un.untar_the_files(trs, job_path)

run_script = \
    """#!/bin/bash
    cd {job_path}
    ./link_grib.csh ./untar/*
    source ./env_WRFv4.bash 
    ./ungrib.exe
    exit $?
    """.format(job_path=job_path)
print(run_script)
bs_path = os.path.join(job_path, 'run_me.sh')
bs_file = open(bs_path, 'w')
bs_file.write(run_script)
bs_file.close()
if gc.ID == 'taito_login':
    res = su.run(['/bin/bash', bs_path], stdout=su.PIPE, stderr=su.PIPE)

if gc.ID == 'taito_login' and res.returncode == 0:
    un.update_run_table(val=100,
                        job=job,
                        date=job_row['date']
                        )

# %%
day_bef = pd.to_datetime(job_row.date) - pd.to_timedelta(1, "D")
day_bef = str(day_bef)

# %%
run_name = gc.RUN_NAME
sql: str = '''
select * from {rn}
where date(date)=date('{dt}')
limit 1
'''
sql = sql.format(rn=run_name, dt=day_bef)
con = sq.connect(gc.PATH_DB)
try:
    job_row = pd.read_sql(sql, con).iloc[0]
finally:
    con.close()
print(job_row)
# return job_row


# %%
import tarfile
r = type_rows.iloc[0]
data_path = gc.PATH_DATA
date = un.date_file_format(job_row.date)
untar_path = os.path.join(job_path, 'untar', date)
_type = r.type
source_tar_path = gc.FILE_TYPES[_type]['data_tar']
source_tar_path = os.path.join(
    data_path,
    source_tar_path,
    r['name']
)
print(source_tar_path)
tf = tarfile.TarFile(source_tar_path)
# tf.extractall(untar_path)

# %%
members = tf.getmembers()
for m in members:
    name = m.name
    if name == 'cdas1.t18z.splgrbf06.grib2':
        print(name)
        tf.extract(m,untar_path)
    

# %%
untar_path

# %%

