```python
import rpy2
print(rpy2.__version__)
```

    3.0.4



```python
import rpy2.robjects as robjects
```


```python
from rpy2.robjects.packages import importr
# import R's "base" package
base = importr('base')

# import R's "utils" package
utils = importr('utils')
```


```python
# import rpy2's package module
import rpy2.robjects.packages as rpackages

# import R's utility package
utils = rpackages.importr('utils')

# select a mirror for R packages
utils.chooseCRANmirror(ind=1) # select the first mirror in the list
```




    <rpy2.rinterface.NULLType object at 0x11e0e1708> [RTYPES.NILSXP]




```python
rpackages.isinstalled('factoextra')
```




    True




```python
# R package names
packnames = ('NbClust','factoextra')

# R vector of strings
from rpy2.robjects.vectors import StrVector

# Selectively install what needs to be install.
# We are fancy, just because we can.
names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    utils.install_packages(StrVector(names_to_install))
```


```python
nbc = rpackages.importr('NbClust')
```


```python
fac = rpackages.importr('factoextra')
```


```python
nbc.NbClust(data=1)
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/rpy2/rinterface/__init__.py:146: RRuntimeWarning: Error in (function (data = NULL, diss = NULL, distance = "euclidean",  : 
      method is NULL
    
      warnings.warn(x, RRuntimeWarning)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/rpy2/rinterface/__init__.py:146: RRuntimeWarning: In addition: 
      warnings.warn(x, RRuntimeWarning)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/rpy2/rinterface/__init__.py:146: RRuntimeWarning: There were 25 warnings (use warnings() to see them)
      warnings.warn(x, RRuntimeWarning)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/rpy2/rinterface/__init__.py:146: RRuntimeWarning: 
    
      warnings.warn(x, RRuntimeWarning)



    ---------------------------------------------------------------------------

    RRuntimeError                             Traceback (most recent call last)

    <ipython-input-8-4801b389dd45> in <module>
    ----> 1 nbc.NbClust(data=1)
    

    ~/miniconda3/envs/b36/lib/python3.6/site-packages/rpy2/robjects/functions.py in __call__(self, *args, **kwargs)
        176                 v = kwargs.pop(k)
        177                 kwargs[r_k] = v
    --> 178         return super(SignatureTranslatedFunction, self).__call__(*args, **kwargs)
        179 
        180 pattern_link = re.compile(r'\\link\{(.+?)\}')


    ~/miniconda3/envs/b36/lib/python3.6/site-packages/rpy2/robjects/functions.py in __call__(self, *args, **kwargs)
        104         for k, v in kwargs.items():
        105             new_kwargs[k] = conversion.py2ri(v)
    --> 106         res = super(Function, self).__call__(*new_args, **new_kwargs)
        107         res = conversion.ri2ro(res)
        108         return res


    RRuntimeError: Error in (function (data = NULL, diss = NULL, distance = "euclidean",  : 
      method is NULL




```python

```
