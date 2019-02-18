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
import wrf_management.base_namelists.base_namelists as nl
import importlib
importlib.reload(nl);

# %%
res,df,df_full = nl.sanity_check(path_wps='./namelist.wps',path_wrf='./namelist.input')
print(res)
df

# %%
df_full

# %%

