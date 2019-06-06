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

# %%
path = '/Volumes/mbProD/Downloads/rich_rwf/wrfout_d04_2017-12-09_19:00:00'

# %%
ds = xr.open_dataset(path)

# %%
sns.distplot(ds.U.values.flatten())

# %%
ds.U.isel(Time=3, west_east_stag=140,south_north=142).plot()

# %%
ds.T.where(ds.T.round(2)==round((296.85269165-290.),2)).to_series().dropna()

# %%
(ds.T.isel(Time=0,west_east=140,south_north=142)).plot()

# %%
tt = [
  2.9685269165E+02,  2.9677893066E+02,  2.9694500732E+02,  2.9670242310E+02,
  2.9633966064E+02,  2.9585580444E+02,  2.9525155640E+02,  2.9445236206E+02,
  2.9320932007E+02,  2.9156552124E+02,  2.8960998535E+02,  2.8731533813E+02,
  2.8555630493E+02,  2.8376669312E+02,  2.8181393433E+02,  2.7947006226E+02,
  2.7667947388E+02,  2.7352664185E+02,  2.7081872559E+02,  2.6802398682E+02,
  2.6524786377E+02,  2.6233285522E+02,  2.5896276855E+02,  2.5624670410E+02,
  2.5263270569E+02,  2.4857107544E+02,  2.4429113770E+02,  2.4009616089E+02,
  2.3613082886E+02,  2.3166197205E+02,  2.2710699463E+02,  2.2387869263E+02,
  2.2014776611E+02,  2.1334902954E+02,  2.0691580200E+02,  2.0321623230E+02,
  1.9999977112E+02,  1.9697372437E+02,  1.9478965759E+02,  1.9309629822E+02,
  1.9145060730E+02,  1.8914906311E+02,  1.9203544617E+02,  1.9389584351E+02,
  1.9714886475E+02,  1.9736492920E+02,  1.9824922180E+02,  2.0023616028E+02,
  2.0192065430E+02,  2.0342620850E+02,
]
plt.plot(tt)

# %%
pp = [
  8.9664539062E+04,  8.9756578125E+04,  8.9159242188E+04,  8.8402781250E+04,
  8.7462914062E+04,  8.6294953125E+04,  8.4868195312E+04,  8.3146914062E+04,
  8.1108414062E+04,  7.8738031250E+04,  7.6041445312E+04,  7.3045132812E+04,
  6.9792257812E+04,  6.6338148438E+04,  6.2738914062E+04,  5.9022742188E+04,
  5.5358738281E+04,  5.1906929688E+04,  4.8648578125E+04,  4.5567558594E+04,
  4.2652714844E+04,  3.9893667969E+04,  3.7281976562E+04,  3.4805468750E+04,
  3.2460773438E+04,  3.0240398438E+04,  2.8138074219E+04,  2.6157736328E+04,
  2.4301029297E+04,  2.2562312500E+04,  2.0939951172E+04,  1.9452503906E+04,
  1.8099107422E+04,  1.6840470703E+04,  1.5651799805E+04,  1.4538021484E+04,
  1.3501234375E+04,  1.2538455078E+04,  1.1647401367E+04,  1.0822774414E+04,
  1.0056514648E+04,  9.3434257812E+03,  8.6812402344E+03,  8.0667509766E+03,
  7.4954741211E+03,  6.9642075195E+03,  6.4706459961E+03,  6.0124985352E+03,
  5.5866577148E+03,  5.1905786133E+03,
]
ax=plt.plot(tt)
plt.gca().set_ylim(0,90000)

# %%
import wrf

# %%
from netCDF4 import Dataset
from wrf import getvar

ncfile = Dataset(path)

# %%
wrf.getvar(ncfile,'tk',timeidx=1).isel(west_east=140,south_north=142).plot()

# %%
wrf.getvar(ncfile,'ua',timeidx=1).isel(west_east=140,south_north=142).plot()

# %%
ds.CLDFRA

# %%
ds.PBLH.plot()

# %%