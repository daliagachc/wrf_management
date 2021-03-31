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
pc = 'mac'

if pc is 'taito':
    path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'
    path_out  = '/proj/atm/saltena/runs/run_2019_05_15/wrf_compressed'
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = '2017-12-0*'
    last_date_lock = True
    
if pc is 'mac':
    path = '/Volumes/mbProD/Downloads/wrf_test_d01/'
    path_out  = '/private/tmp/co_out/'
    db_path = os.path.join(path_out,'zip.sqlite')
    patt = 'd0*'
    last_date_lock = False
self = CO.Compresser(path,
                     path_out,
                     db_path,
                     pattern=patt, 
                     lock_last_date = last_date_lock,
                     source_path_is_file=False
                    )
```

    2019-06-19 16:33:53,657 - DEBUG - number of files is 80
    2019-06-19 16:33:53,667 - DEBUG - number of file remaining after dropping symlinks is 20
    2019-06-19 16:33:56,563 - DEBUG - number of file remaining after dropping not cdf files is 20
    2019-06-19 16:33:59,857 - DEBUG - number of files with compress level lower than target is 0
    2019-06-19 16:33:59,857 - CRITICAL - all files already compressed or no files matched pattern. exiting



    An exception has occurred, use %tb to see the full traceback.


    SystemExit: 1



    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/IPython/core/interactiveshell.py:3304: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)



```python
row = self.compress_out_df.iloc[0]
```


```python
self.get_and_zip_next_row(move=True)
```

    2019-06-19 02:03:32,805 - DEBUG - compressing:wrfout_d01_2017-12-25_04:00:00
    2019-06-19 02:03:47,217 - DEBUG - {'moving /private/tmp/co_out/wrfout_d01_2017-12-25_04:00:00 to /Volumes/mbProD/Downloads/wrf_test_d01/wrfout_d01_2017-12-25_04:00:00'}
    2019-06-19 02:03:49,483 - DEBUG - double check fine. deleting /private/tmp/co_out/wrfout_d01_2017-12-25_04:00:00_source_back_up



```python
self.merge_update_dfs()
```


```python

query = f'''
    select {CO.DATE_COL} from {self.files_table_name}
    order by {CO.DATE_COL} desc limit 1
    '''
with sqlite3.connect(self.db_path) as con:
    last_date = pd.read_sql_query(query,con).iloc[0][CO.DATE_COL]
    
```


```python
last_date
```




    1514228400000000000




```python
query = f'''
    delete from {self.files_table_name} where {CO.DATE_COL}=={last_date}
    '''
with sqlite3.connect(self.db_path) as con:
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()

```


```python

```


```python
while True:
    self.get_and_zip_next_row()
```

    2019-06-18 19:50:45,963 - DEBUG - compressing:wrfout_d01_2017-12-25_07:00:00
    2019-06-18 19:51:05,022 - DEBUG - compressing:wrfout_d01_2017-12-25_09:00:00
    2019-06-18 19:51:23,442 - DEBUG - compressing:wrfout_d01_2017-12-25_11:00:00
    2019-06-18 19:51:41,827 - DEBUG - compressing:wrfout_d01_2017-12-25_13:00:00
    2019-06-18 19:52:00,474 - DEBUG - compressing:wrfout_d01_2017-12-25_15:00:00
    2019-06-18 19:52:19,262 - DEBUG - compressing:wrfout_d01_2017-12-25_17:00:00
    2019-06-18 19:52:37,954 - DEBUG - compressing:wrfout_d01_2017-12-25_19:00:00
    2019-06-18 19:52:47,720 - CRITICAL - we are done! no more files to compress



    An exception has occurred, use %tb to see the full traceback.


    SystemExit: 0



    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/IPython/core/interactiveshell.py:3304: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)



```python
sadf
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-9-baca1840028f> in <module>
    ----> 1 sadf
    

    NameError: name 'sadf' is not defined



```python
CO.run_srun('hola',time_minutes=20,memory=4000,parallel_type='serial',n_cpus=1)
```

    2019-06-19 12:13:02,301 - DEBUG - ['srun', '-t', '20', '-p', 'serial', '-c', '1', '--mem', '4000', 'hola']



    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    <ipython-input-15-0fcbe130d1fd> in <module>
    ----> 1 CO.run_srun('hola',time_minutes=20,memory=4000,parallel_type='serial',n_cpus=1)
    

    ~/wrf_management/wrf_management/modules/CompressOut.py in run_srun(exe, time_minutes, memory, parallel_type, n_cpus, message)
        343            ]
        344     logging.debug(cmd)
    --> 345     subprocess.Popen(cmd)
        346     return cmd


    ~/miniconda3/envs/b36/lib/python3.6/subprocess.py in __init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, encoding, errors)
        727                                 c2pread, c2pwrite,
        728                                 errread, errwrite,
    --> 729                                 restore_signals, start_new_session)
        730         except:
        731             # Cleanup if the child failed starting.


    ~/miniconda3/envs/b36/lib/python3.6/subprocess.py in _execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, start_new_session)
       1362                         if errno_num == errno.ENOENT:
       1363                             err_msg += ': ' + repr(err_filename)
    -> 1364                     raise child_exception_type(errno_num, err_msg, err_filename)
       1365                 raise child_exception_type(err_msg)
       1366 


    FileNotFoundError: [Errno 2] No such file or directory: 'srun': 'srun'



```python
path = '/Volumes/mbProD/Downloads/wrf_test_d01/wrfout_d01_2017-12-25_10:00:00'
# path = '/private/tmp/co_out/wrfout_d01_2017-12-25_18:00:00'
ds = xr.open_dataset(path)
variables = list(ds.variables)
compression_list = []
for var in variables:
    c = ds[var].encoding.get('complevel', 0)
    compression_list.append(c)
compression_list = np.array(compression_list)
```


```python
np.mean(compression_list)
```




    0.0




```python

```
