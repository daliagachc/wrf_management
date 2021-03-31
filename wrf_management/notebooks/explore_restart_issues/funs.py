# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from useful_scit.imps import *

PATH = 'PATH'
DATE = 'DATE'
NAME = 'NAME'
DOM  = 'DOM'
KIND = 'KIND'
wrfrst = 'wrfrst'
wrfout = 'wrfout'
MONTH = 'MONTH'


TIME     = 'Time'
XTIME    = 'XTIME'
XLAT     = 'XLAT'
XLONG    = 'XLONG'
MAPFAC_M = 'MAPFAC_M'
PSFC     = 'PSFC'
U10      = 'U10'
V10      = 'V10'
T2       = 'T2'
Q2       = 'Q2'
SWDOWN   = 'SWDOWN'
RAINNC   = 'RAINNC'
RAINC    = 'RAINC'
HFX      = 'HFX'
UST      = 'UST'
PBLH     = 'PBLH'

VARS2D = [
    # XLAT    ,
    # XLONG   ,
    MAPFAC_M,
    PSFC    ,
    U10     ,
    V10     ,
    T2      ,
    Q2      ,
    SWDOWN  ,
    RAINNC  ,
    RAINC   ,
    HFX     ,
    UST     ,
    PBLH    ,
]

# 3d fields

PB     = 'PB'
P      = 'P'
PHB    = 'PHB'
PH     = 'PH'
T      = 'T'
QVAPOR = 'QVAPOR'
TKE    = 'TKE_PBL'

VARS3D = [
    PB    ,
    P     ,
    PHB   ,
    PH    ,
    T     ,
    QVAPOR,
    TKE   ,
]






def get_files_df(path):
    files = glob.glob(path + '/*_d*:*:*')
    df = pd.DataFrame(files, columns=[PATH])
    _df = df[PATH]
    _date = _df.str.slice(-19, None)
    _date = _date.str.replace('_', ' ')
    _date = pd.to_datetime(_date)
    df[DATE] = _date
    df = df.set_index(DATE).sort_index()
    df[NAME] = df[PATH].str.slice(-30, None)
    df[DOM] = df[PATH].str.slice(-21, -20).astype(int)
    df[KIND] = df[PATH].str.slice(-30, -24)
    df[MONTH] = df.index.month
    return df




















