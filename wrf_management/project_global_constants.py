# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import datetime as dt

# %%
import os
import wrf_management

PACKAGE_PATH = os.path.dirname(wrf_management.__file__)
ID = None
try:
    import wrf_management.pc_id as pc_id

    ID = pc_id.ID
except:
    print('no pc id found. create a pc_id.py file in the root of the package with constant ID')
# print(ID)


INIT_DATE = dt.datetime(2017, 12, 1)
END_DATE = dt.datetime(2018, 6, 1)

PATH_DATA = '/tmp/data/'

if ID == 'mac_diego':
    PATH_DB_FOLDER = os.path.join(PACKAGE_PATH, 'db_folder')
    PATH_DB_FOLDER = '/tmp/wrf_management/db_folder'
    PATH_DATA = '/Volumes/wrf_management_folder'
    PATH_DATA = '/tmp/wrf_management/data_folder'
if ID == 'taito_login':
    PATH_DB_FOLDER = os.path.join(PACKAGE_PATH, 'db_folder')
    PATH_DATA = '/wrk/aliagadi/DONOTREMOVE/wrf_management_data'

NAME_DB = 'wrf_man.sqlite'
PATH_DB = os.path.join(PATH_DB_FOLDER, NAME_DB)
MASTER_DATE_TB_NAME = 'master_date'
RUN_NAME = '2018_02_19'
RUNS_TB_NAME = 'runs_table'
UNIQUE_ID_RUN_TB_NAME = 'run_unique_id'
RUN_CONFIG_DIR = os.path.join(PACKAGE_PATH, 'config_dir', RUN_NAME)
FILE_TYPES = {
    'press' : {
        'suffix'    : 'pgrbh.tar',
        'data_tar'  : 'press_tar',
        'data_untar': 'press_untar',

    },
    'surf_0': {
        'suffix'    : 'splgrbf.tar',
        'data_tar'  : 'surf_0_tar',
        'data_untar': 'surf_0_untar',

    },
    'surf_1': {
        'suffix'    : 'sfluxgrbf.tar',
        'data_tar'  : 'surf_1_tar',
        'data_untar': 'surf_1_untar',

    }
}
