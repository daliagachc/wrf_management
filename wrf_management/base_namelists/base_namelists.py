# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo


import f90nml
import pandas as pd


def sanity_check(*,
                 path_wps, path_wrf, print_table=False
                 ):
    # path_wps = './namelist.wps'
    # path_wrf = './namelist.input'

    wps_dic = f90nml.read(path_wps)
    wrf_dic = f90nml.read(path_wrf)

    wps_df = pd.DataFrame(wps_dic)
    wrf_df = pd.DataFrame(wrf_dic)

    df_full = wrf_df.join(wps_df, how='outer')
    df_joined = wrf_df.join(wps_df, how='inner')

    df_drop = df_joined.dropna(how='all').dropna(how='all', axis=1)

    df_pass = {}
    for k, r in df_drop.iterrows():
        dd = r.dropna()
        d1 = dd.iloc[0]
        d2 = dd.iloc[1]
        #     print(k)
        if k in ['dx', 'dy']:
            d1 = float(d1[0])
            d2 = float(d2)

        df_pass[k] = {
            'pass': d1 == d2,
            'd1'  : dd.iloc[0],
            'd2'  : dd.iloc[1]
        }
    #     print(dd)
    res_df = pd.DataFrame(df_pass).T
    return res_df['pass'].all(), res_df, df_full
