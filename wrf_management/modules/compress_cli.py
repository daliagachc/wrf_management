# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# todo still under construction
import sys
import wrf_management.modules.CompressOut as CO
import os

zip_path = os.path.join(os.path.dirname(sys.argv[1]),'compresser_log_xxx')
input_dic = dict(
    source_path = sys.argv[1],
    zip_path = zip_path,
    db_path = os.path.join(zip_path,f'zip{CO.get_unique_id()}.sqlite'),
    lock_last_date = False,
    source_path_is_file = True,
    compress_level_target = 4
)

if __name__=="__main__":
    co = CO.Compresser(**input_dic)
    co.get_and_zip_next_row(move=True)