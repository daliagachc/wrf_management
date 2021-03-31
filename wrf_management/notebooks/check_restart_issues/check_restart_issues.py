# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # imports

# %%
from useful_scit.imps import (
    pd,np,xr,za,mpl,plt,sns, pjoin, 
    os,glob,dt,sys,ucp,log, splot, crt,axsplot)
import re
import wrf_management.modules.util as wutil

# %% [markdown]
# # code 

# %%
flx_path = '/homeappl/home/aliagadi/appl_taito/' +\
'FLEXPART-WRF_v3.3.2/readwind_nests.f90'

# %%
with open(flx_path, 'r') as op:
    txt = op.read()

# %%
_vars = re.findall(r'\ *?[^!\n]*?varname\ *=\ *\'(.+)\'',txt)

# %%
var = 'var'
df_v = pd.DataFrame(_vars,columns=[var])
df_v = df_v.sort_values(var).reset_index(drop=True)

# %%
df_v = df_v.drop_duplicates().copy()

# %% [markdown]
# ## WRF files

# %%
wrf_path = \
'/proj/atm/saltena/runs/run_2019_05_15/' +\
'wrf/wrfout_d0*2018-03-08_*'


# %%
wrf_path = '/proj/atm/saltena/runs/run_2019_05_15/wrf/'

# %%
wrf_files = wutil.get_df_list(path=wrf_path)

# %%
_i = 1
_s = slice('2018-03-08 14','2018-03-08 16')
_wr = wrf_files.loc[(_s,_i),:]

# %%
p = _wr.iloc[0]['p']
_ds = xr.open_dataset(p)

# %%
var = 'var'

def _find_exists(r,ds):
    va = r['var']
    ret = False
    try: ds[va];ret=True
    except: pass
    return ret

def _find_dims(r,ds):
    va = r['var']
    ret = 0
    try: ret = len(ds[va].dims)
    except: pass
    return ret

def _find_time_dim(r,ds):
    va = r['var']
    ret = False
    try: ret = ('Time' in ds[va].dims)
    except: pass
    return ret
def _find_other_dim(r,ds):
    va = r['var']
    ret = False
    try: ret = list(set(list(ds[va].dims))-set(('Time',)))
    except: pass
    return ret

def _find_desc(r,ds):
    va = r['var']
    ret = False
    try: ret = ds[va].description
    except: pass
    return ret


# %%
exists = 'exists'
ndims = 'ndims'
tdim = 't_dim'
dims = 'dims'
desc = 'desc'

df_v[exists]=df_v.apply(lambda r: _find_exists(r,_ds),axis=1)
df_v[ndims]=df_v.apply(lambda r: _find_dims(r,_ds),axis=1)
df_v[tdim]=df_v.apply(lambda r: _find_time_dim(r,_ds),axis=1)
df_v[dims]=df_v.apply(lambda r: _find_other_dim(r,_ds),axis=1)
df_v[desc]=df_v.apply(lambda r: _find_desc(r,_ds),axis=1)

# %%
df_v1 = df_v[df_v[exists]]

# %% {"jupyter": {"outputs_hidden": true}}
df_v1

# %%
_id = 1
_s = slice('2018-03-08 14','2018-03-08 15')
_wr = wrf_files.loc[(_s,_id),:]

XTIME = 'XTIME'
Time = 'Time'
wds = xr.open_mfdataset(_wr['p'],concat_dim=Time,combine='nested')
wds = wds.swap_dims({Time:XTIME})

# %%

df_v1
row = df_v1.iloc[12]
va = row[var]
_wd = wds[va]
_wds = _wd.shift(**{XTIME:-1})
va

# %%
_der = _wds-_wd
_derAll = _der.loc[{XTIME:slice('2018-03-08 14:00','2018-03-08 14:30')}]
_derRes = _der.loc[{XTIME:slice('2018-03-08 14:45','2018-03-08 14:45')}]

# %%
derResult = _derRes.mean(XTIME)/(_derAll.mean(XTIME).where(
    np.abs(_derAll)>1e-1,1
))

# %%
ax = axsplot()
_res = pd.Series(derResult.values.flatten()).dropna().values
description = pd.DataFrame(_res,columns=[va]).describe()
sns.distplot(_res,kde=False,ax=ax, label = va);
ax.legend()
ax.set_title(f'dom:{_id}-{row[desc]}')
ax.table(
    cellText=description.values,
    rowLabels=description.index.values,
    colLabels=[va],
    cellLoc='left',
    bbox=[1.2,0,.5,1]
        )

# %%
(_derAll.mean(XTIME).where(_derAll!=0,1)).max().values

# %%
_derAll.mean(XTIME).where(~(_derAll==0),1).plot()

# %%
rr=((_derAll.mean(XTIME).where(_derAll!=0,1)).values==0).flatten().astype(int)

# %%
pd.Series(rr).value_counts()

# %%
wds['UST'][{}]

# %%
ucp.set_dpi(300)

# %%
for i in range(1,5):
    _id = i
    _s = slice('2018-03-08 14','2018-03-08 15')
    _wr = wrf_files.loc[(_s,_id),:]

    XTIME = 'XTIME'
    Time = 'Time'
    wds = xr.open_mfdataset(_wr['p'],concat_dim=Time,combine='nested')
    wds = wds.swap_dims({Time:XTIME})
    u1 = wds.loc[{XTIME:'2018-03-08 14:45'}]['UST']
    u2 = wds.loc[{XTIME:'2018-03-08 15:00'}]['UST']
    axs = axsplot(1,3,figsize=(11,3)).flatten()
    u1.plot(ax=axs[0]);
    u2.plot(ax=axs[1]);
    ((u2-u1)).plot(ax=axs[2]);
    axs[2].set_title(f'dom:{i} '+'$\\frac{u^*_2-u^*_1}{1}$');
    axs[2].figure.tight_layout()
    

# %%
# # !jupyter-nbconvert --to markdown check_restart_issues.ipynb

# %%
