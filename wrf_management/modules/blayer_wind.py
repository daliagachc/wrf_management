# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import wrf
from useful_scit.imps import *
from netCDF4 import Dataset

CHC_LAT = -15.713716
CHC_LON = -68.082038
LPB_LAT = -17.125251
LPB_LON = -68.187013
ua, va, wa = 'ua', 'va', 'wa'
pblh = 'PBLH'
z = 'z'
ter = 'ter'
uvmet_wspd_wdir = 'uvmet_wspd_wdir'
uvmet = 'uvmet'
TKE_PBL = 'TKE_PBL'
x, y, lat, lon = 'x', 'y', 'lat', 'lon'
xy_loc = 'xy_loc'

d3_vars = [ua, va, wa, uvmet, uvmet_wspd_wdir, z, TKE_PBL]
d2_vars = [ter, pblh]
all_vars = [*d3_vars, *d2_vars]

cross_line = 'cross_line_ll'
bottom_top_stag = 'bottom_top_stag'

end_point = wrf.CoordPair(lat=CHC_LAT, lon=CHC_LON)
start_point = wrf.CoordPair(lat=LPB_LAT, lon=LPB_LON)


def compressed_netcdf_save(ds, path):
    encoding = {}
    for k, v in ds.variables.items():
        encoding[k] = {'zlib': True, 'shuffle': True}
        if v.dtype.kind == 'U':
            encoding[k]['dtype'] = 'S1'
    ds.to_netcdf(path, encoding=encoding)


def get_ver_cross(path):
    ncfile = Dataset(path, mode='r')
    ds = extract_all_vars(TKE_PBL, all_vars, ncfile)
    ver_cross = cross_3d_vars(cross_line, d3_vars, ds, end_point, start_point, z, ncfile)
    line_cross = cross_2d_vars(cross_line, d2_vars, ds, end_point, start_point, ncfile)
    ver_cross = merge_cross(d2_vars, line_cross, ver_cross)
    ver_cross = fix_xy_loc(lat, lon, ver_cross, x, xy_loc, y)
    ver_cross = get_rid_of_attrs(ver_cross)
    return ver_cross


def get_rid_of_attrs(ver_cross):
    for v in ver_cross.variables:
        try:
            del ver_cross[v].attrs['projection']
        except:
            pass
        try:
            del ver_cross[v].attrs['coordinates']
        except:
            pass
    return ver_cross


def fix_xy_loc(lat, lon, ver_cross, x, xy_loc, y):
    labels = [x, y, lat, lon]
    df = ver_cross[xy_loc].reset_coords().to_dataframe()
    for l in labels:
        df[l] = df.apply(lambda r: get_out(r[xy_loc], l), axis=1)
        ver_cross[l] = df[l].to_xarray()
    ver_cross = ver_cross.drop(xy_loc)
    return ver_cross


def merge_cross(d2_vars, line_cross, ver_cross):
    for v in d2_vars:
        ver_cross[v] = line_cross[v]
    return ver_cross


def cross_2d_vars(cross_line, d2_vars, ds, end_point, start_point, ncfile)->xr.Dataset:
    line_cross = xr.Dataset()
    for v in d2_vars:
        line_cross[v] = wrf.interpline(ds[v], wrfin=ncfile, start_point=start_point,
                                       end_point=end_point, latlon=True, meta=True)
    line_cross = line_cross.rename(**{'line_idx': cross_line})
    return line_cross


def cross_3d_vars(cross_line, d3_vars, ds, end_point, start_point, z, ncfile
                  )->xr.Dataset:
    ver_cross = xr.Dataset()
    for v in d3_vars:
        ver_cross[v] = wrf.vertcross(ds[v], ds[z], wrfin=ncfile, start_point=start_point,
                                     end_point=end_point, latlon=True, meta=True)
    ver_cross = ver_cross.rename(**{'cross_line_idx': cross_line})
    return ver_cross


def extract_all_vars(TKE_PBL, all_vars, ncfile):
    ds = xr.Dataset()
    for v in all_vars:
        ds[v] = wrf.getvar(ncfile, v,
                           timeidx=wrf.ALL_TIMES
                           )
    ds[TKE_PBL] = wrf.destagger(ds[TKE_PBL], 1, meta=True)
    return ds


def get_out(r, l):
    return getattr(r, l)






def read_and_spit(
        glob_pat,
        path_out,
        drop_last=True
    ):
    # %%
    os.makedirs(path_out,exist_ok=True)
    files = glob.glob(glob_pat)
    files.sort()
    if drop_last:
        files=files[:-1]


    for file in files:
        print(file)
    # file = files[0]
        base_name = os.path.basename(file)
        file_out = os.path.join(path_out,base_name)
        ver_cross = get_ver_cross(file)
        compressed_netcdf_save(ver_cross,file_out)
