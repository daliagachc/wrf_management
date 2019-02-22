# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import shutil
import tarfile
from collections import OrderedDict

import wrf_management.utilities as ut
import wrf_management.project_global_constants as gc
import os
import sqlite3 as sq
import pandas as pd
import wrf_management.base_namelists.base_namelists as bn
import f90nml


def get_run_row(run_name=gc.RUN_NAME):
    sql: str = '''
    select * from '{rt}' where run_name='{rn}'
    '''
    sql = sql.format(rt=gc.RUNS_TB_NAME, rn=run_name)
    con = sq.connect(gc.PATH_DB)

    try:
        run_row = pd.read_sql(sql, con).iloc[0]
    finally:
        con.close()
    return run_row


def get_next_row(*, job, run_name=gc.RUN_NAME):
    sql: str = '''
    select * from {rn}
    where {job}<100
    order by date,'{job}'
    limit 1
    '''
    sql = sql.format(rn=run_name, job=job)
    con = sq.connect(gc.PATH_DB)
    try:
        job_row = pd.read_sql(sql, con).iloc[0]
    finally:
        con.close()
    return job_row


def getmk_job_path(run_row, job_row, job):
    date = pd.to_datetime(job_row.date).strftime('%Y_%m_%d')
    job_path = os.path.join(
        gc.PATH_DATA, run_row.data_path, date, job
    )
    os.makedirs(job_path, exist_ok=True)
    return job_path


def get_conf_path(run_row):
    conf_path = os.path.join(
        gc.PACKAGE_PATH, 'config_dir', run_row.config_path
    )
    return conf_path


def get_type_row(file_type, job_row):
    sql: str = '''
    select * from '{ft}' where date(date)=date('{dt}')
    '''
    sql = sql.format(ft=file_type, dt=job_row.date)
    con = sq.connect(gc.PATH_DB)

    try:
        type_row = pd.read_sql(sql, con).iloc[0]
        type_row['type'] = file_type
    finally:
        con.close()
    return type_row


def untar_the_files(type_rows, untar_path,data_path=gc.PATH_DATA):
    for l,r in type_rows.iterrows():
        type = r.type
        source_tar_path = gc.FILE_TYPES[type]['data_tar']
        source_tar_path = os.path.join(
            data_path,
            source_tar_path,
            r['name']
        )
        print(source_tar_path)
        tf=tarfile.TarFile(source_tar_path)
        tf.extractall(untar_path)


def copy_soft_links(source_path, target_path, list_files):
    for f in list_files:
        target_file_path = os.path.join(target_path, f)

        if os.path.isfile(target_file_path):
            print('unilinking')
            os.unlink(target_file_path)

        os.symlink(
            os.path.join(source_path, f, ),
            target_file_path
        )
        print(f)


def copy_hard_links(source_path, target_path, list_files):
    for f in list_files:
        target_file_path = os.path.join(target_path, f)

        if os.path.isfile(target_file_path):
            os.remove(target_file_path)

        shutil.copy2(
            os.path.join(source_path, f, ),
            target_file_path
        )
        print(f)


def skim_namelist_copy(
        input_path, output_path, *, date, prefix
):
    old_dic = f90nml.read(os.path.join(input_path, 'namelist.wps'))

    dt_object = pd.to_datetime(date)
    d_init = dt_object.strftime('%Y-%m-%d_%T')
    d_end = dt_object + pd.DateOffset(hours=18)
    d_end = d_end.strftime('%Y-%m-%d_%T')

    old_dic['share']['start_date'] = old_dic['share']['max_dom'] * [d_init]
    old_dic['share']['end_date'] = old_dic['share']['max_dom'] * [d_end]
    old_dic['share']['interval_seconds'] = 6 * 3600
    old_dic['ungrib']['prefix'] = prefix
    sections = ['share', 'ungrib']
    drops = {}
    new_dic = OrderedDict()
    for s in sections:
        new_dic[s] = old_dic[s]
        if s in drops.keys():
            for d in drops[s]:
                new_dic[s].pop(d)
    f90nml.write(
        new_dic,
        os.path.join(output_path, 'namelist.wps'),
        force=True
    )
    return new_dic
