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
from useful_scit.imps import *

# %%
from sklearn.cluster import KMeans

# %%
pars = ['SST','T2','TSK','SEAICE','LAKEMASK']

# %%
def import_lowinp(file_lowinp,file_input):
    xa_low = xr.open_dataset(file_lowinp)
    xa_inp = xr.open_dataset(file_input)
    xlat = xa_inp.isel(Time=0).XLAT 
    xlkm = xa_inp.isel(Time=0).LAKEMASK 
    xa_low1=xa_low.assign_coords(XLAT=xlat)
    t1=xa_low.Times.to_dataframe().Times.str.decode('utf-8')
    t1=pd.to_datetime(t1.values,format='%Y-%m-%d_%H:%M:%S')
    xa_low1=xa_low1.assign_coords(Time=t1)
    xa_low1['LAKEMASK']=xlkm
    return xa_low1
    
    
    

# %%
p = 'SST'
nc = 8 

# %%
def get_cluster(xa_low,p,nc):
    xp = xa_low[p]
    ps = xp.to_series().unstack(level=0)
    ps1 = ps.dropna(0,'all')


    y_pred = KMeans(n_clusters=nc, random_state=13324).fit_predict(ps1)

    df = pd.DataFrame(ps)
    df1 = pd.DataFrame(ps1)
    df1['flags']=y_pred
    df['flags']=df1['flags']

    return df.flags.to_xarray()

# %%
def plot_clus(xa_low, p_clus , nc,x='XLONG',y='XLAT'):
    xa_low[p_clus].plot(
        x=x,y=y,
        levels=nc+1, colors=sns.color_palette('Set1',nc),vmin=-.5,vmax=nc-.5)

# %%
def line_plot_clus(xa_low,nc,p,p_c):
    pal = sns.color_palette('Set1',nc)
    for i in range(nc):
        va = xa_low[p].where(xa_low[p_c]==i)
        va = va.mean(dim=['south_north','west_east'])
        res = va.plot(color=pal[i])
    ax = res[0].figure.axes[0]
    ax.grid()

# %%

