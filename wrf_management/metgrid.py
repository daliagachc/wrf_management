# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import os
import pathlib
from collections import OrderedDict
import wrf_management.project_global_constants as gc
import sqlite3 as sq
import pandas as pd
import wrf_management.run_utilities as ru

import f90nml


def skim_namelist_copy_metgrid(
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
    old_dic['metgrid']['constants_name'] = 'TAVGSFC'

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


def link_avg_file(
        *, prefix, job_path
):
    file_name = 'TAVGSFC'
    avg_path = pathlib.Path(job_path).parent
    file_path = os.path.join(avg_path, prefix, file_name)
    dest_path = os.path.join(job_path, file_name)
    ru.relink(file_path, dest_path)
