# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.0.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *

# %%
matplotlib.rcParams['figure.figsize'] = (9.0, 6.0)

# %%
path = '/Volumes/mbProD/Downloads/wrf_small_files'

# %%
glob.glob(path+'/wrf*')

# %%
file_path = os.path.join(path,'wrflowinp_d01')

# %%
xa = xr.open_dataset(file_path)

# %%
xa1 = xa.isel(Time=0)

# %%
pars = ['SST','ALBBCK','LAI','VOCE','UOCE','VEGFRA','SEAICE']
for p in pars:
    plt.figure()
    xa1[p].plot()
    ax = plt.gca()
    ax.set_title(xa1[p].description)

# %%
pars = ['SST']
names = ['_q95','_q05','_q50','_mean']

for p in pars:
    np = [p+n for n in names]
    xa[p+'_q95'] = xa[p].quantile(.95,dim=['south_north','west_east'])
    xa[p+'_q05'] = xa[p].quantile(.05,dim=['south_north','west_east'])
    xa[p+'_q50'] = xa[p].quantile(.5,dim=['south_north','west_east'])
    xa[p+'_mean'] = xa[p].mean(dim=['south_north','west_east'])

# %%
np

# %%
for pp in np:
    xa[pp].plot()

# %%
from sklearn.cluster import KMeans

# %%
def scale(x, out_range=(0, 1)):
    domain = np.quantile(x,.05), np.quantile(x,.95)
    y = (x - (domain[1] + domain[0]) / 2) / (domain[1] - domain[0])
    return y * (out_range[1] - out_range[0]) + (out_range[1] + out_range[0]) / 2

# %%
file_lowinp = '/Volumes/mbProD/Downloads/wrf_small_files/wrflowinp_d01'

# %%
file_input = '/Volumes/mbProD/Downloads/wrf_small_files/wrfinput_d01' 

# %%
xa_low = import_lowinp(file_lowinp,file_input)

# %%
p = 'SST'
p_c = p+'_clus'
nc = 8 
xa_low[p_c]=get_cluster(xa_low,p,nc)

# %%
plot_clus(xa_low,'SST_clus',nc)

# %%
x2 = xa_low[[p,p_c]].rolling(Time=4,center=True,min_periods=4).mean()
line_plot_clus(x2,nc,p,p_c)
ax = plt.gca()
ax.set_xlim(736655.95, 736855.05)
ax.set_ylim(270,310)

# %%
x1 = xa_low.where(xa_low.LAKEMASK==1)
p = 'SST'
nc = 6
p_c = p+'_clus_lake'

# %%
 
xa_low[p_c]=get_cluster(x1,p,nc)

# %%
plot_clus(xa_low,p_c,nc)

# %%
line_plot_clus(xa_low,nc,p,p_c)
ax = plt.gca()
ax.set_ylim(270,310)

# %%
p = 'ALBBCK'
p_c = p+'_clus'
nc = 7 
xa_low[p_c]=get_cluster(xa_low,p,nc)

# %%
plot_clus(xa_low,p_c,nc)

# %%
x2 = xa_low[[p,p_c]].rolling(Time=4,center=True,min_periods=4).mean()
line_plot_clus(x2,nc,p,p_c)
ax = plt.gca()
ax.set_xlim(736655.95, 736855.05)
# ax.set_ylim(270,310)
