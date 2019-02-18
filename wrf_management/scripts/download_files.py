# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: ''
#     name: ''
# ---

# %%
import wrf_management.utilities as ut
import wrf_management.project_global_constants as gc

# %%
ut.create_date_db(override=True)

# %%
ut.get_date_tb().sample()

# %%
for k in gc.FILE_TYPES:
    print(k)
    ut.create_download_db(db_name=k,override=True)

# %%
i=0
ii = 10
while i < ii:
    for ftype in gc.FILE_TYPES:
        print(ftype)
        row = ut.get_next_row_to_down(tb_name=ftype,)
        down_str = ut.get_down_string_from_row(row=row,ftype=ftype)
        print(down_str)
        tar_path = ut.get_tar_path(ftype)
        print(tar_path)
        res = ut.down_file_from_str(down_str,tar_path)
        if res:
            ut.update_sucess_down(row=row,tb_name=ftype)
            ut.update_row_name(row=row,tb_name=ftype,down_string=down_str)
    i=i+1

# %%


