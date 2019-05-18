#!/usr/bin/python     

from netCDF4 import Dataset
import numpy as np

# Script modifies wrf input files correcting Lake Titicaca surface water temperature
# It assumes to have Lake temperature txt file and wrf input files in the same folder
# SCRIPT DOES NOT CREATE NEW FILES, IT MODIFIES ORIGINAL ONES

wrflowinp_d01='wrflowinp_d01'
wrflowinp_d02='wrflowinp_d02'
wrflowinp_d03='wrflowinp_d03'
wrflowinp_d04='wrflowinp_d04'

wrfinput_d01='wrfinput_d01'
wrfinput_d02='wrfinput_d02'
wrfinput_d03='wrfinput_d03'
wrfinput_d04='wrfinput_d04'

print('reading lake temperatures')

# Could be done with fancier LakeTemp.txt that includes dates
f=open("LakeTemp_no_date.txt", "r")
lines = f.readlines()
LakeTemp = []
for i in range(len(lines)):
    LakeTemp.append(float(lines[i]))
f.close()

print('modifiying d01')

data_wrflowinp_d01 = Dataset(wrflowinp_d01, 'r+')
data_wrfinput_d01 = Dataset(wrfinput_d01, 'r+')

MASK_d01 = data_wrfinput_d01.variables['LANDMASK'][:]
SST_d01 = data_wrflowinp_d01.variables['SST'][:]
SEAICE_d01 = data_wrflowinp_d01.variables['SEAICE'][:]
SST_init_d01 = data_wrfinput_d01.variables['SST'][:]
TSK_init_d01 = data_wrfinput_d01.variables['TSK'][:]

day =  data_wrfinput_d01.JULDAY

# Creating Lake Titicaca mask
MASK_LAKE_d01 = np.zeros_like(MASK_d01)
for i in range(7):
    for j in range(7):
        MASK_LAKE_d01[0][42+i][47+j] = 1-MASK_d01[0][42+i][47+j]
		
# Modifying temperatures
SST_init_d01_new = SST_init_d01*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1]+273.15)
TSK_init_d01_new = TSK_init_d01*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1]+273.15)
SST_d01_new = np.zeros_like(SST_d01)
SEAICE_d01_new = np.zeros_like(SEAICE_d01)
# (didn't bother to do it properly, my bad) 
for k in range(181):
    SST_d01_new[4*k+0] = SST_d01[4*k+0]*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1+k]+273.15)
    SST_d01_new[4*k+1] = SST_d01[4*k+1]*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1+k]+273.15)
    SST_d01_new[4*k+2] = SST_d01[4*k+2]*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1+k]+273.15)
    SST_d01_new[4*k+3] = SST_d01[4*k+3]*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1+k]+273.15)
SST_d01_new[724] = SST_d01[724]*(1-MASK_LAKE_d01)+MASK_LAKE_d01*(LakeTemp[day-1+181]+273.15)
SEAICE_d01_new = SEAICE_d01*(1-MASK_LAKE_d01)

# Writing modified fields back
data_wrflowinp_d01.variables['SST'][:] = SST_d01_new
data_wrflowinp_d01.variables['SEAICE'][:] = SEAICE_d01_new
data_wrflowinp_d01.close()
data_wrfinput_d01.variables['SST'][:] = SST_init_d01_new
data_wrfinput_d01.variables['TSK'][:] = TSK_init_d01_new
data_wrfinput_d01.close()

print('modifiying d02')

data_wrflowinp_d02 = Dataset(wrflowinp_d02, 'r+')
data_wrfinput_d02 = Dataset(wrfinput_d02, 'r+')

MASK_d02 = data_wrfinput_d02.variables['LANDMASK'][:]
SST_d02 = data_wrflowinp_d02.variables['SST'][:]
SEAICE_d02 = data_wrflowinp_d02.variables['SEAICE'][:]
SST_init_d02 = data_wrfinput_d02.variables['SST'][:]
TSK_init_d02 = data_wrfinput_d02.variables['TSK'][:]

day =  data_wrfinput_d02.JULDAY

# Creating Lake Titicaca mask
MASK_LAKE_d02 = np.zeros_like(MASK_d02)
for i in range(16):
    for j in range(19):
        MASK_LAKE_d02[0][105+i][86+j] = 1-MASK_d02[0][105+i][86+j]  
		
# Modifying temperatures
SST_init_d02_new = SST_init_d02*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1]+273.15)
TSK_init_d02_new = TSK_init_d02*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1]+273.15)
SST_d02_new = np.zeros_like(SST_d02)
SEAICE_d02_new = np.zeros_like(SEAICE_d02)
# (didn't bother to do it properly, my bad) 
for k in range(181):
    SST_d02_new[4*k+0] = SST_d02[4*k+0]*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1+k]+273.15)
    SST_d02_new[4*k+1] = SST_d02[4*k+1]*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1+k]+273.15)
    SST_d02_new[4*k+2] = SST_d02[4*k+2]*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1+k]+273.15)
    SST_d02_new[4*k+3] = SST_d02[4*k+3]*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1+k]+273.15)
SST_d02_new[724] = SST_d02[724]*(1-MASK_LAKE_d02)+MASK_LAKE_d02*(LakeTemp[day-1+181]+273.15)
SEAICE_d02_new = SEAICE_d02*(1-MASK_LAKE_d02)

# Writing modified fields back
data_wrflowinp_d02.variables['SST'][:] = SST_d02_new
data_wrflowinp_d02.variables['SEAICE'][:] = SEAICE_d02_new
data_wrflowinp_d02.close()
data_wrfinput_d02.variables['SST'][:] = SST_init_d02_new
data_wrfinput_d02.variables['TSK'][:] = TSK_init_d02_new
data_wrfinput_d02.close()

print('modifiying d03')

data_wrflowinp_d03 = Dataset(wrflowinp_d03, 'r+')
data_wrfinput_d03 = Dataset(wrfinput_d03, 'r+')

MASK_d03 = data_wrfinput_d03.variables['LANDMASK'][:]
SST_d03 = data_wrflowinp_d03.variables['SST'][:]
SEAICE_d03 = data_wrflowinp_d03.variables['SEAICE'][:]
SST_init_d03 = data_wrfinput_d03.variables['SST'][:]
TSK_init_d03 = data_wrfinput_d03.variables['TSK'][:]

day =  data_wrfinput_d03.JULDAY

# Creating Lake Titicaca mask
MASK_LAKE_d03 = np.zeros_like(MASK_d03)
for i in range(44):
    for j in range(49):
        MASK_LAKE_d03[0][126+i][25+j] = 1-MASK_d03[0][126+i][25+j]
		
# Modifying temperatures
SST_init_d03_new = SST_init_d03*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1]+273.15)
TSK_init_d03_new = TSK_init_d03*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1]+273.15)
SST_d03_new = np.zeros_like(SST_d03)
SEAICE_d03_new = np.zeros_like(SEAICE_d03)
# (didn't bother to do it properly, my bad) 
for k in range(181):
    SST_d03_new[4*k+0] = SST_d03[4*k+0]*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1+k]+273.15)
    SST_d03_new[4*k+1] = SST_d03[4*k+1]*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1+k]+273.15)
    SST_d03_new[4*k+2] = SST_d03[4*k+2]*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1+k]+273.15)
    SST_d03_new[4*k+3] = SST_d03[4*k+3]*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1+k]+273.15)
SST_d03_new[724] = SST_d03[724]*(1-MASK_LAKE_d03)+MASK_LAKE_d03*(LakeTemp[day-1+181]+273.15)
SEAICE_d03_new = SEAICE_d03*(1-MASK_LAKE_d03)

# Writing modified fields back
data_wrflowinp_d03.variables['SST'][:] = SST_d03_new
data_wrflowinp_d03.variables['SEAICE'][:] = SEAICE_d03_new
data_wrflowinp_d03.close()
data_wrfinput_d03.variables['SST'][:] = SST_init_d03_new
data_wrfinput_d03.variables['TSK'][:] = TSK_init_d03_new
data_wrfinput_d03.close()

print('modifiying d04')

data_wrflowinp_d04 = Dataset(wrflowinp_d04, 'r+')
data_wrfinput_d04 = Dataset(wrfinput_d04, 'r+')

MASK_d04 = data_wrfinput_d04.variables['LANDMASK'][:]
SST_d04 = data_wrflowinp_d04.variables['SST'][:]
SEAICE_d04 = data_wrflowinp_d04.variables['SEAICE'][:]
SST_init_d04 = data_wrfinput_d04.variables['SST'][:]
TSK_init_d04 = data_wrfinput_d04.variables['TSK'][:]

day =  data_wrfinput_d04.JULDAY

# Creating Lake Titicaca mask
MASK_LAKE_d04 = np.zeros_like(MASK_d04)
for i in range(83):
    for j in range(38):
        MASK_LAKE_d04[0][39+i][0+j] = 1-MASK_d04[0][39+i][0+j]
		
# Modifying temperatures
SST_init_d04_new = SST_init_d04*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1]+273.15)
TSK_init_d04_new = TSK_init_d04*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1]+273.15)
SST_d04_new = np.zeros_like(SST_d04)
SEAICE_d04_new = np.zeros_like(SEAICE_d04)
# (didn't bother to do it properly, my bad) 
for k in range(181):
    SST_d04_new[4*k+0] = SST_d04[4*k+0]*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1+k]+273.15)
    SST_d04_new[4*k+1] = SST_d04[4*k+1]*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1+k]+273.15)
    SST_d04_new[4*k+2] = SST_d04[4*k+2]*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1+k]+273.15)
    SST_d04_new[4*k+3] = SST_d04[4*k+3]*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1+k]+273.15)
SST_d04_new[724] = SST_d04[724]*(1-MASK_LAKE_d04)+MASK_LAKE_d04*(LakeTemp[day-1+181]+273.15)
SEAICE_d04_new = SEAICE_d04*(1-MASK_LAKE_d04)

# Writing modified fields back
data_wrflowinp_d04.variables['SST'][:] = SST_d04_new
data_wrflowinp_d04.variables['SEAICE'][:] = SEAICE_d04_new
data_wrflowinp_d04.close()
data_wrfinput_d04.variables['SST'][:] = SST_init_d04_new
data_wrfinput_d04.variables['TSK'][:] = TSK_init_d04_new
data_wrfinput_d04.close()
