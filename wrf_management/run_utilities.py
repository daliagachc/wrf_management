# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import os
import shutil
import sqlite3 as sq

import pandas as pd

from wrf_management import project_global_constants as gc
from wrf_management.utilities import date_file_format


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


def get_conf_path(run_row):
    conf_path = os.path.join(
        gc.PACKAGE_PATH, 'config_dir', run_row.config_path
    )
    return conf_path


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


def relink(
        source_file_path, dest_file_path
):
    rm_if_path_exists(dest_file_path)

    os.symlink(source_file_path, dest_file_path)


def rm_if_path_exists(dest_file_path):
    ifs = [
        os.path.lexists,
        os.path.isfile,
        os.path.isdir,
    ]
    for f in ifs:
        if f(dest_file_path):
            os.remove(dest_file_path)


def is_log_success(log_path, succes_str):
    try:
        with open(log_path, 'r') as f:
            log_str = f.read()
            success = (succes_str in log_str)
    except:
        success = False

    return success


def get_logpath(log_name, row_date, run_name, ungrib_type):
    path_run = os.path.join(
        gc.PATH_DATA, 'runs', run_name, date_file_format(row_date), ungrib_type
    )
    path_run
    log_path = os.path.join(path_run, log_name)
    log_path
    return log_path


def get_1_df(tb_name, ungrib_type, lim=1):
    sql = '''
    select * from {tb} where {ut}<{lim} 
    '''
    sql = sql.format(tb=tb_name, ut=ungrib_type, lim=lim)
    con = sq.connect(gc.PATH_DB)
    try:
        df = pd.read_sql(sql, con)
        con.commit()
    finally:
        con.close()
    return df


def is_log_success_from_row(log_name, row, run_name, succes_str, ungrib_type):
    row_date = row.date
    log_path = get_logpath(log_name, row_date, run_name, ungrib_type)
    success = is_log_success(log_path, succes_str)
    return success


def update_table_True(*,
                      row, tb_name, path_db=gc.PATH_DB,
                      ungrib_type, true_val=100
                      ):
    update_table(path_db, row, tb_name, true_val, ungrib_type)


def update_table_False(*,
                       row, tb_name, path_db=gc.PATH_DB,
                       ungrib_type, true_val=5
                       ):
    update_table(path_db, row, tb_name, true_val, ungrib_type)


def update_table(path_db, row, tb_name, true_val, ungrib_type):
    sql = '''
    update {tb_name}
    set {ungrib_type}={true_val}
    where date(date)=date('{date}')
    '''
    sql = sql.format(tb_name=tb_name, ungrib_type=ungrib_type,
                     date=row.date, true_val=true_val)
    # print(sql)
    con = sq.connect(path_db)
    try:
        p = con.cursor()
        p.execute(sql)
        con.commit()
    finally:
        con.close()


def update_rows(
        row, tb_name, ungrib_type, true_val=100,false_val=5
):
    if row.success:
        update_table_True(
            row=row, tb_name=tb_name, ungrib_type=ungrib_type, true_val=true_val)
    else:
        update_table_False(
            row=row, tb_name=tb_name, ungrib_type=ungrib_type, true_val=false_val)
