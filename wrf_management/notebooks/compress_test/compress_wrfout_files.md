```python
%load_ext autoreload
%autoreload 2
```


```python
from useful_scit.imps import * 
import useful_scit.util.zarray as za
```


```python
import wrf_management.modules.CompressOut as CO
import sqlite3

```


```python
# path  = '/Volumes/mbProD/Downloads/wrf_test_d01/'
pc = 'taito'
# pc = 'mac'

if pc is 'taito':
    path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'
    path_out  = '/proj/atm/saltena/runs/run_2019_05_15/wrf_compressed'
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = '2017-12-0*'
    wrfout_patt = 'wrfout'
    
if pc is 'taito':
    path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-18_17-40-56_/2017-12-08'
    path_out  = os.path.join(path,'.compressed_log')
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = '*.nc'
    wrfout_patt = ''
    date_pattern = ''
    
if pc is 'taito':
    path = '/proj/atm/saltena/runs/run_2019_03_01/wrf'
    path_out  = os.path.join(path,'wrf_compressed')
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = ''
    wrfout_patt = 'wrfout'
    
if pc is 'mac':
    path = '/Volumes/mbProD/Downloads/wrf_test_d01/'
    path_out  = '/private/tmp/co_out/'
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = 'd01*'
    wrfout_patt = 'wrfout'
self = CO.Compresser(path,path_out,db_path,pattern=patt,wrfout_patt=wrfout_patt,lock_last_date=False)
```

    2019-06-19 02:13:29,162 - DEBUG - creating db table
    2019-06-19 02:13:29,169 - DEBUG - file table already exist in db



```python
# self.drop_files_table()
```


```python
self.reset_locks()
while True:
    self.get_and_zip_next_row(move=True)
```

    2019-06-18 19:49:37,376 - DEBUG - compressing:wrfout_d01_2017-12-25_00:00:00
    2019-06-18 19:49:47,053 - DEBUG - compressing:wrfout_d01_2017-12-25_01:00:00
    2019-06-18 19:49:57,185 - DEBUG - compressing:wrfout_d01_2017-12-25_02:00:00
    2019-06-18 19:50:07,698 - DEBUG - compressing:wrfout_d01_2017-12-25_03:00:00
    2019-06-18 19:50:17,415 - DEBUG - compressing:wrfout_d01_2017-12-25_04:00:00
    2019-06-18 19:50:27,097 - DEBUG - compressing:wrfout_d01_2017-12-25_05:00:00
    2019-06-18 19:50:36,855 - DEBUG - compressing:wrfout_d01_2017-12-25_06:00:00
    2019-06-18 19:50:46,616 - DEBUG - compressing:wrfout_d01_2017-12-25_08:00:00
    2019-06-18 19:51:05,661 - DEBUG - compressing:wrfout_d01_2017-12-25_10:00:00
    2019-06-18 19:51:24,094 - DEBUG - compressing:wrfout_d01_2017-12-25_12:00:00
    2019-06-18 19:51:42,638 - DEBUG - compressing:wrfout_d01_2017-12-25_14:00:00
    2019-06-18 19:52:01,195 - DEBUG - compressing:wrfout_d01_2017-12-25_16:00:00
    2019-06-18 19:52:19,956 - DEBUG - compressing:wrfout_d01_2017-12-25_18:00:00
    2019-06-18 19:52:38,514 - CRITICAL - we are done! no more files to compress



    An exception has occurred, use %tb to see the full traceback.


    SystemExit: 0



    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/IPython/core/interactiveshell.py:3304: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)



```python

```
