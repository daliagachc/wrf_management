# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import os

import wrf_management.project_global_constants as gc
from datetime import datetime as dt
import pandas as pd
import f90nml

# %%
NAMELIST_INPUT = 'namelist.input'


def get_date_range(
        init_date: dt, end_date: dt
) -> pd.DataFrame:
    dates = pd.date_range(init_date, end_date)
    df = pd.DataFrame(dates, columns=['dt'])
    return df


def link_data_file(

) -> pd.DataFrame:
    pass


def copy_executables(

) -> pd.DataFrame:
    pass


def modify_dt_input_dic(
        init_date, end_date, input_dic
):
    dt_dic = {'start': init_date, 'end': end_date}
    pars = {'year', 'month', 'day', 'hour', 'minute', 'second'}

    for k, dt in dt_dic.items():
        for p in pars:
            key = k + '_' + p
            input_dic['time_control'][key] = getattr(dt, p)
    return input_dic


def get_input_file_path(run_name: str) -> str:
    res = os.path.join(gc.PACKAGE_PATH, 'config_dir', run_name, NAMELIST_INPUT)
    return res


def get_input_dic(file_path):
    return f90nml.read(file_path)


def create_run_type_dir(data_path, run_path, type_path):
    ret = os.path.join(data_path, run_path, type_path)
    os.makedirs(ret, exist_ok=True)
    return ret


def write_input_dic(
        run_type_dir, new_input_dic
):
    f90nml.write(new_input_dic,
                 os.path.join(run_type_dir, NAMELIST_INPUT),
                 run_type_dir)
