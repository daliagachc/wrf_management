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
from out_grid_funs import *
from matplotlib.patches import Polygon

# %%
path = '/Users/diego/Downloads/wrf_out_sample/'

# %%
files = os.path.join(path,'wrf*')
files = glob.glob(files)
files

# %%
files_dic = get_files(path)

# %%
files_dic['ll']=files_dic.apply(lambda r: get_ll(r.path), axis=1 )

# %%

# %%
ax,proj = get_map(-100,-35,-50,10,pargs={'figsize':(10,10)})
for l,r in files_dic.iterrows():
    ll = r.ll
    plot_pol(r.ll,ax)
    add_text_ll(ll,ax)
ax.set_xlim(-100,-35)
ax.set_ylim(-50,10);

# %%
ax,proj = get_map(-100,-35,-50,10,pargs={'figsize':(10,10)})
for l,r in files_dic[-2:].iterrows():
    ll = r.ll
    plot_pol(r.ll,ax)
    add_text_ll(ll,ax)
ax.set_xlim(-72,-60)
ax.set_ylim(-22,-12);

# %%
for r,v in files_dic.iterrows():
    print(pd.DataFrame(v['ll'],[r]).T.round(7))

# %%
file = files[0]

# %%
xa = xr.open_dataset(file)

# %%
df = xa.XLONG_U[0,0].to_pandas()


# %%
def fun(x):
    global xx
    xx=x
    return x[-1] - x[0]
res = df.rolling(2).apply(lambda x: fun(x), raw=True)

# %%
res.value_counts()

# %%
xx[0]

# %%
