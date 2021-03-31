```python
from useful_scit.imps import *
from matplotlib.patches import Polygon
```


```python
def get_ll(file):
    xd = xr.open_dataset(file)
    loM = float(xd.XLONG_U.max())
    lom = float(xd.XLONG_U.min())
    laM = float(xd.XLAT_V.max())
    lam = float(xd.XLAT_V.min())

    ll_dic = dict(
    loM = loM,
    lom = lom,
    laM = laM,
    lam = lam,
    )
    return ll_dic
```


```python
def plot_pol(ll,ax):
    pol_points = [
        [ll['lom'],ll['lam']],
        [ll['lom'],ll['laM']],
        [ll['loM'],ll['laM']],
        [ll['loM'],ll['lam']],
    ]
#     print(ll)
    polygon = Polygon(pol_points, True, edgecolor='k',facecolor='none')
    ax.add_patch(polygon)
```


```python
def get_files(path):
    path = '/Users/diego/Downloads/wrf_out_sample/'
    file_pat = dict(
        d1='d01_2017',
        d2='d02_2017',
        d3='d03_2017',
        d4='d04_2017',
    )
    files_dic={}
    for d,p in file_pat.items():
        files_dic[d]=glob.glob(os.path.join(path,'*'+p+'*'))
    files_dic = pd.DataFrame(files_dic,['path']).T
    return files_dic
    
    
```


```python
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


def get_map(lom,loM,lam,laM,pargs={}):
    fig = plt.figure(**pargs)
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([lom,loM,lam,laM], crs=proj)

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    gl = ax.gridlines(crs=proj, draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
    return ax, proj
```


```python
def add_text(t,x,y,ax):
    ax.text(x, y, t, size=8,
             ha="center", va="center",
             bbox=dict(boxstyle="round",
                       ec='w',
                       fc='w',
                       )
             )
```


```python
def add_text_ll(ll,ax):
    pol_points = [
        [ll['lom'],ll['lam']],
        [ll['lom'],ll['laM']],
        [ll['loM'],ll['laM']],
        [ll['loM'],ll['lam']],
    ]
    
    for p in pol_points:
        pr = [np.round(pp,1) for pp in p]
        add_text(pr,*p,ax)
```


```python

```
