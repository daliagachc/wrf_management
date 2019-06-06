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
import wrf_management.utilities as ut
import importlib
importlib.reload(ut);
import wrf_management.project_global_constants as gc
importlib.reload(gc)
import wrf_management.geogrid as geo
import os
import sqlite3 as sq
import pandas as pd
import wrf_management.base_namelists.base_namelists as bn
importlib.reload(bn);
import f90nml

# %%
gc.PATH_DB

# %%
con = sq.connect(gc.PATH_DB)

# %%
pd.read_sql('select * from sqlite_master',con)

# %%
df = pd.DataFrame(
    [{
        'run_name':gc.RUN_NAME,
        'unique_id':'2019-02-21T15-04-27_476148_geogrid',
        'program':'geogrid',
        'comments':'exploring geogrid',
     }]
)
df=df.set_index('unique_id')

# %%
# df.to_sql(gc.UNIQUE_ID_RUN_TB_NAME,con,if_exists='replace',index_label='unique_id')

# %%
run_path = ut.get_run_data_path()
os.makedirs(run_path, exist_ok=True)

# %%
import datetime as dt 

# %%
unique_id = ut.get_unique_id()

# %%
unique_id

# %%
ut.list_table_names()

# %%
df = ut.get_tb_from_name(tb_name='run_unique_id')

# %%
df

# %%
path = '/private/tmp/wrf_management/data_folder/runs/2018_02_19/2019-02-21T15-04-27_476148_geogrid/namelist.wps'

# %%
importlib.reload(bn);
o1,o2,o3 = bn.sanity_check(path_wps=path,path_wrf='../config_dir/run_2018_02_19/namelist.wps')

# %%
o1

# %%
o2[o2['pass'] == False]

# %%
in_path = '../config_dir/2018_02_19/namelist.wps'
ou_path = '/tmp/borrar.wps'
importlib.reload(geo)
geo.skim_namelist(in_path, ou_path)

# %%
ut.get_tb_from_name(tb_name='run_unique_id')

# %%
UID = '2019-02-21T15-04-27_476148_geogrid'

# %%
upath = os.path.join(gc.PATH_DATA,'runs','2018_02_19',UID)
print(upath)
ou_path = os.path.join(upath,'namelist.wps')

# %%
os.remove(ou_path)
geo.skim_namelist(in_path,ou_path)

# %%
importlib.reload(ut)
program = 'ungrib'
unique_id = ut.get_unique_id(program)
print(unique_id)
unique_id = '2019-02-21T17-29-01_753696_ungrib'

# %%
importlib.reload(ut)
new_path = ut.get_new_unique_path_for_program(unique_id=unique_id)
print(new_path)
new_path = '/tmp/wrf_management/data_folder/runs/2018_02_19/2019-02-21T17-29-01_753696_ungrib'

# %%
importlib.reload(ut)
ut.add_unique_id_run_db(unique_id=unique_id+'_ungrib',program_nm='ungrib',comment='first run')
con.commit()

# %%
ut.get_tb_from_name(tb_name='run_unique_id')

# %%
ut.list_table_names()

# %%
date_to_ungrib = '2017-12-15'

# %%
rows = {}
for tb in gc.FILE_TYPES.keys():
#     print(tb)
    sql = """
    select * from {tb} where date(date)=date('{dt}')
    """.format(tb=tb,dt=date_to_ungrib)
    rows[tb]=pd.read_sql(sql,con)
    rows[tb]['tb']=tb
df = pd.concat(list(rows.values()))
if df.downloaded.all()!=True: print('not all downloaded')
df


# %%
df['tar_path']=df.apply(lambda r: os.path.join(ut.get_tar_path(r.tb),r['name']),
         axis = 1)
df['untar_path']=df.apply(lambda r: new_path,
         axis = 1)
row = df.iloc[0]
df


# %%
import tarfile
tfile = tarfile.TarFile(row.tar_path)

# %%
tfile.extractall(row.untar_path)

# %%
con.close()

# %%
import f90nml
from collections import OrderedDict


def skim_namelist(
        input_path, output_path, *,date, prefix
    ):
    old_dic = f90nml.read(input_path)
    
    dt_object = pd.to_datetime(date)
    d_init = dt_object.strftime('%Y-%m-%d_%T')
    d_end = dt_object + pd.DateOffset(hours=18)
    d_end = d_end.strftime('%Y-%m-%d_%T')
    
    old_dic['share']['start_date']=old_dic['share']['max_dom']*[d_init]
    old_dic['share']['end_date']=old_dic['share']['max_dom']*[d_end]
    old_dic['share']['interval_seconds']=6*3600
    old_dic['ungrib']['prefix']=prefix
    sections = ['share','ungrib']
    drops = {}
    new_dic = OrderedDict()
    for s in sections:
        new_dic[s]= old_dic[s]
        if s in drops.keys():
            for d in drops[s]:
                new_dic[s].pop(d)
    f90nml.write(new_dic, output_path)
    return new_dic

# %%
try:os.remove('/tmp/borrar')
except:pass    
skim_namelist('../config_dir/2018_02_19/namelist.wps','/tmp/borrar',date=date_to_ungrib,prefix='PRESSURE')

# %%
date_to_ungrib = '2017-12-15' 
date = date_to_ungrib

# %%
dt_object = pd.to_datetime(date)
d_init = dt_object.strftime('%Y-%m-%d_%T')

# %%
d_end = dt_object + pd.DateOffset(hours=18)
d_end = d_end.strftime('%Y-%m-%d_%T')
d_end

# %%

