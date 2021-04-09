

from useful_scit.imps import *
from out_grid_funs import *
from matplotlib.patches import Polygon


path = '/Users/diego/Downloads/wrf_out_sample/'


files = os.path.join(path,'wrf*')
files = glob.glob(files)
files


files_dic = get_files(path)


files_dic['ll']=files_dic.apply(lambda r: get_ll(r.path), axis=1 )





ax,proj = get_map(-100,-35,-50,10,pargs={'figsize':(10,10)})
for l,r in files_dic.iterrows():
    ll = r.ll
    plot_pol(r.ll,ax)
    add_text_ll(ll,ax)
ax.set_xlim(-100,-35)
ax.set_ylim(-50,10);


ax,proj = get_map(-100,-35,-50,10,pargs={'figsize':(10,10)})
for l,r in files_dic[-2:].iterrows():
    ll = r.ll
    plot_pol(r.ll,ax)
    add_text_ll(ll,ax)
ax.set_xlim(-72,-60)
ax.set_ylim(-22,-12);


for r,v in files_dic.iterrows():
    print(pd.DataFrame(v['ll'],[r]).T.round(7))


add_hoc_dic = {
'd1':
{
    'loM': -43.211700,
    'lom': -89.388306,
    'laM':  -0.481514,
    'lam': -32.188271,},
'd2':
{
    'loM': -53.867840,
    'lom': -78.732163,
    'laM':  -7.172142,
    'lam': -26.339253,},
'd3':
{
    'loM': -61.958614,
    'lom': -70.937401,
    'laM': -13.861786,
    'lam': -20.549194,},
'd4':
{
    'loM': -67.286682,
    'lom': -68.964035,
    'laM': -15.579453,
    'lam': -17.157211,}
              }


import pandas as pd
ahdf = pd.DataFrame(add_hoc_dic).T


def _c(r,a,b): return (r[a] + r[b]) / 2 
for ll in ['lo','la']:
    ahdf[f'{ll}C']=ahdf.apply(_c,axis=1,args=[f'{ll}M',f'{ll}m'])
ahdf





file = files[0]


xa = xr.open_dataset(file)


df = xa.XLONG_U[0,0].to_pandas()


def fun(x):
    global xx
    xx=x
    return x[-1] - x[0]
res = df.rolling(2).apply(lambda x: fun(x), raw=True)


res.value_counts()


xx[0]



