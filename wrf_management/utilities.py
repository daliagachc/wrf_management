# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import os
import sqlite3 as sq
import pandas as pd
from wrf_management import project_global_constants as gc


def create_date_db(init_date=gc.INIT_DATE,
                   end_date=gc.END_DATE,
                   db_path=gc.PATH_DB_FOLDER,
                   tb_name=gc.MASTER_DATE_TB_NAME,
                   override=False,
                   db_name=gc.NAME_DB
                   ):
    """

    Parameters
    ----------
    init_date
    end_date
    db_path
    tb_name
    override

    Returns
    -------

    """
    date_index = pd.date_range(
        start=init_date,
        end=end_date
    )

    df = pd.DataFrame(date_index, columns=['date'])
    df = df.reset_index()
    df = df.set_index('date')
    df = df.rename(columns={'index': 'i'})

    os.makedirs(db_path, exist_ok=True)

    db_con_path = os.path.join(db_path, db_name)
    con = sq.connect(db_con_path)
    try:
        df.to_sql(tb_name, con)
    except:
        print('could not create the table maybe it exists already')
    finally:
        con.close()


def get_date_tb(
        path_db=gc.PATH_DB,
        tb_name=gc.MASTER_DATE_TB_NAME
):
    """

    Parameters
    ----------
    path_db
    tb_name

    Returns
    -------
    df : pandas.DataFrame

    """
    con = sq.connect(path_db)
    try:
        st = 'select * from {}'.format(tb_name)
        df = pd.read_sql_query(st, con, index_col='date')
    finally:
        con.close()
    return df


def get_tb_from_name(*,
                     path_db=gc.PATH_DB,
                     tb_name
                     ):
    """

    Parameters
    ----------
    path_db
    tb_name

    Returns
    -------
    df : pandas.DataFrame

    """
    con = sq.connect(path_db)
    try:
        st = 'select * from {}'.format(tb_name)
        df = pd.read_sql_query(st, con, index_col='date')
    finally:
        con.close()
    return df


def create_download_db(
        *,
        path_db=gc.PATH_DB,
        db_name,
        override=False,
        date_tb_name=gc.MASTER_DATE_TB_NAME,
):
    date_db = get_date_tb(path_db, date_tb_name)
    date_db['downloaded'] = False
    # date_db['tar_path'] = False
    date_db['name'] = False
    date_db['untarred'] = False
    # date_db['untar_path'] = False

    down_db = date_db.copy()
    con = sq.connect(path_db)
    try:
        down_db.to_sql(db_name, con)
    except:
        print('could not create. it might exist already')
    finally:
        con.close()


def get_down_string_from_row(*, row, ftype):
    suffix = gc.FILE_TYPES[ftype]['suffix']
    date = row.date
    date_pd = pd.to_datetime(str(date))
    date_string = date_pd.strftime('%Y%m%d')
    string_template = '{y}/cdas1.{date_string}.{suffix}'
    string = string_template.format(y=date_pd.year, date_string=date_string, suffix=suffix)
    return string


def get_next_row_to_down(
        *,
        tb_name,
        db_path=gc.PATH_DB,
):
    con = sq.connect(db_path)
    try:
        st = '''
        select * from {tb} 
        where downloaded = 0
        order by date 
        limit 1
        '''.format(tb=tb_name)
        row = pd.read_sql(st, con)
        ll = len(row)
        # print(ll)
        if ll < 1:
            raise SystemExit('no more rows to download')
    finally:
        con.close()
    return row.iloc[0]


def update_sucess_down(
        *, row, tb_name, db_path=gc.PATH_DB
):
    i = row.i
    con = sq.connect(db_path)
    try:
        st = '''
        update {tb} 
        set downloaded=1
        where i={i}
        '''
        st = st.format(tb=tb_name, i=i)
        print(st)
        c = con.cursor()
        c.execute(st)
        con.commit()
    finally:
        con.close()

def update_row_name(
        *, row, tb_name, down_string, db_path=gc.PATH_DB
):
    i = row.i
    name = os.path.basename(down_string)
    con = sq.connect(db_path)
    try:
        st = '''
        update {tb} 
        set name='{name}'
        where i={i}
        '''
        st = st.format(tb=tb_name, i=i, name=name)
        print(st)
        c = con.cursor()
        c.execute(st)
        con.commit()
    finally:
        con.close()

def down_file_from_str(
        file_str, down_folder,
):
    import sys
    import os
    import urllib.request, urllib.error, urllib.parse
    import http.cookiejar
    #
    verbose = True
    #
    cj = http.cookiejar.MozillaCookieJar()
    processor = urllib.request.HTTPCookieProcessor(cj)
    print('processor', processor)
    opener = urllib.request.build_opener(processor)

    print(opener)
    #
    # check for existing cookies file and authenticate if necessary
    do_authentication = False
    if (os.path.isfile("auth.rda.ucar.edu")):
        cj.load("auth.rda.ucar.edu", False, True)
        for cookie in cj:
            if (cookie.name == "sess" and cookie.is_expired()):
                do_authentication = True
    else:
        do_authentication = True

    if (do_authentication):
        login_string = "email=diego.aliaga@helsinki.fi&password=22711253N&action=login"
        print('login', login_string)
        login_string_encoded = login_string.encode('utf-8')
        login = opener.open(
            "https://rda.ucar.edu/cgi-bin/login",
            login_string_encoded
        )
        #
        # save the authentication cookies for future downloads
        # NOTE! - cookies are saved for future sessions because overly-frequent authentication to our server can cause your data access to be blocked
        cj.clear_session_cookies()
        cj.save("auth.rda.ucar.edu", True, True)
    #
    # download the data file(s)
    listoffiles = [file_str]
    for file in listoffiles:
        idx = file.rfind("/")
        if (idx > 0):
            ofile = file[idx + 1:]
        else:
            ofile = file
        if (verbose):
            sys.stdout.write("downloading " + ofile + "...")
            sys.stdout.flush()
        infile = opener.open("http://rda.ucar.edu/data/ds094.0/" + file)
        down_path = os.path.join(down_folder, ofile)
        os.makedirs(down_folder, exist_ok=True)
        is_downloaded = False
        try:
            outfile = open(down_path, "wb",)
            outfile.write(infile.read())
            outfile.close()
            is_downloaded = True
        except:
            print('failed to download')
            os.remove(down_path)
            print('removing unfinished path')

        return is_downloaded


def get_tar_path(
        tb_name
    ):
    tar_path = gc.FILE_TYPES[tb_name]['data_tar']
    tar_path = os.path.join(gc.PATH_DATA,tar_path)
    return tar_path
