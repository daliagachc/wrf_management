# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from useful_scit.imps import *
from useful_scit.util import zarray as za
import sqlite3
import logging

LOG_LEVEL=logging.DEBUG

logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


DELETED_COL = 'deleted'

ZIPPED_COL = 'zipped'

ZIP_PATH_COL = 'zip_path'

NAME_COL = 'name'

DOM_COL = 'dom'

SOURCE_PATH_COL = 'source_path'


class Compresser:
    '''
    - this class takes the path where the original files are stored
    - it creates CompressOut objects for each available file
    - compresses the files
    - upon success, might be directed to erase the files
    - should keep track of compressed files in an sql database

    Attributes
    ----------
    source_path:str
        path to the source wrf files
    '''

    source_path: str = None
    zip_path: str = None
    db_path: str = None
    compress_out_df: pd.DataFrame = None
    files_table_name: str = None
    sqlite_df: pd.DataFrame = None

    wrfout_patt = 'wrfout'
    '''wrfout pattern'''

    pattern: str = None
    '''optional pattern to subset via glob the source path. added after wrfout_patt'''

    def __init__(self, source_path, zip_path, db_path, pattern='', files_table_name='files_table'):
        self.db_path = db_path
        self.source_path = source_path
        self.zip_path = zip_path
        self.pattern = pattern
        self.files_table_name = files_table_name
        self.set_df_from_file_list()
        try:
            logging.debug('creating db table')
            self.create_db_table_from_df()
        except:
            logging.debug('file table already exist in db')

        self.get_set_sql_df()

        # self.merge_update_dfs()

        # self.get_and_zip_next_row()

        # self.get_next_unzipped_row()

    def merge_update_dfs(self):
        self.get_set_sql_df()
        dfs = self.sqlite_df
        dff = self.compress_out_df
        joined_df = pd.merge(dfs, dff, how='outer')
        self.compress_out_df = joined_df
        df2append = dff[~dff.index.isin(dfs.index)]
        with sqlite3.connect(self.db_path) as con:
            df2append.to_sql(self.files_table_name, con, if_exists='append')
        self.get_set_sql_df()

    def get_and_zip_next_row(self):
        r = self.get_next_unzipped_row()
        zip_row(self, r)

    def get_next_unzipped_row(self):
        query = f'select * from {self.files_table_name} where {ZIPPED_COL}==0 order by {NAME_COL} limit 1'
        with sqlite3.connect(self.db_path) as con:
            df = pd.read_sql_query(query, con, index_col=NAME_COL)
        if len(df) == 0:
            logging.fatal('we are done! no more files to compress')
            sys.exit(0)

        row = df.iloc[0]
        return row

    def get_set_sql_df(self):
        query = 'select * from {} order by {}'.format(self.files_table_name,NAME_COL)
        con = sqlite3.connect(self.db_path)
        self.sqlite_df = pd.read_sql_query(query, con,index_col=NAME_COL)
        con.close()

    def create_db_table_from_df(self):
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir,exist_ok=True)
        df = self.compress_out_df
        with sqlite3.connect(self.db_path) as con:
            df.to_sql(self.files_table_name, con=con, index=True, index_label=NAME_COL)

    def set_df_from_file_list(self):
        glob_patt = os.path.join(self.source_path,
                                 self.wrfout_patt + '*' + self.pattern
                                 )
        file_list = glob.glob(glob_patt)
        df = pd.DataFrame(file_list, columns=[SOURCE_PATH_COL])
        df[DOM_COL] = df[SOURCE_PATH_COL].str.extract('d0(\d)').astype(int)

        col = df[SOURCE_PATH_COL]
        df[NAME_COL] = col.apply(lambda p: os.path.basename(p))
        df = df.set_index(NAME_COL)

        df[ZIP_PATH_COL] = df.apply(lambda r: os.path.join(self.zip_path, r.name), axis=1)
        df[ZIPPED_COL] = 0
        df[DELETED_COL] = 0

        self.compress_out_df = df


class CompressOut:
    source_path: str = None
    zip_path: str = None

    def __init__(self,
                 source_path,
                 zip_path):
        self.source_path = source_path
        self.zip_path = zip_path

        self.ds = xr.open_dataset(self.source_path)

    def get_compression_percentage(self):
        per = os.path.getsize(self.zip_path) / os.path.getsize(self.source_path)
        return int(per * 100)

    def save_zip(self, complevel=4):
        zip_dir = os.path.dirname(self.zip_path)
        os.makedirs(zip_dir,exist_ok=True)
        za.compressed_netcdf_save(self.ds, self.zip_path, complevel=complevel, fletcher32=True, encode_u=False)

def zip_row(compresser:Compresser, r):
    co = CompressOut(r.source_path,r.zip_path)
    co.save_zip()
    qdic = {
        'table_name': compresser.files_table_name,
        'zipped': ZIPPED_COL,
        'name_col': NAME_COL,
        'name': r.name
    }
    query = "update {table_name} set {zipped}=1 where {name_col}=='{name}'".format(**qdic)
    con = sqlite3.connect(compresser.db_path)
    try:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except:
        logging.debug('could not update')
    finally:
        con.close()




