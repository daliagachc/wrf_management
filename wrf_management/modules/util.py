# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''
general utilities for wrf management python
'''
from useful_scit.imps import (
    pd,np,xr,za,mpl,plt,sns, pjoin,
    os,glob,dt,sys,ucp,log, splot, crt)
from useful_scit.imps import *



def get_df_list(*, path, pref='wrfout_d')->pd.DataFrame:
    '''return a pd.DataFrame with a list of files from the path
    matching the pref[fix].

    Parameters
    ----------
    path:str
    pref:str

    Returns
    -------
    df

    '''
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


