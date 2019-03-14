# MAFATE : CliMAF Automatic Treatment Extension

A Python package for extending CliMAF application

**Requirements**

`mafate` only requires [`climaf`](http://climaf.readthedocs.org), [`numpy`](http://numpy.org) and [`xarray`](http://xarray.pydata.org).
It can also require [`iris`](https://scitools.org.uk/iris/docs/latest).

**Contents**

* `varexpe.py` : definition of classes Expe and Var
* `utils.py` : main functions
* `dicts.py` : provide some predefined dictionaries of Expe-s and of Var-s
* `examples.py` : simple examples to getting started

**Getting started**

`mafate` allows to :
* easily define a new CliMAF project
* specify a list of experiments and a list of variables
* load\_datas corresponding to the specific lists of experiments and of variables in a dictionary of xarray's objects
* the load\_datas function allows all cdo's operation (with successive steps).

> Define specific CLIMAF projects
```python
from climaf.api import *
from mafate import *
```

> Define a specific dict of experiments and of vars
```python
dictexps = {}
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', ybeg=2000, yend=2014, number=1)))
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', ybeg=2000, yend=2014, number=2)))

dictvars = {}
dictvars.update(dict_var('tas', 'Amon'))
```
> Load data : you can specify a list of cdo operations : list\_cdops
```
datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['zonmean', 'ymonmean'], verbose=True)

ds = datasets['historical']
```
