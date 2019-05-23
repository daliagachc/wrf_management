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



# %%
from useful_scit.imps import *
import check_input_01_funs
importlib.reload(check_input_01_funs)
from check_input_01_funs import *
matplotlib.rcParams['figure.figsize'] = (9.0, 6.0)

# %%
path = '/Volumes/mbProD/Downloads/met'

# %%
files = glob.glob(path+'/met*')
files.sort()

# %%
f = files[1]

# %%
ta = xr.open_dataset(f)

# %%
# var = list(ta.variables)
# for v in var:
#     try: 
#         print(v,ta[v].description)
#     except: pass

# %%
xas = [xr.open_dataset(f)[['TT','LU_INDEX','XLAT_M','XLONG_M','Times','SKINTEMP']] for f in files[1:]]
xas1 = []
for xa in xas:
    t1=xa.Times.to_dataframe().Times.str.decode('utf-8')
    t1=pd.to_datetime(t1.values,format='%Y-%m-%d_%H:%M:%S')
    xa=xa.assign_coords(Time=t1)
    xas1.append(xa)

# %%
xa = xr.concat(xas,dim='Time')
xa = xa.assign_coords(XLAT=xa.XLAT_M.isel(Time=0))
xa = xa.assign_coords(XLONG=xa.XLONG_M.isel(Time=0))

# %%
t1=xa.Times.to_dataframe().Times.str.decode('utf-8')
t1=pd.to_datetime(t1.values,format='%Y-%m-%d_%H:%M:%S')
xa=xa.assign_coords(Time=t1)

# %%
xa.TT.isel(num_metgrid_levels=0,Time=12).plot()

# %%



# %%
xa.Time


# %%
# xa['T0']=xa.TT.isel(num_metgrid_levels=0)
p = 'SKINTEMP'
p_c = 'SKINTEMP_clus'
nc = 7
cols = 2
plot_clus_sig(xa,p,p_c,nc,cols=2)

# %%
xa['T0']=xa.TT.isel(num_metgrid_levels=0)
p = 'T0'
p_c = p+'_clus'
nc = 7
cols = 2
plot_clus_sig(xa,p,p_c,nc,cols=2)

# %%
x1 = xa[['SKINTEMP']].where(xa.LU_INDEX[0]==21).isel(Time=slice(1,None))

# %%
p = 'SKINTEMP'
p_c = p+'lake_clus'
nc = 7
cols = 2
plot_clus_sig(x1,p,p_c,nc,cols=2)

# %%



# %%


