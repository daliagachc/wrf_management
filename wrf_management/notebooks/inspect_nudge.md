```python
from useful_scit.imps import *
import wrf 
```


```python
path = '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/'
```


```python
gl=glob.glob(path+'wrf*')
df = pd.DataFrame(gl,columns=['path'])
gl
```




    ['/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrfinput_d03',
     '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrffdda_d01',
     '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrfinput_d01',
     '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrfinput_d04',
     '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrfinput_d02',
     '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrfbdy_d01']




```python
bo = df.path.str.contains('bdy')
bdy = df[bo]['path'].iloc[0]
bdy
```




    '/tmp/wrf_management/data_folder/runs/run_2019_02_28/real/wrfbdy_d01'




```python
bdy_d = xr.open_dataset(bdy)
# bdy_d.dims
print(str(bdy_d)[:3000])

```

    <xarray.Dataset>
    Dimensions:                                          (Time: 83, bdy_width: 5, bottom_top: 49, bottom_top_stag: 50, south_north: 85, south_north_stag: 86, west_east: 117, west_east_stag: 118)
    Dimensions without coordinates: Time, bdy_width, bottom_top, bottom_top_stag, south_north, south_north_stag, west_east, west_east_stag
    Data variables:
        Times                                            (Time) |S19 ...
        md___thisbdytimee_x_t_d_o_m_a_i_n_m_e_t_a_data_  (Time) |S19 ...
        md___nextbdytimee_x_t_d_o_m_a_i_n_m_e_t_a_data_  (Time) |S19 ...
        U_BXS                                            (Time, bdy_width, bottom_top, south_north) float32 ...
        U_BXE                                            (Time, bdy_width, bottom_top, south_north) float32 ...
        U_BYS                                            (Time, bdy_width, bottom_top, west_east_stag) float32 ...
        U_BYE                                            (Time, bdy_width, bottom_top, west_east_stag) float32 ...
        U_BTXS                                           (Time, bdy_width, bottom_top, south_north) float32 ...
        U_BTXE                                           (Time, bdy_width, bottom_top, south_north) float32 ...
        U_BTYS                                           (Time, bdy_width, bottom_top, west_east_stag) float32 ...
        U_BTYE                                           (Time, bdy_width, bottom_top, west_east_stag) float32 ...
        V_BXS                                            (Time, bdy_width, bottom_top, south_north_stag) float32 ...
        V_BXE                                            (Time, bdy_width, bottom_top, south_north_stag) float32 ...
        V_BYS                                            (Time, bdy_width, bottom_top, west_east) float32 ...
        V_BYE                                            (Time, bdy_width, bottom_top, west_east) float32 ...
        V_BTXS                                           (Time, bdy_width, bottom_top, south_north_stag) float32 ...
        V_BTXE                                           (Time, bdy_width, bottom_top, south_north_stag) float32 ...
        V_BTYS                                           (Time, bdy_width, bottom_top, west_east) float32 ...
        V_BTYE                                           (Time, bdy_width, bottom_top, west_east) float32 ...
        W_BXS                                            (Time, bdy_width, bottom_top_stag, south_north) float32 ...
        W_BXE                                            (Time, bdy_width, bottom_top_stag, south_north) float32 ...
        W_BYS                                            (Time, bdy_width, bottom_top_stag, west_east) float32 ...
        W_BYE                                            (Time, bdy_width, bottom_top_stag, west_east) float32 ...
        W_BTXS                                           (Time, bdy_width, bottom_top_stag, south_north) float32 ...
        W_BTXE                                           (Time, bdy_width, bottom_top_stag, south_north) float32 ...
        W_BT



```python
bo = df.path.str.contains('fdda')
dda = df[bo]['path'].iloc[0]
```


```python
# dda_d.close()
dda_d = xr.open_dataset(dda)
print(str(dda_d)[:2000])
# dda_d.Times
```

    <xarray.Dataset>
    Dimensions:     (Time: 83, bottom_top: 49, one_stag: 1, south_north: 85, west_east: 117)
    Dimensions without coordinates: Time, bottom_top, one_stag, south_north, west_east
    Data variables:
        Times       (Time) |S19 ...
        U_NDG_OLD   (Time, bottom_top, south_north, west_east) float32 ...
        V_NDG_OLD   (Time, bottom_top, south_north, west_east) float32 ...
        T_NDG_OLD   (Time, bottom_top, south_north, west_east) float32 ...
        Q_NDG_OLD   (Time, bottom_top, south_north, west_east) float32 ...
        PH_NDG_OLD  (Time, bottom_top, south_north, west_east) float32 ...
        U_NDG_NEW   (Time, bottom_top, south_north, west_east) float32 ...
        V_NDG_NEW   (Time, bottom_top, south_north, west_east) float32 ...
        T_NDG_NEW   (Time, bottom_top, south_north, west_east) float32 ...
        Q_NDG_NEW   (Time, bottom_top, south_north, west_east) float32 ...
        PH_NDG_NEW  (Time, bottom_top, south_north, west_east) float32 ...
        MU_NDG_OLD  (Time, one_stag, south_north, west_east) float32 ...
        MU_NDG_NEW  (Time, one_stag, south_north, west_east) float32 ...
    Attributes:
        TITLE:                            OUTPUT FROM REAL_EM V4.0.3 PREPROCESSOR
        START_DATE:                      2017-12-02_00:00:00
        WEST-EAST_GRID_DIMENSION:        118
        SOUTH-NORTH_GRID_DIMENSION:      86
        BOTTOM-TOP_GRID_DIMENSION:       50
        DX:                              38000.0
        DY:                              38000.0
        AERCU_OPT:                       0
        AERCU_FCT:                       1.0
        IDEAL_CASE:                      0
        DIFF_6TH_SLOPEOPT:               0
        AUTO_LEVELS_OPT:                 2
        DIFF_6TH_THRESH:                 0.1
        DZBOT:                           50.0
        DZSTRETCH_S:                     1.3
        DZSTRETCH_U:                     1.1
        GRIDTYPE:                        C
        DIFF_OPT:                        2
        KM_OPT:                          4
        DAMP_OPT:                        3
        DAMPCOEF:                        0.



```python

```
