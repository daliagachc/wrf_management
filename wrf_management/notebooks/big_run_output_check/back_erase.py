# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *
import wrf 
from netCDF4 import Dataset
from sklearn.cluster import KMeans

# %%
path = '/Volumes/mbProD/Downloads/wrf_out_sample/wrfout_d04*'

# %%
files = glob.glob(path)
files.sort()
ncs = [Dataset(f) for f in files]

# %%
tc = wrf.getvar(ncs,'tc',timeidx=wrf.ALL_TIMES, method="cat")

# %%
z = wrf.getvar(ncs,'z',timeidx=wrf.ALL_TIMES, method="cat")

# %%
tc['height']=z

# %%
tc_t = tc1 = tc.to_series()
tc1 = tc1.unstack(level='Time')

# %%
tc

# %%
kmeans = KMeans(n_clusters=6, random_state=0).fit(tc1)

# %%
tc1['lab']=kmeans.labels_

# %%
lab_da = tc1['lab'].to_xarray()

# %%
labs = tc1['lab'].unique()
labs.sort()
labs
i = labs[5]

# %%
labs

# %%
ti = tc.where(lab_da==i)

# %%
ts = tc.to_dataset()

# %%
ts['b_t']=ts.bottom_top

# %%
tic=ti.count(dim=['Time','south_north','west_east'])

# %%
(ts.b_t * tic).sum()/tic.sum()

# %%
plt.subplots()
ti.count(dim=['Time','bottom_top']).plot(x='XLONG',y='XLAT')
plt.subplots()
tii = ti.count(dim=['Time','west_east'])
tii = tii.assign_coords(heights=ti.height.mean(dim=['Time','west_east']))
tii = tii.assign_coords(XLAT=ti.XLAT.mean(dim=['west_east']))
tii.plot(x='XLAT',y='heights')
plt.subplots()
dimx = 'south_north'
tii = ti.count(dim=['Time',dimx])
tii = tii.assign_coords(heights=ti.height.mean(dim=['Time',dimx]))
tii = tii.assign_coords(XLONG=ti.XLONG.mean(dim=[dimx]))
tii.plot(x='XLONG',y='heights')
plt.subplots()
ti.median(dim=['bottom_top','south_north','west_east']).plot()

# %%
sns.choose_colorbrewer_palette('s')

# %%
tii

# %%
ti.count(dim=['Time','west_east'])

# %%
ti.height.mean(dim=['Time','west_east'])

# %%
r,c = tc1.shape

# %%
print(r,c)

# %%

# %%
import rpy2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages

# %%
rnc = rpackages.importr('NbClust')

# %%
ii=10000
m = robjects.r.matrix(
    robjects.FloatVector(tc1[:ii*c].values.flatten()),
    nrow=ii*c
)

# %%
res = rnc.NbClust(m,distance = "euclidean",
         method ='kmeans',**{'min.nc':2,'max.nc':3},
           index="silhouette")

# %%
res

# %%
a

# %%
print(res)

# %%
