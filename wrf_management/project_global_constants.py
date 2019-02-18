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
import platform

PLATFORM = platform.platform()

INIT_DATE = dt.datetime(2017, 12, 1)
END_DATE = dt.datetime(2018, 6, 1)

PATH_DATA = '/tmp/data/'

PATH_DB_FOLDER = '/homeappl/home/aliagadi/saltena_2018/wrf_management/wrf_management/db_folder'
PATH_DATA = '/wrk/aliagadi/DONOTREMOVE/wrf_management_data'
NAME_DB = 'wrf_man.sqlite'
PATH_DB = os.path.join(PATH_DB_FOLDER, NAME_DB)
MASTER_DATE_TB_NAME = 'master_date'

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
