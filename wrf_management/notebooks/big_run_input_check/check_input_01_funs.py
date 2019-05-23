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
def plot_clus(xa_low, p_clus , nc,x='XLONG',y='XLAT',pargs=dict()):
    xa_low[p_clus].plot(
        x=x,y=y,
        levels=nc+1, 
        colors=sns.color_palette('Dark2',nc),
        vmin=-.5,vmax=nc-.5,
        **pargs
    )





# %%


# %%


# %%


def multiplot(va, f1, f2, arg1, arg2, col, ax, dim):
    va1 =getattr(va,f1)(dim=dim, **arg1).to_series()
    va2 =getattr(va,f2)(dim=dim, **arg2).to_series()
    ax.fill_between(va1.index,va1,va2, color = col, alpha=.3)
    return ax

# %%

def plot_histograms(xa,p, ax):
    desc = xa[p].description
    ser = xa[p].to_series()
    sns.distplot(ser,ax=ax)
    ax.set_title(desc)

def plot_lowinp_pars(xa):
    pars = ['SST','ALBBCK','LAI','VEGFRA','SEAICE']
    fig, axs = plt.subplots(3,2)
    # plt.close(fig)
    axsf = axs.flatten()
    for p,ax in zip(pars,axsf):
    #     fig, ax = plt.subplots()
        plot_histograms(xa,p, ax)
    fig.tight_layout()

def plot_clus_with_uncer(xa_low, p, p_c, i, nc, ax=False):
    if ax is False:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    # i = 0
    pal = sns.color_palette('Dark2',nc)
    va  = xa_low[p].where(xa_low[p_c]==i)
    dim = ['south_north', 'west_east']
    col = pal[i]


    min_max = dict(
        col = col,
        f1 = 'min',
        f2 = 'max',
        arg1 = {},
        arg2 = {},
        va = va,
        ax =ax,
        dim=dim
    )

    per = dict(
        col = col,
        f1 = 'quantile',
        f2 = 'quantile',
        arg1 = {'q':.05},
        arg2 = {'q':.95},
        va = va,
        ax =ax,
        dim=dim
    )


    dics = [min_max,per]


    for d in dics: multiplot(**d)

    va1 = va.median(dim).to_series()
    ax.plot_date(va1.index,va1.values,
                 color = col, marker=None, linestyle='-.',linewidth=3)

    va1 = va.mean(dim).to_series()
    ax.plot_date(va1.index,va1.values,
                 color = col, marker=None, linestyle='-',linewidth=3)

    fig





def plot_clus_sig(xa_low,p,p_c,nc,cols=2):
    xa_low[p_c] = get_cluster(xa_low, p, nc)
    rows = int(np.ceil((nc + 1) / cols))
    fig = plt.figure(figsize=(cols * 3.5, rows * 3))
    ax = fig.add_subplot(rows, cols, 1)
    # ax.set_title(p_c)
    plot_clus(xa_low, p_c, nc, pargs=dict(ax=ax))
    for i in range(nc):
        if i > 0:
            ss = ax
        else:
            ss = None
        ax = fig.add_subplot(rows, cols, i + 2, sharey=ss, sharex=ss)
        plot_clus_with_uncer(xa_low, p, p_c, i, nc, ax=ax)
        ax.grid(True, axis='y')
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
    fig.tight_layout()

