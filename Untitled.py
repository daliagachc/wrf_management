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
path = './du.log'

# %%
import pandas as pd
df = pd.read_csv(path,
                names=['mem','path'],
                 sep='\t'
                )
import numpy as np

df['mem']=np.round(df['mem']/1000000)
df.sort_values('mem',ascending=False)

# %%
