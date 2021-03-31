---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
path = '/tmp/wrf_management/data_folder/runs/run_2019_02_20/2017_12_02/metgrid/'
```

```python
import os
fls = os.listdir(path)
df = pd.DataFrame(fls,columns=['names'])
df = df[df.names.str.startswith('met_em.d')]
df['dom']=df.names.str.extract(r'd0(.)\.').astype(int)
df = df.sort_values('dom')
df['path']=df.names.apply(
    lambda n: os.path.join(path,n)
)
df = df.sort_values('names')
```

```python
p = df[df.dom==3].iloc[-1].path
```

```python
cols = [
    'SKINTEMP','TAVGSFC','SOILTEMP',
    'ST','LU_INDEX','LANDSEA','SEAICE','LANDMASK'
]
skim = ['ST']
ar = xr.open_dataset(p)
lcols = len(cols)
fx, fy = 3, 10
ic = 4
fig = plt.figure(1,figsize=(ic*fx * (1.3),ic*fy))
for i in range(lcols):
    col = cols[i]
    ax = fig.add_subplot(fy,fx,i+1)
    to_pl=ar[col]
    if col in skim:
        to_pl=to_pl[0][0]
    to_pl.plot(ax=ax)
fig.set_tight_layout('pad')
import warnings
warnings.filterwarnings('ignore')
```

```python
list(ar.variables)
```

```python
ar
```

```python

```


```python
path = '/tmp/wrf_management/data_folder/runs/run_2019_02_20/2017_12_02/real/'
```

```python
import os
fls = os.listdir(path)
df = pd.DataFrame(fls,columns=['names'])
df = df[df.names.str.startswith('wrfinput_')]
df['dom']=df.names.str.extract(r'd0(.)').astype(int)
df = df.sort_values('dom')
df['path']=df.names.apply(
    lambda n: os.path.join(path,n)
)
df
```

```python
p = df[df.dom==4].iloc[0].path

cols = [
    'T','SST','T2','TSLB'
]
skim = ['T','TSLB']
ar = xr.open_dataset(p)
lcols = len(cols)
fx, fy = 3, 10
ic = 4
fig = plt.figure(1,figsize=(ic*fx * (1.3),ic*fy))
for i in range(lcols):
    col = cols[i]
    ax = fig.add_subplot(fy,fx,i+1)
    to_pl=ar[col]
    if col in skim:
        to_pl=to_pl[0][0]
    to_pl.plot(ax=ax)
    ax.set_title(ar[col].description)
fig.set_tight_layout('pad')
import warnings
warnings.filterwarnings('ignore')
```

```python
p = df[df.dom==3].iloc[0].path

cols = [
    'T','SST','T2','TSLB','LU_INDEX'
]
skim = ['T','TSLB']
ar = xr.open_dataset(p)
lcols = len(cols)
fx, fy = 3, 10
ic = 4
fig = plt.figure(1,figsize=(ic*fx * (1.3),ic*fy))
for i in range(lcols):
    col = cols[i]
    ax = fig.add_subplot(fy,fx,i+1)
    to_pl=ar[col]
    if col in skim:
        to_pl=to_pl[0][0]
    to_pl.plot(ax=ax)
    ax.set_title(ar[col].description)
fig.set_tight_layout('pad')
import warnings
warnings.filterwarnings('ignore')
```

```python
list(ar.variables)
```

```python
ar['TSLB'].description
```

```python
ar.Times
```

```python

```

