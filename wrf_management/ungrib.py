# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import pathlib
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


def get_next_row(*, job, run_name=gc.RUN_NAME, i_max=1):
    sql: str = '''
    select * from {rn}
    where {job}<={i_max}
    order by {job},date
    limit 1
    '''
    sql = sql.format(rn=run_name, job=job, i_max=i_max)
    con = sq.connect(gc.PATH_DB)
    try:
        job_row = pd.read_sql(sql, con).iloc[0]
    finally:
        con.close()
    return job_row


def get_prev_row(*, job, run_name=gc.RUN_NAME, job_row):
    day_bef = pd.to_datetime(job_row.date) - pd.to_timedelta(1, "D")
    day_bef = str(day_bef)
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
    # print(job_row)
    return job_row


def getmk_job_path(run_row, job_row, job):
    date = date_file_format(job_row.date)
    job_path = os.path.join(
        gc.PATH_DATA, run_row.data_path, date, job
    )
    os.makedirs(job_path, exist_ok=True)
    return job_path


def date_file_format(date):
    return pd.to_datetime(date).strftime('%Y_%m_%d')


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


def untar_the_files_prev(
        type_rows,
        job_path,
        *,
        data_path=gc.PATH_DATA,
        job_row,
):
    for l, r in type_rows.iterrows():
        date = date_file_format(job_row.date)
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
        members = tf.getmembers()
        for m in members:
            name = m.name
            if 't18z' in name:
                print(name)
                tf.extract(m, untar_path)


def untar_the_files(
        type_rows,
        job_path,
        *,
        data_path=gc.PATH_DATA,
        job_row,
):
    for l, r in type_rows.iterrows():
        date = date_file_format(job_row.date)
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
        tf.extractall(untar_path)


def copy_soft_links(source_path, target_path, list_files):
    for f in list_files:
        target_file_path = os.path.join(target_path, f)

        if os.path.isfile(target_file_path):
            print('unilinking')
            os.unlink(target_file_path)

        if os.path.isdir(target_file_path):
            print('unilinking')
            os.unlink(target_file_path)


        if os.path.lexists(target_file_path):
            print('unilinking')
            os.remove(target_file_path)

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

        if os.path.isdir(target_file_path):
            os.remove(target_file_path)
        shutil.copy2(
            os.path.join(source_path, f, ),
            target_file_path
        )
        print(f)


def skim_namelist_copy(
        input_path, output_path, *, date, prefix,
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


def skim_namelist_copy_avgtsfc(
        input_path, output_path, *, date, prefix,
):
    old_dic = f90nml.read(os.path.join(input_path, 'namelist.wps'))

    dt_object = pd.to_datetime(date)
    d_init = dt_object.strftime('%Y-%m-%d_%T')
    d_end = dt_object + pd.DateOffset(hours=18)
    d_end = d_end.strftime('%Y-%m-%d_%T')

    old_dic['share']['start_date'] = old_dic['share']['max_dom'] * [d_init]
    old_dic['share']['end_date'] = old_dic['share']['max_dom'] * [d_end]
    old_dic['share']['interval_seconds'] = 6 * 3600
    old_dic['metgrid']['fg_name'] = ['ungrib_surf', 'ungrib_press']
    sections = ['share',
                # 'ungrib',
                'metgrid']
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


def update_run_table(
        *,
        run_name=gc.RUN_NAME,
        val,
        job,
        date,
        path_db=gc.PATH_DB
):
    # val = job_row[job]+1
    # print(val)
    sql = """
    update {tb}
    set {job} = {val}
    where date('{dt}')=date(date)
    """.format(dt=date, tb=run_name, val=val, job=job)
    # print(sql)

    con = sq.connect(path_db)
    try:
        cu = con.cursor()
        cu.execute(sql)
        con.commit()
    finally:
        con.close()


def get_ungrib_files_for_avg(
        *, job_path, pre
):
    pre_path = pathlib.Path(job_path).parent
    pre_path = os.path.join(pre_path, pre)
    # print(pre_path)
    import glob
    file_list = glob.glob(os.path.join(pre_path, pre + ':*'))
    return file_list


def relink(
        source_file_path, dest_file_path
):
    if os.path.lexists(dest_file_path):
        os.remove(dest_file_path)

    os.symlink(source_file_path, dest_file_path)


def link_grub_files(
        *, ungrib_prefixes, job_path
):
    for pre in ungrib_prefixes:
        ungrib_list = get_ungrib_files_for_avg(job_path=job_path, pre=pre)
        df = pd.DataFrame(ungrib_list, columns=['source'])
        df['base_name'] = df['source'].apply(lambda p: os.path.basename(p))
        df['dest'] = df['base_name'].apply(lambda bn: os.path.join(job_path, bn))
        df.apply(lambda r: relink(r['source'], r['dest']), axis=1)
