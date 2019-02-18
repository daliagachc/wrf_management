# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import os

import pandas as pd


def create_date_db(init_date, end_date, path, db_name='master_date',
                   override = False):
    date_index = pd.date_range(
        start=init_date,
        end=end_date
    )

    df = pd.DataFrame(date_index, columns=['date'])
    df = df.reset_index()
    df = df.set_index('date')
    df = df.rename(columns={'index': 'i'})

    os.makedirs(path, exist_ok=True)

    db_path = os.path.join(path, db_name)
    if os.path.isfile(db_path) and override is not True:
        print('db exist and is not overriden')
        df = False
    else:
        df.to_csv(db_path)
    return df
