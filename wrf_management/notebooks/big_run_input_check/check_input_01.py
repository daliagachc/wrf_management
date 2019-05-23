# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *
from check_input_01_funs import * 

# %%
path = '/Volumes/mbProD/Downloads/wrf_small_files'

# %%
glob.glob(path+'/wrf*')

# %%
file_path = os.path.join(path,'wrfinput_d01')

# %%
xa = xr.open_dataset(file_path).isel(Time=0)
list(xa.dims)

# %%
xa.coords

# %%
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
        
        

# %%
xa = xr.open_dataset(file_path).isel(Time=0)
list(xa.dims)




# %%
variables = list(xa.variables)

# %%
for v in variables:
    ll = len(xa[v].dims)
    if ll==2:
        try: desc=xa[v].description
        except: desc=''
        fig, ax = plt.subplots()
        xa[v].plot()
        ax.set_title(desc)

# %%
for v in variables:
    ll = len(xa[v].dims)
    if ll==1:
        try: desc=xa[v].description
        except: desc=''
        fig, ax = plt.subplots()
        xa[v].plot()
        ax.set_title(desc)

# %%
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
       
        
        
        


# %%

