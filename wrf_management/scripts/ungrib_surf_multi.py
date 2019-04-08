# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.0.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import subprocess as su 

# %%
ress = {}
ii=0

# %%
import time 
for i in range(13):
    time.sleep(1)
    res = su.Popen(['python','-u','ungrib_surf.py'], stdout=su.PIPE, stderr=su.PIPE)
    ress[ii]=res
    ii=ii+1

# %%
res.communicate(timeout=1)

# %%
pu = su.run(['squeue', '-u', 'aliagadi'],stdout=su.PIPE, stderr=su.PIPE)
pu.stdout

# %%
