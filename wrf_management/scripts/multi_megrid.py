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
res = su.Popen(['python','-u','metgrid.py'], stdout=su.PIPE, stderr=su.PIPE)

# %%
res.communicate(timeout=1)

# %%
pu = su.run(['squeue', '-u', 'aliagadi', '-l'],stdout=su.PIPE, stderr=su.PIPE)
pu.stdout

# %%
