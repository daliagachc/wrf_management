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
import subprocess

# %%
pr = subprocess.run(["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)

# %%
pr = subprocess.run(["sleep", "5"], stdout=subprocess.PIPE)

# %%
from subprocess import Popen, PIPE
process = Popen(['sleep', '20',';','echo','"hola"'], stdout=PIPE, stderr=PIPE)


# %%
import wrf_management.project_global_constants as gc
import wrf_management.utilities as ut
import wrf_management.run_utilities as ru
import importlib
rl = [gc,ut,ru]
for m in rl: importlib.reload(m)

# %%
rdp = ut.get_run_data_path()

# %%
import glob
import pandas as pd
paths = glob.glob(rdp+'/20*')
df = pd.DataFrame(paths,columns=['paths'])
df

# %%

# %%

# %%
stdout, stderr

# %%
process.communicate('echo')

# %%
