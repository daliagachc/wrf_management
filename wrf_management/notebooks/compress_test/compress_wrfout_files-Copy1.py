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
# %load_ext autoreload
# %autoreload 2

# %%
from useful_scit.imps import * 
import useful_scit.util.zarray as za

# %%
import wrf_management.modules.CompressOut as CO
import sqlite3


# %%
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

# %%
row = self.compress_out_df.iloc[0]

# %%
self.get_and_zip_next_row(move=True)

# %%
self.merge_update_dfs()

# %%

query = f'''
    select {CO.DATE_COL} from {self.files_table_name}
    order by {CO.DATE_COL} desc limit 1
    '''
with sqlite3.connect(self.db_path) as con:
    last_date = pd.read_sql_query(query,con).iloc[0][CO.DATE_COL]
    

# %%
last_date

# %%
query = f'''
    delete from {self.files_table_name} where {CO.DATE_COL}=={last_date}
    '''
with sqlite3.connect(self.db_path) as con:
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()


# %%

# %%
while True:
    self.get_and_zip_next_row()

# %%
sadf

# %%
CO.run_srun('hola',time_minutes=20,memory=4000,parallel_type='serial',n_cpus=1)

# %%
path = '/Volumes/mbProD/Downloads/wrf_test_d01/wrfout_d01_2017-12-25_10:00:00'
# path = '/private/tmp/co_out/wrfout_d01_2017-12-25_18:00:00'
ds = xr.open_dataset(path)
variables = list(ds.variables)
compression_list = []
for var in variables:
    c = ds[var].encoding.get('complevel', 0)
    compression_list.append(c)
compression_list = np.array(compression_list)

# %%
np.mean(compression_list)

# %%
