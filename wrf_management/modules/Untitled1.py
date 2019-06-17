# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload

# %autoreload 2
from useful_scit.imps import *
import wrf

# %%
path = '/Volumes/mbProD/Downloads/wrf_cross/slices_chc_lapaz/wrfout_d04_*'

# %%
files = glob.glob(path)
files.sort()

# %%
i = 5
t = 1  
time = 'Time'
cl = 'cross_line_ll'
uv = 'u_v'
ver = 'vertical'
ws = 'wspd_wdir'
PBLH ='PBLH'
ter='ter'
TKE_PBL = 'TKE_PBL'



# %%
xa = xr.open_mfdataset(path,concat_dim='Time',)
# xa

# %%
df = xa[PBLH].to_pandas()

# %%

# %%
dt = 'day_time'
cl = 'cross_line_ll'

# %%

# %%
# df.drop(dt,inplace=True,axis=1)

# %%

# %%
d1 = pd.to_datetime('2000-01-01')
df1 = df.copy()
df1[dt] = d1 + (df1.index - (df1.index+pd.Timedelta(hours=12)).round('D'))

# %%
df1.groupby(dt).median().median(axis=1).plot()

# %%
nxa = df1.groupby(dt).median().stack().to_xarray()

# %%
nxa[cl]=nxa[cl].astype(int)

# %%
nxa.plot(x='day_time')

# %%
a1 = nxa.groupby('day_time.hour').median(dim='day_time')

# %%
a1[ter]=xa[ter][{time:0}]

# %%
a1.name=PBLH

# %%
a1 = a1.to_dataset()

# %%
a1['z']=a1[PBLH]+a1[ter]

# %%
a1['z']

# %%
a1['z'].plot(col='hour',col_wrap=6)

# %%
nxa.day_time.to_series().index.round('H')

# %%
