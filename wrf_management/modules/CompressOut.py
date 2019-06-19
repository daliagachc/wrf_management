# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import shutil
import uuid
from pathlib import Path

from useful_scit.imps import *
from useful_scit.util import zarray as za
import sqlite3
import subprocess
import logging

SYMLINK_COL = 'symlink'

ORIG_COMP_LEVEL_COL = 'orig_comp_level'
LOG_LEVEL = logging.DEBUG
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

LAST_DATE_COL = 'last_date_lock'

DATE_COL = 'unix_time'

LOCKED_COL = 'locked'

MOVED_COL = 'moved'

ZIPPED_COL = 'zipped'

ZIP_PATH_COL = 'zip_path'

NAME_COL = 'file_name'

INDEX_COL = 'index_col'

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

    lock_last_date: bool = True
    '''avoid any modification on the last date (in case a program is running'''

    date_pattern:str = None

    compress_level_target = 4
    '''the compress level target'''

    source_path_is_file = False
    '''is source_path true, no pattern matching is used'''

    def __init__(self,
                 source_path,
                 zip_path,
                 db_path,
                 pattern='',
                 files_table_name='files_table',
                 lock_last_date = True,
                 wrfout_patt='wrfout',
                 date_pattern='%Y-%m-%d_%H:%M:%S',
                 compress_level_target = 4,
                 source_path_is_file = False
                 ):
        self.source_path_is_file = source_path_is_file
        self.compress_level_target = compress_level_target
        self.date_pattern = date_pattern
        self.wrfout_patt = wrfout_patt
        self.db_path = db_path
        self.source_path = source_path
        self.zip_path = zip_path
        self.pattern = pattern
        self.files_table_name = files_table_name
        self.lock_last_date = lock_last_date
        self.set_df_from_file_list()
        # return None
        try:
            logging.debug('creating db table')
            self.create_db_table_from_df()
        except:
            logging.debug('file table already exist in db')

        self.get_set_sql_df()
        self.set_reset_lock_last_date()

        # self.merge_update_dfs()

        # self.get_and_zip_next_row()

        # self.get_next_unzipped_row()

    def merge_update_dfs(self):
        self.get_set_sql_df()
        dfs = self.sqlite_df
        self.set_df_from_file_list()
        dff = self.compress_out_df
        # return [dfs, dff]
        joined_df = pd.merge(dfs, dff, how='outer')
        self.compress_out_df = joined_df
        df2append = dff[~dff.index.isin(dfs.index)]
        # return df2append
        with sqlite3.connect(self.db_path) as con:
            df2append.to_sql(self.files_table_name, con, if_exists='append')
        self.get_set_sql_df()

    def get_and_zip_next_row(self, move=False):
        r = self.get_next_unzipped_row()
        logging.debug('compressing:' + r.name)
        zip_row(self, r,complevel=self.compress_level_target)
        if move:
            self.move_zip_file_to_source_file(r)

    def get_next_unzipped_row(self):
        query = f"""
        select * from {self.files_table_name} 
        where {ZIPPED_COL}==0 and {LOCKED_COL}==0 and {LAST_DATE_COL} == 0 and {MOVED_COL} == 0 
        order by {DATE_COL} limit 1
        """

        with sqlite3.connect(self.db_path) as con:
            # con: sqlite3.Connection = con
            con.isolation_level = 'EXCLUSIVE'
            con.execute('BEGIN EXCLUSIVE')

            df = pd.read_sql_query(query, con, index_col=NAME_COL)
            if len(df) == 0:
                logging.fatal('we are done! no more files to compress')
                sys.exit(0)
            row = df.iloc[0]
            query = f"update {self.files_table_name} set {LOCKED_COL}=1 where {NAME_COL}=='{row.name}'"
            cu = con.cursor()
            cu.execute(query)


            con.commit()
            # conn.close()
        return row

    def drop_files_table(self):
        query = f"""
        drop table {self.files_table_name}
        """
        with sqlite3.connect(self.db_path) as con:
            cursor: sqlite3.Cursor = con.cursor()
            cursor.execute(query)
            con.commit()

    def get_set_sql_df(self):
        # todo change name_col to date_col
        query = 'select * from {} order by {}'.format(self.files_table_name, DATE_COL)
        con = sqlite3.connect(self.db_path)
        self.sqlite_df = pd.read_sql_query(query, con, index_col=INDEX_COL)
        con.close()

    def set_reset_lock_last_date(self):
        query1 = f'''
        update {self.files_table_name}
        set {LAST_DATE_COL} = 0
        '''
        query2 = f'''
        select {DATE_COL} from {self.files_table_name}
        order by {DATE_COL} desc limit 1
        '''
        with sqlite3.connect(self.db_path) as con:
            last_date = pd.read_sql_query(query2,con).iloc[0][DATE_COL]
            query3 = f'''
            update {self.files_table_name}
            set {LAST_DATE_COL} = 1
            where {DATE_COL} == {last_date}
            '''
            cursor:sqlite3.Cursor = con.cursor()
            cursor.execute(query1)
            if self.lock_last_date:
                cursor.execute(query3)
            con.commit()


    def create_db_table_from_df(self):
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        df = self.compress_out_df
        with sqlite3.connect(self.db_path) as con:
            df.to_sql(self.files_table_name, con=con, index=True, index_label=INDEX_COL)

    def set_df_from_file_list(self):
        glob_patt = os.path.join(self.source_path,
                                 self.wrfout_patt + '*' + self.pattern
                                 )
        if self.source_path_is_file:
            glob_patt = self.source_path

        file_list = glob.glob(glob_patt)
        logging.debug(f'number of files is {len(file_list)}')

        if len(file_list)==0:
            logging.debug('no match. aborting')
            sys.exit(1)

        df = pd.DataFrame(file_list, columns=[SOURCE_PATH_COL])

        df[SYMLINK_COL] = df[SOURCE_PATH_COL].apply(lambda p: check_if_path_symlink(p))

        df = df[~df[SYMLINK_COL]]
        df = df.drop(SYMLINK_COL,axis=1)

        logging.debug(f'number of file remaining after dropping symlinks is {len(df)}')

        is_netcdf = 'is_netcdf'
        df[is_netcdf]=df[SOURCE_PATH_COL].apply(lambda p: check_net_cdf(p))
        df = df[df[is_netcdf]]
        df = df.drop(is_netcdf,axis=1)
        logging.debug(f'number of file remaining after dropping not cdf files is {len(df)}')


        df[ORIG_COMP_LEVEL_COL] = df[SOURCE_PATH_COL].apply(lambda p: get_compression_level(p))

        df = df[df[ORIG_COMP_LEVEL_COL]<self.compress_level_target]

        logging.debug(f'number of files with compress level lower than target is {len(df)}')

        if len(df) == 0:
            logging.critical(f'all files already compressed or no files matched pattern. exiting')
            sys.exit(1)

        df[DOM_COL] = df[SOURCE_PATH_COL].str.extract('d0(\d)').astype(int)

        col = df[SOURCE_PATH_COL]
        df[NAME_COL] = col.apply(lambda p: os.path.basename(p))
        df = df.set_index(NAME_COL, drop=False)
        df.index.name = INDEX_COL
        str_col = df[NAME_COL].str
        str_col = str_col.extract('(\d\d\d\d-\d\d-\d\d_\d\d:\d\d:\d\d)')
        str_col = pd.to_datetime(str_col[0], format=self.date_pattern)
        str_col = str_col.astype(np.int64)
        df[DATE_COL] = str_col

        df[ZIP_PATH_COL] = df.apply(lambda r: os.path.join(self.zip_path, r.name), axis=1)
        df[ZIPPED_COL] = 0
        df[MOVED_COL] = 0
        df[LOCKED_COL] = 0
        df[LAST_DATE_COL] = 0

        self.compress_out_df = df

    def move_zip_file_to_source_file(self, row):
        #check row is not locked
        with sqlite3.connect(self.db_path) as con:
            con.isolation_level = 'EXCLUSIVE'
            con.execute('BEGIN EXCLUSIVE')

            query = f"select {LOCKED_COL} from {self.files_table_name} where {INDEX_COL}=='{row.name}'"
            df = pd.read_sql_query(query,con)
            locked = df.iloc[0][LOCKED_COL]
            # return locked
            if locked == 1:
                logging.critical(f'row {row.name} is locked. aborting')
                sys.exit(1)

            query = f"update {self.files_table_name} set {LOCKED_COL}=1 where {INDEX_COL}=='{row.name}'"

            cursor:sqlite3.Cursor = con.cursor()
            cursor.execute(query)
            con.commit()

        original = row[SOURCE_PATH_COL]
        zipped = row[ZIP_PATH_COL]
        original_back_up = f'{zipped}_source_back_up_{get_unique_id()}'
        check = check_source_zip_identical(original,zipped)
        if check:
            shutil.copy(original,original_back_up)
            shutil.move(zipped,original)
            logging.debug({f'moving {zipped} to {original}'})
            check_again = check_source_zip_identical(original,original_back_up)
            if check_again:
                logging.debug(f'double check fine. deleting {original_back_up}')
                os.remove(original_back_up)
                query = f"update {self.files_table_name} set {MOVED_COL}=1, {LOCKED_COL}=0 where {INDEX_COL}=='{row.name}'"
                self.execute_query(query)
            else:
                logging.critical(f'critical error {original} and {original_back_up} are not identical. aborting')
                sys.exit(1)
        else:
            logging.critical(f'{original} and {zipped} are not identical. We aer aborting')
            sys.exit(1)

    def execute_query(self,query):
        with sqlite3.connect(self.db_path) as con:
            c:sqlite3.Connection = con
            cursor = c.cursor()
            cursor.execute(query)
            c.commit()

    def reset_locks(self):
        '''
        setting all locks to 0
        Returns
        -------

        '''
        query = f"update {self.files_table_name} set {LOCKED_COL}=0"
        logging.debug('resetting all locks to 0')
        self.execute_query(query)


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
        os.makedirs(zip_dir, exist_ok=True)
        za.compressed_netcdf_save(self.ds, self.zip_path, complevel=complevel, fletcher32=True, encode_u=False)




def zip_row(compresser: Compresser, r, complevel):
    co = CompressOut(r.source_path, r.zip_path)
    co.save_zip(complevel=complevel)
    qdic = {
        'table_name': compresser.files_table_name,
        'zipped'    : ZIPPED_COL,
        'name_col'  : NAME_COL,
        'name'      : r.name,
        'lock'      : LOCKED_COL,
    }
    query = """
    update {table_name} 
    set {zipped}=1, {lock}=0
    where {name_col}=='{name}'
    """.format(**qdic)
    con = sqlite3.connect(compresser.db_path)
    try:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except:
        logging.debug('could not update')
        sys.exit(1)
    finally:
        con.close()


def check_source_zip_identical(path1,path2):
    ds1 = xr.open_dataset(path1)
    ds2 = xr.open_dataset(path2)
    return ds1.identical(ds2)



def run_srun(exe:str, *,
             time_minutes,
             memory,
             parallel_type,
             n_cpus,
             message = 'jup '

             ):
    cmd = ['srun',
           '-t',f'{time_minutes}',
           '-p',parallel_type,
           '-c',f'{n_cpus}',
           '--mem', f'{memory}',
           exe
           ]
    logging.debug(cmd)
    subprocess.Popen(cmd)
    return cmd

def get_compression_level(path):
    ds = xr.open_dataset(path)
    variables = list(ds.variables)
    compression_list = []
    for var in variables:
        c = ds[var].encoding.get('complevel', 0)
        compression_list.append(c)
    compression_list = np.array(compression_list)
    mean = np.mean(compression_list)
    ds.close()

    logging.debug(f'mean compresion level for {path} is {mean}')
    return mean

def get_unique_id():
    id = uuid.uuid4()
    return id

def check_if_path_symlink(path):
    return Path(path).is_symlink()

def check_net_cdf(path):
    try:
        ds = xr.open_dataset(path)
        is_netcdf = True
        ds.close()
    except:
        is_netcdf = False
    return is_netcdf