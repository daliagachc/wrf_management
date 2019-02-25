# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import glob
import os
import pathlib
from collections import OrderedDict
import wrf_management.project_global_constants as gc
import sqlite3 as sq
import pandas as pd
import wrf_management.run_utilities as ru

import f90nml


def skim_namelist_copy_real(
        input_path, output_path, *, date, duration_h
):
    old_dic = f90nml.read(os.path.join(input_path, 'namelist.input'))

    s_dt = pd.to_datetime(date)
    e_dt = s_dt + pd.Timedelta(duration_h, 'h')

    d_list = [
        ['start_year', s_dt.year],
        ['start_month', s_dt.month],
        ['start_day', s_dt.day],
        ['start_hour', s_dt.hour],
        ['end_year', e_dt.year],
        ['end_month', e_dt.month],
        ['end_day', e_dt.day],
        ['end_hour', e_dt.hour],
        # ['end_second', e_dt.second],
    ]

    for k, v in d_list:
        # print(k)
        # print(v)
        old_dic['time_control'][k] = 4*[v]
    f90nml.write(
        old_dic,
        os.path.join(output_path, 'namelist.input'),
        force=True
    )
    return old_dic


def get_met_files(
        *, job_path, met_pref
):
    met_path = pathlib.Path(job_path).parent
    pre_path = os.path.join(met_path, met_pref)
    # print(pre_path)
    file_list = glob.glob(os.path.join(pre_path, 'met_em.d' + '*'))
    return file_list


def link_met_files(
        *,
        job_path, met_pref
):
    met_list = get_met_files(
        job_path=job_path,
        met_pref=met_pref)

    df = pd.DataFrame(met_list, columns=['source'])

    df['base_name'] = df['source'].apply(
        lambda p: os.path.basename(p)
    )

    df['dest'] = df['base_name'].apply(
        lambda bn: os.path.join(job_path, bn)
    )

    df.apply(
        lambda r: ru.relink(r['source'], r['dest']),
        axis=1
    )
