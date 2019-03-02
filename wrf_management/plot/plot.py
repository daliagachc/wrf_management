# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

import os
import pandas as pd
import wrf_management.project_global_constants as gc
import xarray as xr


def get_df_list(*, path, pref='wrfout_d'):
    fs = os.listdir(path)
    df = pd.DataFrame(fs, columns=['fn'])
    _b = df.fn.str.startswith(pref)
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


def get_subdf_in_multin(df: pd.DataFrame, ind: str, val):
    _bool = df.index.get_level_values(ind) == val
    return df[_bool]


def get_index_from_xr(xd, par, lm, lM, sel1):
    # lm, lM = -21, -20
    # par = 'XLAT'
    # sel1 = 'west_east'
    arr = xd[par].isel({'Time': 0, sel1: 0})
    arr = arr.drop(par)
    adf = arr.to_dataframe()
    c1 = adf[par] > lm
    c2 = adf[par] < lM
    ind = adf[c1 & c2].index
    im, iM = ind.min(), ind.max()
    return im, iM


def get_coords_from_la_lo(xd, ll_dic):
    lam = ll_dic['lam']
    laM = ll_dic['laM']
    lom = ll_dic['lom']
    loM = ll_dic['loM']
    par = 'XLAT'
    sel1 = 'west_east'
    snm, snM = get_index_from_xr(xd, par, lam, laM, sel1)

    par = 'XLONG'
    sel1 = 'south_north'
    wem, weM = get_index_from_xr(xd, par, lom, loM, sel1)

    rd = {'wem': wem, 'weM': weM, 'snm': snm, 'snM': snM}
    return rd
