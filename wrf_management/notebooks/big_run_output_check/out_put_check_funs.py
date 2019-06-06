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
from useful_scit.imps import *
import wrf 
from netCDF4 import Dataset
from sklearn.cluster import KMeans


# %%
def import_ds(path,var):
    files = glob.glob(path)
    files.sort()
    ncs = [Dataset(f) for f in files]
    tc = wrf.getvar(ncs,'tc',timeidx=wrf.ALL_TIMES, method="cat")
    z = wrf.getvar(ncs,'z',timeidx=wrf.ALL_TIMES, method="cat")
    tc['height']=z
    ds = tc.to_dataset()
    return ds
    


# %%
def cluster_ds_raw(ds, clus_num, var, var_name):
    tc1 = ds[var_name].to_series()
    tc1 = tc1.unstack(level='Time').dropna(axis=0,how='all')
    kmeans = KMeans(n_clusters=clus_num, random_state=0).fit(tc1)
    tc1['lab']=kmeans.labels_
    lab_da = tc1['lab'].to_xarray()
    labs = tc1['lab'].unique()
    labs.sort()
    labs
    ds['clus_lab'] = lab_da
    return {'ds':ds, 'labs':labs} 


# %%
def find_bot_top(ds,i):
    dsi = ds[var_name].where(ds['clus_lab']==i)
    dsi
    b_t = ds.bottom_top
    dic = dsi.count(dim=['Time','south_north','west_east'])
    bot_top_val = (b_t*dic).sum()/dic.sum()
    bot_top_val
    return i , bot_top_val


# %%
def get_sorted_labs(ds,labs):
    lab_dic = {}
    for i in labs:
        nn,tb = find_bot_top(ds,i)
        lab_dic[i]= float(tb)
    df = pd.DataFrame(lab_dic,['bt']).T
    df['old_lab']=df.index
    df=df.sort_values('bt').reset_index(drop=True)
    df['new_lab']=df.index
    return df


# %%
def ds_fix_cluster_lab(ds_i,df):
    ds = ds_i.copy()
    ds['old_lab'] = ds.clus_lab.copy()
    ds['new_lab'] = ds.clus_lab.copy()
    for l,r in df.iterrows():
        ds['i'] = r.new_lab
        ds['new_lab']= ds['i'].where(ds.old_lab==r.old_lab,ds['new_lab'])
    ds = ds.drop(['old_lab','i'])
    ds['new_lab']=ds.new_lab.astype(int)
    return ds


# %%
def cluster_ds(path, clus_num, var, var_name):
    ds = import_ds(path,var)
    res = cluster_ds_raw(ds,clus_num,var, var_name)
    ds = res['ds']
    labs = res['labs'] 
    df = get_sorted_labs(ds,labs)
    ds1 = ds_fix_cluster_lab(ds,df)
    return ds1 

    
    

# %%
cmap=matplotlib.colors.ListedColormap(sns.color_palette('Greys',18))
dsi = ds2[var_name].where(ds2.clus_lab==i)
plt.subplots()
dsc = dsi.count(dim=['Time','bottom_top'])
dsc.name = 'counts'
dsc.plot.imshow(vmin=0,vmax=tot_max,
                cmap=cmap)

# %%
tot = ds2[var_name].count()
tot_max = ds2[var_name].count(dim=['Time','bottom_top']).max()
grid_max = dsc.max()

# %%
tot_max

# %%
sns.choose_colorbrewer_palette('d')

# %%
cmBuRd = mpl.colors.ListedColormap(sns.color_palette('RdBu_r',18))

# %%
