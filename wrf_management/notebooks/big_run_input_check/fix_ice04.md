```python

```


```python
%load_ext autoreload
```


```python
%autoreload 2
```


```python
from useful_scit.imps import *
import check_input_01_funs as pp
from check_input_01_funs import *
```


```python
path = '/wrk/kadantse/wrfimp_longrun'
out_path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'
fn_low = 'wrflowinp_d04'
fn_inp = 'wrfinput_d04'
file_out = os.path.join(out_path,fn_low)
```


```python
glob.glob(path+'/wrf*')
```




    ['/wrk/kadantse/wrfimp_longrun/wrflowinp_d01',
     '/wrk/kadantse/wrfimp_longrun/wrflowinp_d04',
     '/wrk/kadantse/wrfimp_longrun/wrfinput_d03',
     '/wrk/kadantse/wrfimp_longrun/wrfinput_d01',
     '/wrk/kadantse/wrfimp_longrun/wrfinput_d04',
     '/wrk/kadantse/wrfimp_longrun/wrflowinp_d03',
     '/wrk/kadantse/wrfimp_longrun/wrfinput_d02',
     '/wrk/kadantse/wrfimp_longrun/wrflowinp_d02']




```python
xr.set_options(keep_attrs=True)
file_path = os.path.join(path,fn_low)
file_input = os.path.join(path,fn_inp)
xa_help =  import_lowinp(file_path,file_input)
xa_raw = xr.open_dataset(file_path)
xa_cop = xa_raw.copy()
```


```python
dims = ['south_north','west_east']
sst = 'SST'
si = 'SEAICE'
```


```python
xa_cop[sst] = xa_cop[sst].where(xa_cop[si]==0) 
xa_cop[sst] = xa_cop[sst].interpolate_na(dim='Time',method='linear')
xa_cop[sst].attrs = xa_raw[sst].attrs
xa_cop[si]=xa_cop[si].where(xa_cop[si]==0,0.0)
xa_cop[si].attrs = xa_raw[si].attrs
```


```python
b_l = xa_help['LAKEMASK']==1
b_l = b_l.drop('XLONG').drop('XLAT')
b_t = xa_cop[sst]>307
```


```python
xa_cop[sst]=xa_cop[sst].where(~(b_t & b_l))
xa_cop[sst] = xa_cop[sst].interpolate_na(dim='Time',method='linear')
xa_cop[sst].attrs = xa_raw[sst].attrs
```


```python
try: os.remove(file_out)
except: pass
xa_cop.to_netcdf(file_out)
```


```python
xa_low_new = import_lowinp(file_out,file_input)
```


```python
x1 = xa_low_new.where(xa_low_new.LAKEMASK==1)
p = 'SST'
nc = 6
p_c = p+'_clus_lake'
cols = 2
plot_clus_sig(x1,p,p_c,nc,cols=2)
```


![png](fix_ice04_files/fix_ice04_13_0.png)



```python
x1 = xa_low_new
p = 'SST'
nc = 7
p_c = p+'_clus_lake'
cols = 2
plot_clus_sig(x1,p,p_c,nc,cols=2)
```


![png](fix_ice04_files/fix_ice04_14_0.png)



```python

```
