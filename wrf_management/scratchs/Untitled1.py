# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import wrf_management.project_global_constants as gc
import wrf_management.utilities as ut
import os 
import pandas as pd 
import xarray as xr
import di_python.ya_esta as ye

# %%
path = os.path.join(gc.PATH_DATA,'runs/run_2019_02_20/2017_12_10/ungrib_lake/')
paths = mp,mps,mt = 'met_pre','met_pre_sur','met_tav'
pdic={}
for m in paths:
    pdic[m]={}
    pdic[m]['n']=m
    pdic[m]['p']=os.path.join(path,m)
df = pd.DataFrame(pdic).T
df

# %%
for m in paths:
    fs = os.listdir(pdic[m]['p'])
    dff = pd.DataFrame(fs,columns=['file'])
    dff = dff[dff.file.str.startswith('met_em.d0')]
    dff =dff.sort_values('file')
    pdic[m]['f']=dff

# %%
m = mp
for m in paths:
    fp = os.path.join(pdic[m]['p'],pdic[m]['f'].iloc[0].file)
    xa=xr.open_dataset(fp)
    pdic[m]['vars']=list(xa.variables)

# %%
s1 = pdic[mt]['vars']
s2 = pdic[mps]['vars']
set(s1).difference(set(s2))

# %%
path = os.path.join(gc.PATH_DATA,'runs/run_2019_02_20/2017_12_10/ungrib_lake/')
print(path)

fs = os.listdir(path)
df = pd.DataFrame(fs,columns=['file'])
df = df[df.file.str.startswith('met_em.d01')]
df

file =df.iloc[0].file
file = os.path.join(path,file)
print(file)


vm,vM = 260,280
xa = xr.open_dataset(file)
xa.SKINTEMP.plot(levels=10, vmin=vm,vmax=vM)


# %%
xa.NUM_METGRID_SOIL_LEVELS

# %%
with xa['TAVGSFC'] as a :
    a.plot()
    print(a)


# %%
pls='LANDSEA','LANDMASK','LU_INDEX','TAVGSFC'
ops={},{},{'levels':21,'cmap':'tab20'},{}
for i in range(len(pls)):
    fig,ax = plt.subplots()
    xa[pls[i]].plot(**ops[i])
for i in range(len(pls)):
    fig,ax = plt.subplots()
    xa[pls[i]].plot.hist()

# %%
x1 = xa['TT'].mean('num_metgrid_levels')[0]
x1
x1.plot()

# %%
path1 = os.path.join('/Users/diego/wrf_management/wrf_management/tucu-april-rm-data')
print(path1)

fs = os.listdir(path1)
df = pd.DataFrame(fs,columns=['file'])
df = df[df.file.str.startswith('met_em.d03')]
df

file =df.iloc[1].file
file = os.path.join(path1,file)
print(file)

os.path.isfile(file)

xa = xr.open_dataset(file)
xa.SKINTEMP.plot(levels=10,  vmin=vm,vmax=vM)

# %%


# %%
xa

# %%
st='cdas1.t18z.splgrbf06.grib2'

# %%
't18' in st


# %%

