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
f = files[0]

# %%
xas = [xr.open_dataset(f)[['TT','LU_INDEX','XLAT_M','XLONG_M','Times']] for f in files]

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


# %%
xa['T0']=xa.TT.isel(num_metgrid_levels=0)
p = 'T0'
p_c = 'T0_clus'
nc = 8 
xa[p_c]=get_cluster(xa,p,nc)

# %%
plot_clus(xa,p_c,nc,x='XLONG',y='XLAT')

# %%
x2 = xa[[p,p_c]].isel(Time=slice(1,None)).rolling(Time=4,center=True,min_periods=4).mean()

# %%
line_plot_clus(x2,nc,p,p_c)
ax = plt.gca()
ax.set_xlim(736655.95, 736855.05)
ax.set_ylim(270,310)

# %%
x1 = xa[['T0']].where(xa.LU_INDEX[0]==21).isel(Time=slice(1,None))

# %%
p = 'T0'
nc = 6
p_c = p+'_clus_lake'

# %%
 
x1[p_c]=get_cluster(x1,p,nc)

# %%
plot_clus(x1,p_c,nc)

# %%
x2 = x1.rolling(Time=4,center=True,min_periods=1).mean()
line_plot_clus(x2,nc,p,p_c)
ax = plt.gca()
ax.set_xlim(736655.95, 736855.05)


# %%
ax.get_xlim()

# %%
x1

# %%


# %%


# %%

