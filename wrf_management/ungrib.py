# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import pathlib
import tarfile
from collections import OrderedDict

import wrf_management.project_global_constants as gc
import os
import sqlite3 as sq
import pandas as pd
import f90nml

from wrf_management.utilities import date_file_format
from wrf_management.run_utilities import get_run_row, get_next_row, get_prev_row, getmk_job_path, get_conf_path, \
    copy_soft_links, copy_hard_links, update_run_table, relink


def MIGRATED_FUNS():
    [
        date_file_format,
        get_run_row,
        get_next_row,
        get_prev_row,
        getmk_job_path,
        get_conf_path,
        copy_soft_links,
        copy_hard_links,
        update_run_table,
        relink,

    ]


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


def skim_namelist_copy(
        input_path, output_path, *, date, prefix, hours=18
):
    old_dic = f90nml.read(os.path.join(input_path, 'namelist.wps'))

    dt_object = pd.to_datetime(date)
    d_init = dt_object.strftime('%Y-%m-%d_%T')
    d_end = dt_object + pd.DateOffset(hours=hours)
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
        input_path, output_path, *, date, prefix, hours=18
):
    old_dic = f90nml.read(os.path.join(input_path, 'namelist.wps'))

    dt_object = pd.to_datetime(date)
    d_init = dt_object.strftime('%Y-%m-%d_%T')
    d_end = dt_object + pd.DateOffset(hours=hours)
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


def get_ungrib_files_for_avg(
        *, job_path, pre
):
    pre_path = pathlib.Path(job_path).parent
    pre_path = os.path.join(pre_path, pre)
    # print(pre_path)
    import glob
    file_list = glob.glob(os.path.join(pre_path, pre + ':*'))
    return file_list


def link_grub_files(
        *, ungrib_prefixes, job_path
):
    for pre in ungrib_prefixes:
        ungrib_list = get_ungrib_files_for_avg(job_path=job_path, pre=pre)
        df = pd.DataFrame(ungrib_list, columns=['source'])
        df['base_name'] = df['source'].apply(lambda p: os.path.basename(p))
        df['dest'] = df['base_name'].apply(lambda bn: os.path.join(job_path, bn))
        df.apply(lambda r: relink(r['source'], r['dest']), axis=1)
