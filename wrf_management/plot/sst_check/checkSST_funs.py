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
def get_file_list(path):
#     wrf_path = pjoin(path,'wrf') 
    wrf_path=path
    fls = glob.glob(pjoin(wrf_path,'wrf*'))
    dffile = pd.DataFrame(fls,columns=['path'])
    b1 = ~dffile.path.str.contains('wrfrst')
    b2 = ~dffile.path.str.contains('wrf.exe')
    dffile = dffile[b1 & b2]
    dffile['bname']=dffile.path.apply(lambda p: os.path.basename(p))
    dffile = dffile[['bname','path']]
    dffile = dffile.sort_values('bname')
    dffile['dom'] = dffile.bname.str.extract('(d0\d)')
    dffile['kind'] = dffile.bname.str.extract('(^.*?)_')
    dffile = dffile.set_index('bname')
    return dffile



# %%
def get_specific_files(col_kind_list,dfT):
    b1 = ~dfT.isna().all(axis=1)
    for c,k in col_kind_list:
        b1 = (dfT[c]==k) & b1
    df1 = dfT[b1]
    df1 = df1.sort_values('bname')
    return df1
    
    

# %%
def get_d0(pathTest,kind='wrfinput',dom='d01'):
    dfT = get_file_list(pathTest)
    pT = get_specific_files([['kind',kind],['dom',dom]],dfT).path.iloc[0]
    dsT = xr.open_dataset(pT)
    return dsT
def get_d01(*args,**kargs):
    return get_d0(*args,**kargs)
    
    
    

# %%
ttcc = -69.97139000879771,-15.39788779837302,-69.88877898555209,-15.53607583843065,-69.98353301593667,-15.64061002790482,-70.0520469626809,-15.74814077570002,-70.01039486576632,-15.88482809810006,-69.82643436497722,-15.9587658518762,-69.67270243413878,-15.99151893895542,-69.5583061176992,-15.98787823597414,-69.45931614193165,-16.02405088269405,-69.5472809147729,-16.17322273550132,-69.46350370443112,-16.22123077155368,-69.38417746881494,-16.26511191902281,-69.2541402052409,-16.33161317248631,-69.16803120021579,-16.29279981786604,-69.09305748582055,-16.26344346309993,-69.06170931236727,-16.39563568594153,-69.13969638567227,-16.49887323021604,-69.13991492517496,-16.50469266757229,-68.9937025720463,-16.62874885223271,-68.83546804030154,-16.63472436615536,-68.79360194242751,-16.54353842679494,-68.75924413378448,-16.47697068792091,-68.62267367403142,-16.40552037934324,-68.55123747999355,-16.32749601802275,-68.54979646572588,-16.20177498988945,-68.63862124521188,-16.17040713287612,-68.82260624635538,-16.14883326349966,-68.81892090945934,-16.08291207897927,-68.73310071588764,-16.05567112026258,-68.67843435144056,-15.98041270659036,-68.70306277861214,-15.9082668895298,-68.93233178043184,-15.8472344790016,-69.02505440849212,-15.76167308436384,-69.1409338522068,-15.65405732321192,-69.22672499501377,-15.64310830970895,-69.26958069531815,-15.55492071682268,-69.34422177571264,-15.48175592641214,-69.49077621966197,-15.38778943855211,-69.5988280808557,-15.33365582027952,-69.65234330423733,-15.24217600913368,-69.72199893243206,-15.22191314259212,-69.77586174266176,-15.28007454368652,-69.8287278827017,-15.27354000812603,-69.87994187327028,-15.29266763720533,-69.97139000879771,-15.39788779837302,
ttcc = np.array(ttcc)
ttcc = np.vstack(np.split(ttcc,len(ttcc)/2))


# %%
def plot_lake_example():
    pc = mpl.collections.PatchCollection([plt.Polygon(ttcc)])
    fig, ax = plt.subplots()
    # pc.set_array(np.array([2342]))
    ax.add_collection(pc)
    ax.set_xlim(-72,-67)
    ax.set_ylim(-17,-14)


# %%
def add_isttcc(dsO):
    ds = dsO
    ds['lat']=ds.XLAT
    ds['lon']=ds.XLONG

    ds1 =  ds[['lat','lon']].copy()

    ttccP = mpl.path.Path(ttcc)
    def fun(la,lo):
        global xx
        xx=(la,lo)
        res = ttccP.contains_points([[lo,la]])
        return res
    ds['is_ttcc']=xr.apply_ufunc(fun,ds1['lat'],ds1['lon'],vectorize=True)
    ds['is_ttcc']= ds['is_ttcc'] & (ds.LAKEMASK==1)
    
    return ds
    


# %%
def get_sst_ttcc(f1,sst='SST'):
    ds = xr.open_dataset(f1.path)
    ds = add_isttcc(ds)
    ds = ds[[sst]].where(ds.is_ttcc,drop=True)
    ds = ds.swap_dims({'Time':'XTIME'})
#     ds = ds.swap_dims({'south_north':'XLAT'})
#     ds = ds.swap_dims({'west_east':'XLONG'})
    return ds


# %%
test_time = dt.datetime.now()

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
