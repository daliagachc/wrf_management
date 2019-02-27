# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import glob
import os

import wrf_management.project_global_constants as gc
from datetime import datetime as dt
import pandas as pd
import f90nml
import wrf_management.run_utilities as ru
import wrf_management.utilities as ut

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
            input_dic['time_control'][key] = 4*[getattr(dt, p)]
    return input_dic


def get_input_file_path(run_name: str) -> str:
    res = os.path.join(gc.PACKAGE_PATH, 'config_dir', run_name, NAMELIST_INPUT)
    return res


def get_input_dic(file_path):
    return f90nml.read(file_path)


def create_run_type_dir(data_path, run_path, type_path):
    ret = os.path.join(data_path, 'runs', run_path, type_path)
    os.makedirs(ret, exist_ok=True)
    return ret


def write_input_dic(
        run_type_dir, new_input_dic
):
    f90nml.write(new_input_dic,
                 os.path.join(run_type_dir, NAMELIST_INPUT),
                 run_type_dir)


def get_metgrid_path(*, parent_run_path, date):
    ds = date.strftime('%Y_%m_%d')
    ret = os.path.join(parent_run_path, ds, 'metgrid')
    return ret


def link_metgrids_single(
        *, parent_run_path, date, dest_path
):
    met_path = get_metgrid_path(parent_run_path=parent_run_path,
                                date=date)
    sources = glob.glob(met_path + '/met_em*')
    for s in sources:
        dest = os.path.basename(s)
        dest = os.path.join(dest_path, dest)
        ru.relink(source_file_path=s, dest_file_path=dest)


def link_metgrids(*, parent_run_path, dates, dest_path):
    for d in dates:
        link_metgrids_single(parent_run_path=parent_run_path,
                             date=d,
                             dest_path=dest_path)


def link_real(
        *, wrf_path=gc.PATH_WRF, dest_path
    ):
    source = os.path.join(wrf_path, 'main/real.exe')
    target = os.path.join(dest_path, 'real.exe')
    ru.relink(source_file_path=source,
              dest_file_path=target)

