# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

import os
import pandas as pd
import wrf_management.project_global_constants as gc
import xarray as xr


def get_df_list(*, path):
    fs = os.listdir(path)
    df = pd.DataFrame(fs, columns=['fn'])
    _b = df.fn.str.startswith('wrfout_d')
    df = df[_b].reset_index(drop=True)
    df['p'] = df.fn.apply(lambda f: os.path.join(path, f))
    df['d'] = df.fn.str.extract('d0(.)').astype(int)
    df['date'] = pd.to_datetime(df.fn.str.slice(11, 30), format='%Y-%m-%d_%H:%M:%S')
    df = df.set_index(['date', 'd'])
    df = df.sort_values(['date', 'd'])
    return df


def print_var_starting_with(path, start_string):
    xar = xr.open_dataset(path)
    ser = pd.Series(list(xar.variables))
    li = ser[ser.str.startswith(start_string)]
    li = list(li)
    for l in li:
        va = xar[l]
        #     print(va)
        try:
            des = va.attrs['description']
        except:
            des = ''
        print(l, '-', des)
        print('---------------')
