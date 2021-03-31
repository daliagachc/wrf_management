```python
from useful_scit.imps import *
```


```python
path = '/proj/atm/saltena/runs/run_2019_05_15/wrf/'
```


```python
files = glob.glob(path+'wrf*_*')
```


```python
files
```




    ['/proj/atm/saltena/runs/run_2019_05_15/wrf/wrflowinp_d04',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfbdy_d01',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfinput_d04',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrflowinp_d02',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrflowinp_d01',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfinput_d02',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrflowinp_d03',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrffdda_d01',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfinput_d01',
     '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfinput_d03']




```python
ffdda = '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfbdy_d01'
```


```python
xa = xr.open_dataset(ffdda)
```


```python
xa1=xa.isel(Time=slice(0,None,50))
```


```python
xa1.to_netcdf('/proj/atm/wrfbdy_d0_short')
```


```python

```
