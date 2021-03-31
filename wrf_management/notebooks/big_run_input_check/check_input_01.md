```python
from useful_scit.imps import *
from check_input_01_funs import * 
```


```python
path = '/Volumes/mbProD/Downloads/wrf_small_files'
```


```python
glob.glob(path+'/wrf*')
```




    ['/Volumes/mbProD/Downloads/wrf_small_files/wrfbdy_d0_short',
     '/Volumes/mbProD/Downloads/wrf_small_files/wrffdda_d0_short',
     '/Volumes/mbProD/Downloads/wrf_small_files/wrfinput_d01',
     '/Volumes/mbProD/Downloads/wrf_small_files/wrflowinp_d01']




```python
file_path = os.path.join(path,'wrfinput_d01')
```


```python
xa = xr.open_dataset(file_path).isel(Time=0)
list(xa.dims)
```




    ['DIM0010',
     'bottom_top',
     'bottom_top_stag',
     'dust_erosion_dimension',
     'land_cat_stag',
     'num_ext_model_couple_dom_stag',
     'soil_cat_stag',
     'soil_layers_stag',
     'south_north',
     'south_north_stag',
     'west_east',
     'west_east_stag']




```python
xa.coords
```




    Coordinates:
        XLAT     (south_north, west_east) float32 ...
        XLONG    (south_north, west_east) float32 ...
        XLAT_U   (south_north, west_east_stag) float32 ...
        XLONG_U  (south_north, west_east_stag) float32 ...
        XLAT_V   (south_north_stag, west_east) float32 ...
        XLONG_V  (south_north_stag, west_east) float32 ...




```python
for v in list(xa.variables):
    try: 
        desc = xa[v].description
    except: desc = ''
    fig, ax = plt.subplots()
    ax.set_title(desc)
    ax.set_xlabel(v)
    try:
        sns.distplot(xa[v].values.flatten())
    except: 
        pass
        
        
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/matplotlib/pyplot.py:514: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      max_open_warning, RuntimeWarning)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/numpy/core/_methods.py:140: RuntimeWarning: Degrees of freedom <= 0 for slice
      keepdims=keepdims)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/numpy/core/_methods.py:132: RuntimeWarning: invalid value encountered in double_scalars
      ret = ret.dtype.type(ret / rcount)



![png](check_input_01_files/check_input_01_6_1.png)



![png](check_input_01_files/check_input_01_6_2.png)



![png](check_input_01_files/check_input_01_6_3.png)



![png](check_input_01_files/check_input_01_6_4.png)



![png](check_input_01_files/check_input_01_6_5.png)



![png](check_input_01_files/check_input_01_6_6.png)



![png](check_input_01_files/check_input_01_6_7.png)



![png](check_input_01_files/check_input_01_6_8.png)



![png](check_input_01_files/check_input_01_6_9.png)



![png](check_input_01_files/check_input_01_6_10.png)



![png](check_input_01_files/check_input_01_6_11.png)



![png](check_input_01_files/check_input_01_6_12.png)



![png](check_input_01_files/check_input_01_6_13.png)



![png](check_input_01_files/check_input_01_6_14.png)



![png](check_input_01_files/check_input_01_6_15.png)



![png](check_input_01_files/check_input_01_6_16.png)



![png](check_input_01_files/check_input_01_6_17.png)



![png](check_input_01_files/check_input_01_6_18.png)



![png](check_input_01_files/check_input_01_6_19.png)



![png](check_input_01_files/check_input_01_6_20.png)



![png](check_input_01_files/check_input_01_6_21.png)



![png](check_input_01_files/check_input_01_6_22.png)



![png](check_input_01_files/check_input_01_6_23.png)



![png](check_input_01_files/check_input_01_6_24.png)



![png](check_input_01_files/check_input_01_6_25.png)



![png](check_input_01_files/check_input_01_6_26.png)



![png](check_input_01_files/check_input_01_6_27.png)



![png](check_input_01_files/check_input_01_6_28.png)



![png](check_input_01_files/check_input_01_6_29.png)



![png](check_input_01_files/check_input_01_6_30.png)



![png](check_input_01_files/check_input_01_6_31.png)



![png](check_input_01_files/check_input_01_6_32.png)



![png](check_input_01_files/check_input_01_6_33.png)



![png](check_input_01_files/check_input_01_6_34.png)



![png](check_input_01_files/check_input_01_6_35.png)



![png](check_input_01_files/check_input_01_6_36.png)



![png](check_input_01_files/check_input_01_6_37.png)



![png](check_input_01_files/check_input_01_6_38.png)



![png](check_input_01_files/check_input_01_6_39.png)



![png](check_input_01_files/check_input_01_6_40.png)



![png](check_input_01_files/check_input_01_6_41.png)



![png](check_input_01_files/check_input_01_6_42.png)



![png](check_input_01_files/check_input_01_6_43.png)



![png](check_input_01_files/check_input_01_6_44.png)



![png](check_input_01_files/check_input_01_6_45.png)



![png](check_input_01_files/check_input_01_6_46.png)



![png](check_input_01_files/check_input_01_6_47.png)



![png](check_input_01_files/check_input_01_6_48.png)



![png](check_input_01_files/check_input_01_6_49.png)



![png](check_input_01_files/check_input_01_6_50.png)



![png](check_input_01_files/check_input_01_6_51.png)



![png](check_input_01_files/check_input_01_6_52.png)



![png](check_input_01_files/check_input_01_6_53.png)



![png](check_input_01_files/check_input_01_6_54.png)



![png](check_input_01_files/check_input_01_6_55.png)



![png](check_input_01_files/check_input_01_6_56.png)



![png](check_input_01_files/check_input_01_6_57.png)



![png](check_input_01_files/check_input_01_6_58.png)



![png](check_input_01_files/check_input_01_6_59.png)



![png](check_input_01_files/check_input_01_6_60.png)



![png](check_input_01_files/check_input_01_6_61.png)



![png](check_input_01_files/check_input_01_6_62.png)



![png](check_input_01_files/check_input_01_6_63.png)



![png](check_input_01_files/check_input_01_6_64.png)



![png](check_input_01_files/check_input_01_6_65.png)



![png](check_input_01_files/check_input_01_6_66.png)



![png](check_input_01_files/check_input_01_6_67.png)



![png](check_input_01_files/check_input_01_6_68.png)



![png](check_input_01_files/check_input_01_6_69.png)



![png](check_input_01_files/check_input_01_6_70.png)



![png](check_input_01_files/check_input_01_6_71.png)



![png](check_input_01_files/check_input_01_6_72.png)



![png](check_input_01_files/check_input_01_6_73.png)



![png](check_input_01_files/check_input_01_6_74.png)



![png](check_input_01_files/check_input_01_6_75.png)



![png](check_input_01_files/check_input_01_6_76.png)



![png](check_input_01_files/check_input_01_6_77.png)



![png](check_input_01_files/check_input_01_6_78.png)



![png](check_input_01_files/check_input_01_6_79.png)



![png](check_input_01_files/check_input_01_6_80.png)



![png](check_input_01_files/check_input_01_6_81.png)



![png](check_input_01_files/check_input_01_6_82.png)



![png](check_input_01_files/check_input_01_6_83.png)



![png](check_input_01_files/check_input_01_6_84.png)



![png](check_input_01_files/check_input_01_6_85.png)



![png](check_input_01_files/check_input_01_6_86.png)



![png](check_input_01_files/check_input_01_6_87.png)



![png](check_input_01_files/check_input_01_6_88.png)



![png](check_input_01_files/check_input_01_6_89.png)



![png](check_input_01_files/check_input_01_6_90.png)



![png](check_input_01_files/check_input_01_6_91.png)



![png](check_input_01_files/check_input_01_6_92.png)



![png](check_input_01_files/check_input_01_6_93.png)



![png](check_input_01_files/check_input_01_6_94.png)



![png](check_input_01_files/check_input_01_6_95.png)



![png](check_input_01_files/check_input_01_6_96.png)



![png](check_input_01_files/check_input_01_6_97.png)



![png](check_input_01_files/check_input_01_6_98.png)



![png](check_input_01_files/check_input_01_6_99.png)



![png](check_input_01_files/check_input_01_6_100.png)



![png](check_input_01_files/check_input_01_6_101.png)



![png](check_input_01_files/check_input_01_6_102.png)



![png](check_input_01_files/check_input_01_6_103.png)



![png](check_input_01_files/check_input_01_6_104.png)



![png](check_input_01_files/check_input_01_6_105.png)



![png](check_input_01_files/check_input_01_6_106.png)



![png](check_input_01_files/check_input_01_6_107.png)



![png](check_input_01_files/check_input_01_6_108.png)



![png](check_input_01_files/check_input_01_6_109.png)



![png](check_input_01_files/check_input_01_6_110.png)



![png](check_input_01_files/check_input_01_6_111.png)



![png](check_input_01_files/check_input_01_6_112.png)



![png](check_input_01_files/check_input_01_6_113.png)



![png](check_input_01_files/check_input_01_6_114.png)



![png](check_input_01_files/check_input_01_6_115.png)



![png](check_input_01_files/check_input_01_6_116.png)



![png](check_input_01_files/check_input_01_6_117.png)



![png](check_input_01_files/check_input_01_6_118.png)



![png](check_input_01_files/check_input_01_6_119.png)



![png](check_input_01_files/check_input_01_6_120.png)



![png](check_input_01_files/check_input_01_6_121.png)



![png](check_input_01_files/check_input_01_6_122.png)



![png](check_input_01_files/check_input_01_6_123.png)



![png](check_input_01_files/check_input_01_6_124.png)



![png](check_input_01_files/check_input_01_6_125.png)



![png](check_input_01_files/check_input_01_6_126.png)



![png](check_input_01_files/check_input_01_6_127.png)



![png](check_input_01_files/check_input_01_6_128.png)



![png](check_input_01_files/check_input_01_6_129.png)



![png](check_input_01_files/check_input_01_6_130.png)



![png](check_input_01_files/check_input_01_6_131.png)



![png](check_input_01_files/check_input_01_6_132.png)



![png](check_input_01_files/check_input_01_6_133.png)



![png](check_input_01_files/check_input_01_6_134.png)



![png](check_input_01_files/check_input_01_6_135.png)



![png](check_input_01_files/check_input_01_6_136.png)



![png](check_input_01_files/check_input_01_6_137.png)



![png](check_input_01_files/check_input_01_6_138.png)



![png](check_input_01_files/check_input_01_6_139.png)



![png](check_input_01_files/check_input_01_6_140.png)



![png](check_input_01_files/check_input_01_6_141.png)



![png](check_input_01_files/check_input_01_6_142.png)



![png](check_input_01_files/check_input_01_6_143.png)



![png](check_input_01_files/check_input_01_6_144.png)



![png](check_input_01_files/check_input_01_6_145.png)



![png](check_input_01_files/check_input_01_6_146.png)



![png](check_input_01_files/check_input_01_6_147.png)



![png](check_input_01_files/check_input_01_6_148.png)



![png](check_input_01_files/check_input_01_6_149.png)



![png](check_input_01_files/check_input_01_6_150.png)



![png](check_input_01_files/check_input_01_6_151.png)



![png](check_input_01_files/check_input_01_6_152.png)



![png](check_input_01_files/check_input_01_6_153.png)



![png](check_input_01_files/check_input_01_6_154.png)



![png](check_input_01_files/check_input_01_6_155.png)



![png](check_input_01_files/check_input_01_6_156.png)



![png](check_input_01_files/check_input_01_6_157.png)



![png](check_input_01_files/check_input_01_6_158.png)



![png](check_input_01_files/check_input_01_6_159.png)



![png](check_input_01_files/check_input_01_6_160.png)



![png](check_input_01_files/check_input_01_6_161.png)



![png](check_input_01_files/check_input_01_6_162.png)



![png](check_input_01_files/check_input_01_6_163.png)



![png](check_input_01_files/check_input_01_6_164.png)



![png](check_input_01_files/check_input_01_6_165.png)



![png](check_input_01_files/check_input_01_6_166.png)



![png](check_input_01_files/check_input_01_6_167.png)



![png](check_input_01_files/check_input_01_6_168.png)



![png](check_input_01_files/check_input_01_6_169.png)



![png](check_input_01_files/check_input_01_6_170.png)



![png](check_input_01_files/check_input_01_6_171.png)



![png](check_input_01_files/check_input_01_6_172.png)



![png](check_input_01_files/check_input_01_6_173.png)



![png](check_input_01_files/check_input_01_6_174.png)



![png](check_input_01_files/check_input_01_6_175.png)



![png](check_input_01_files/check_input_01_6_176.png)



![png](check_input_01_files/check_input_01_6_177.png)



![png](check_input_01_files/check_input_01_6_178.png)



![png](check_input_01_files/check_input_01_6_179.png)



![png](check_input_01_files/check_input_01_6_180.png)



![png](check_input_01_files/check_input_01_6_181.png)



![png](check_input_01_files/check_input_01_6_182.png)



![png](check_input_01_files/check_input_01_6_183.png)



![png](check_input_01_files/check_input_01_6_184.png)



![png](check_input_01_files/check_input_01_6_185.png)



```python
xa = xr.open_dataset(file_path).isel(Time=0)
list(xa.dims)



```




    ['DIM0010',
     'bottom_top',
     'bottom_top_stag',
     'dust_erosion_dimension',
     'land_cat_stag',
     'num_ext_model_couple_dom_stag',
     'soil_cat_stag',
     'soil_layers_stag',
     'south_north',
     'south_north_stag',
     'west_east',
     'west_east_stag']




```python
variables = list(xa.variables)
```


```python
for v in variables:
    ll = len(xa[v].dims)
    if ll==2:
        try: desc=xa[v].description
        except: desc=''
        fig, ax = plt.subplots()
        xa[v].plot()
        ax.set_title(desc)
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/matplotlib/pyplot.py:514: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      max_open_warning, RuntimeWarning)



![png](check_input_01_files/check_input_01_9_1.png)



![png](check_input_01_files/check_input_01_9_2.png)



![png](check_input_01_files/check_input_01_9_3.png)



![png](check_input_01_files/check_input_01_9_4.png)



![png](check_input_01_files/check_input_01_9_5.png)



![png](check_input_01_files/check_input_01_9_6.png)



![png](check_input_01_files/check_input_01_9_7.png)



![png](check_input_01_files/check_input_01_9_8.png)



![png](check_input_01_files/check_input_01_9_9.png)



![png](check_input_01_files/check_input_01_9_10.png)



![png](check_input_01_files/check_input_01_9_11.png)



![png](check_input_01_files/check_input_01_9_12.png)



![png](check_input_01_files/check_input_01_9_13.png)



![png](check_input_01_files/check_input_01_9_14.png)



![png](check_input_01_files/check_input_01_9_15.png)



![png](check_input_01_files/check_input_01_9_16.png)



![png](check_input_01_files/check_input_01_9_17.png)



![png](check_input_01_files/check_input_01_9_18.png)



![png](check_input_01_files/check_input_01_9_19.png)



![png](check_input_01_files/check_input_01_9_20.png)



![png](check_input_01_files/check_input_01_9_21.png)



![png](check_input_01_files/check_input_01_9_22.png)



![png](check_input_01_files/check_input_01_9_23.png)



![png](check_input_01_files/check_input_01_9_24.png)



![png](check_input_01_files/check_input_01_9_25.png)



![png](check_input_01_files/check_input_01_9_26.png)



![png](check_input_01_files/check_input_01_9_27.png)



![png](check_input_01_files/check_input_01_9_28.png)



![png](check_input_01_files/check_input_01_9_29.png)



![png](check_input_01_files/check_input_01_9_30.png)



![png](check_input_01_files/check_input_01_9_31.png)



![png](check_input_01_files/check_input_01_9_32.png)



![png](check_input_01_files/check_input_01_9_33.png)



![png](check_input_01_files/check_input_01_9_34.png)



![png](check_input_01_files/check_input_01_9_35.png)



![png](check_input_01_files/check_input_01_9_36.png)



![png](check_input_01_files/check_input_01_9_37.png)



![png](check_input_01_files/check_input_01_9_38.png)



![png](check_input_01_files/check_input_01_9_39.png)



![png](check_input_01_files/check_input_01_9_40.png)



![png](check_input_01_files/check_input_01_9_41.png)



![png](check_input_01_files/check_input_01_9_42.png)



![png](check_input_01_files/check_input_01_9_43.png)



![png](check_input_01_files/check_input_01_9_44.png)



![png](check_input_01_files/check_input_01_9_45.png)



![png](check_input_01_files/check_input_01_9_46.png)



![png](check_input_01_files/check_input_01_9_47.png)



![png](check_input_01_files/check_input_01_9_48.png)



![png](check_input_01_files/check_input_01_9_49.png)



![png](check_input_01_files/check_input_01_9_50.png)



![png](check_input_01_files/check_input_01_9_51.png)



![png](check_input_01_files/check_input_01_9_52.png)



![png](check_input_01_files/check_input_01_9_53.png)



![png](check_input_01_files/check_input_01_9_54.png)



![png](check_input_01_files/check_input_01_9_55.png)



![png](check_input_01_files/check_input_01_9_56.png)



![png](check_input_01_files/check_input_01_9_57.png)



![png](check_input_01_files/check_input_01_9_58.png)



![png](check_input_01_files/check_input_01_9_59.png)



![png](check_input_01_files/check_input_01_9_60.png)



![png](check_input_01_files/check_input_01_9_61.png)



![png](check_input_01_files/check_input_01_9_62.png)



![png](check_input_01_files/check_input_01_9_63.png)



![png](check_input_01_files/check_input_01_9_64.png)



![png](check_input_01_files/check_input_01_9_65.png)



![png](check_input_01_files/check_input_01_9_66.png)



![png](check_input_01_files/check_input_01_9_67.png)



![png](check_input_01_files/check_input_01_9_68.png)



![png](check_input_01_files/check_input_01_9_69.png)



![png](check_input_01_files/check_input_01_9_70.png)



```python
for v in variables:
    ll = len(xa[v].dims)
    if ll==1:
        try: desc=xa[v].description
        except: desc=''
        fig, ax = plt.subplots()
        xa[v].plot()
        ax.set_title(desc)
```


![png](check_input_01_files/check_input_01_10_0.png)



![png](check_input_01_files/check_input_01_10_1.png)



![png](check_input_01_files/check_input_01_10_2.png)



![png](check_input_01_files/check_input_01_10_3.png)



![png](check_input_01_files/check_input_01_10_4.png)



![png](check_input_01_files/check_input_01_10_5.png)



![png](check_input_01_files/check_input_01_10_6.png)



![png](check_input_01_files/check_input_01_10_7.png)



![png](check_input_01_files/check_input_01_10_8.png)



![png](check_input_01_files/check_input_01_10_9.png)



![png](check_input_01_files/check_input_01_10_10.png)



![png](check_input_01_files/check_input_01_10_11.png)



![png](check_input_01_files/check_input_01_10_12.png)



![png](check_input_01_files/check_input_01_10_13.png)



![png](check_input_01_files/check_input_01_10_14.png)



![png](check_input_01_files/check_input_01_10_15.png)



![png](check_input_01_files/check_input_01_10_16.png)



![png](check_input_01_files/check_input_01_10_17.png)



![png](check_input_01_files/check_input_01_10_18.png)



![png](check_input_01_files/check_input_01_10_19.png)



![png](check_input_01_files/check_input_01_10_20.png)



![png](check_input_01_files/check_input_01_10_21.png)



![png](check_input_01_files/check_input_01_10_22.png)



![png](check_input_01_files/check_input_01_10_23.png)



![png](check_input_01_files/check_input_01_10_24.png)



```python
for v in variables:
    ll = len(xa[v].dims)
    if ll==3:
        try: desc = xa[v].description
        except: desc = ''
        dat = xa[v]
        dims = xa[v].dims
        lens = [len(dat[d]) for d in dims]
        dl = pd.DataFrame(lens,dims,['l'])
        id_min = dl.idxmin()[0]
        val_min = dl.loc[id_min][0]
        if val_min ==1:
            fig,ax = plt.subplots()
            dat.plot()
            fig.suptitle(desc,y=1.1)
            
        else:
            if val_min <=6:
                sp = 1
            else:
                sp = int(np.ceil(val_min/6))
            dat = dat.isel(**{id_min:slice(0,None,sp)})
            res = dat.plot(col=id_min,col_wrap=3)
            res.fig.suptitle(desc,y=1.1)
       
        
        
        

```


![png](check_input_01_files/check_input_01_11_0.png)



![png](check_input_01_files/check_input_01_11_1.png)



![png](check_input_01_files/check_input_01_11_2.png)



![png](check_input_01_files/check_input_01_11_3.png)



![png](check_input_01_files/check_input_01_11_4.png)



![png](check_input_01_files/check_input_01_11_5.png)



![png](check_input_01_files/check_input_01_11_6.png)



![png](check_input_01_files/check_input_01_11_7.png)



![png](check_input_01_files/check_input_01_11_8.png)



![png](check_input_01_files/check_input_01_11_9.png)



![png](check_input_01_files/check_input_01_11_10.png)



![png](check_input_01_files/check_input_01_11_11.png)



![png](check_input_01_files/check_input_01_11_12.png)



![png](check_input_01_files/check_input_01_11_13.png)



![png](check_input_01_files/check_input_01_11_14.png)



![png](check_input_01_files/check_input_01_11_15.png)



![png](check_input_01_files/check_input_01_11_16.png)



![png](check_input_01_files/check_input_01_11_17.png)



![png](check_input_01_files/check_input_01_11_18.png)



![png](check_input_01_files/check_input_01_11_19.png)



![png](check_input_01_files/check_input_01_11_20.png)



![png](check_input_01_files/check_input_01_11_21.png)



![png](check_input_01_files/check_input_01_11_22.png)



![png](check_input_01_files/check_input_01_11_23.png)



![png](check_input_01_files/check_input_01_11_24.png)



![png](check_input_01_files/check_input_01_11_25.png)



```python

```
