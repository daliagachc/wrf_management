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
d=dict(sdf=4)

# %%
def f(**d): 
    return d

# %%
f(**d)

# %%
l=[[1,2,3]]


# %%
np.ndarray.flatten(np.ndarray(l))

# %%
list(matplotlib.cbook.flatten(l))

# %%
nc = 8 

# %%


# %%


# %%
cols

# %%
fig,axs = plt.subplots(rows,cols,sharey=True,sharex=True,)

# %%
fig.add_subplot(5,4,1)

# %%
sns.choose_colorbrewer_palette('q')

# %%

