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
path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/wrf_management_data/runs/run_2019_02_28_2'

# %%
wrf_path = pjoin(path,'wrf') 

# %%
fls = glob.glob(pjoin(wrf_path,'wrf*'))
dffile = pd.DataFrame(fls,columns=['path'])
b1 = ~dffile.path.str.contains('wrfout')
b2 = ~dffile.path.str.contains('wrf.exe')
dffile = dffile[b1 & b2]
dffile['bname']=dffile.path.apply(lambda p: os.path.basename(p))
dffile = dffile[['bname','path']]
dffile = dffile.sort_values('bname')

b = dffile.bname =='wrffdda_d01'
nudge01 = dffile[b].iloc[0].path



# %%
dsn01 = xr.open_dataset(nudge01)
ti, bt, = 40, 5,
dsn01.U_NDG_OLD[ti,bt].plot()
plt.subplots()
dsn01.U_NDG_NEW[ti,bt].plot()



# %%
dsn01 = xr.open_dataset(nudge01)
ti, bt, = 41, 5,
dsn01.U_NDG_OLD[ti,bt].plot()
plt.subplots()
dsn01.U_NDG_NEW[ti,bt].plot()



# %%
(
    dsn01.U_NDG_NEW[40,5] - \
    dsn01.U_NDG_OLD[41,5]
).plot()

# %%
dsn01.U_NDG_NEW

# %%
dsn01 = xr.open_dataset(nudge01)
ti, bt, = 82, 5,
dsn01.U_NDG_OLD[ti,bt].plot()
plt.subplots()
dsn01.U_NDG_NEW[ti,bt].plot()



# %%
dsn01.MU_NDG_NEW



# %%
dffile = dffile.set_index('bname')

# %%
in01 = dffile.loc['wrfinput_d01'].path

# %%
din01 = xr.open_dataset(in01)
din01.dims

# %%
bd01 = dffile.loc['wrfbdy_d01'].path
dbd01 = xr.open_dataset(bd01)
dbd01

# %%
i1=dffile.loc['wrfinput_d01'].path
di1 = xr.open_dataset(i1)
lus = ['LANDUSEF','LAKE_DEPTH','LU_INDEX']
for l in lus:
    print(di1[l])
    print('------')

# %%
di1.LAKE_DEPTH[0].plot()

# %%
di1.LANDUSEF.where(di1.LANDUSEF>0).plot()

# %%
di1.LANDUSEF[0,15:17,30:50,35:65].plot(col='land_cat_stag',col_wrap=2)

# %%
i1=dffile.loc['wrfinput_d03'].path
di1 = xr.open_dataset(i1)
di1.LANDUSEF[0,16].plot(figsize=(10,8))
ax = plt.gca()
ax.set_title('water=17')

# %%
l1 = dffile.loc['wrflowinp_d01'].path
dl1 = xr.open_dataset(l1)

# %%
dl1.SST[0:84:10].plot(col='Time',col_wrap=5)

# %%
_df = dl1[['Times','SST']].to_dataframe()

# %%
_df = _df.reset_index(drop=True)
_df.Times = pd.to_datetime(_df.Times.str.decode('utf-8'),format='%Y-%m-%d_%H:%M:%S')

# %%
sns.relplot(x='Times',y='SST',data=_df,kind='line',ci='sd')
fig = plt.gcf()
fig.autofmt_xdate()

# %%
vas = list(dl1.variables)
for v in vas:
    try:
        p = dl1[v].description
        print(v,p)
    except: 
        pass

# %%
dl1[v].description

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
