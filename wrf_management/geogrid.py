# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

"""
this package is a layer for geogrid wps
"""
import f90nml
from collections import OrderedDict


def skim_namelist(
        input_path, output_path
    ):
    old_dic = f90nml.read(input_path)
    sections = ['share','geogrid']
    drops = {'share':['end_date','start_date','interval_seconds']}
    new_dic = OrderedDict()
    for s in sections:
        new_dic[s]= old_dic[s]
        if s in drops.keys():
            for d in drops[s]:
                new_dic[s].pop(d)
    f90nml.write(new_dic, output_path)
    return new_dic


