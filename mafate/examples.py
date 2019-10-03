from climaf.api import *
from mafate import *
import numpy as np

print('----------------------------------------------------------------------------------------------')

# mafate allows to :
#   (1) define easily a new CliMAF project
#   (2) specify a list of experiments and a list of variables
#   (3) to load datas corresponding to the specific lists of experiments and of variables in a dictionary of xarray's objects
#   The 'load_datas' function allows all cdo's operation (with successive steps).

# -- To define a new CliMAF project by setting :
#   -- a name (string) 
#   -- a data localization : full combination of root_dirs (list) and file_patterns (list)
#   -- with default CliMAF's facets : 'model', 'experiment', 'member', 'realization', 'variable', 'table'

name = 'myDATA'

my_facets = ['experiment', 'variable']

my_root_dirs = []
my_root_dirs.append('./datas')

my_file_patterns = []
my_file_patterns.append('${variable}_${experiment}_YYYY-YYYY.monthly.nc')

define_climaf_project(name, facets=my_facets, root_dirs=my_root_dirs, file_patterns=my_file_patterns)


# -- mafate defines 2 Python's object :
#   -- Expe with main attributes :
#       - project (name of CliMAF project associated)
#       - name
#       - number
#       - ybeg
#       - yend
#       - adds : a dict of additional attributes (e.g. CliMAF facets)
#   -- Variable with attributes :
#       - name
#       - table
#       - grid


# -- To define a dict of Expe-s, use function dict_exp
#   -- return dict_expe[my_expe.expid()] = my_expe

dictexps = {}
dictexps.update(dict_exp(Expe(project='myDATA', model='CNRM-CM6-beta', name='PRE621FRCRef1sw1', ybeg=1979, yend=1980)))


# -- To define a dict of Variable-s, use function dict_var
#   -- return dict_vars[v.name] = v

dictvars = {}
dictvars.update(dict_var('tas', 'Amon'))


# -- Load data with successive operations 'zonmean' and 'yearavg'
datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['zonmean', 'yearavg'], verbose=True)

#print(datasets['PRE621FRCRef1sw1'])
print('----------------------------------------------------------------------------------------------')


# -- If your data follow a kwown CliMAF pattern, 
#       no need to redefine a CliMAF project
#       you only need to specify the path of your data via arguments adds

# -- In the example above, data are organized following CMIP6's pattern and are localized in ./datas/CMIP6/etc

dictexps = {}
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='piClim-control', adds=dict(root='./datas'), ybeg=1850, yend=1851)))
datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['yearavg'], verbose=True)

#print(datasets['piClim-control'])
print('----------------------------------------------------------------------------------------------')


# -- datasets is a python dictionary of xarray's Datasets or iris' objects
#   - datasets[expe.name] contains all the experiments (multi-model, multi-member, multi-variables) corresponding to the experiment expe
#   - by default, the key used in the user's dictexps is : expe.expid() = model'_'+name+'_r'+number

#   NB : CliMAF's project 'multiCMIP5' is among the additional CliMAF's project defined by mafate
#       These additional project can be loaded via function define_climaf_projects()

define_climaf_projects()

dictexps = {}
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', number=1, ybeg=2000, yend=2004)))
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', number=3, ybeg=2000, yend=2004)))
dictexps.update(dict_exp(Expe(project='multiCMIP5', model='CNRM-CM5', name='historical', number=1, ybeg=2000, yend=2004)))

datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['zonmean', 'yearavg'], verbose=True)

print(datasets.keys())
print(datasets['historical'])
print('----------------------------------------------------------------------------------------------')


# -- in this case, if you want to select a Dataset specific to an specific experiment
#       - you could use function extract_from_exp(dict datasets, Expe my_expe)
#       - or you could select directly model and member using xarray's function : sel        
ds = extract_from_exp(datasets, dictexps['CNRM-CM6-1_historical_r3'])
print(ds)
print('----------------------------------------------------------------------------------------------')

ds = datasets['historical'].sel(model='CNRM-CM6-1', member=3)
print(ds)
print('----------------------------------------------------------------------------------------------')


# -- Some pre-defined dictionaries of Variable-s are defined
#   -- dict_vars_NT() : rsdt, rlut, rst, tas
#   -- dict_vars_heatc() : hc2000_HOMOImon, hc700_HOMOImon, heatc_HOMOImon, hcont300_Emon

# -- Some pre-defined dictionaries of Expe-s are defined
#   -- dict_expes_CMIP5_piControl : CMIP-5 piControl experiments
#   -- dict_expes_CMIP5_historical : CMIP-5 historical experiments
#   -- dict_expes_CMIP5_abrupt4xCO2 : CMIP-5 abrupt-4xCO2 experiments
#   -- dict_expes_historical_CNRMCM : CMIP-5 (CNRM-CM5) or CMIP-6 (CNRM-CM6) historical experiments
#       - def dict_expes_historical_CNRMCM(model_name, n_member=10, ybeg=1850, yend=2014, yend_piControl=0):

dictexps = {}
dictexps.update(dict_expes_historical_CNRMCM('CNRM-CM5', n_member=10, ybeg=2005, yend=2005, yend_piControl=2349)) 
dictexps.update(dict_expes_historical_CNRMCM('CNRM-CM6-1', n_member=10, ybeg=2010, yend=2014, yend_piControl=2349))

datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['zonmean', 'yearavg'], verbose=True)
print(datasets['historical'])
print('----------------------------------------------------------------------------------------------')


# -- Example to concatenate historical and historicalExt CMIP5 experiments
import xarray as xr
import numpy as np
n_exps = 2
dictexps = {}
for k in range(n_exps):
    dictexps.update(dict_exp(Expe(project='CMIP5', model='CNRM-CM5', name='historical', number=k+1, ybeg=1981, yend=2005)))
    dictexps.update(dict_exp(Expe(project='CMIP5', model='CNRM-CM5', name='historicalExt', number=k+1, ybeg=2005, yend=2010)))
ds_CM5 = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['zonmean', 'invertlev'], harmonizeCoords=True, verbose=True)
ds_CM5['historical'] = xr.concat([ds_CM5['historical'], ds_CM5['historicalExt']], dim='time')
ds_CM5.pop('historicalExt')
print('> Size of dimension time = %s'%np.size(ds_CM5['historical']['time']))
print('----------------------------------------------------------------------------------------------')


# -- Example to compute AMOC in ssp245 experiment
dictexps = {}
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='ssp245', ybeg=2015, yend=2020, number=1)))

dictvars = {}
var='msftyz'
dictvars.update(dict_var(var, 'Omon', grid='gn'))

amoc = lambda dico : amoc26(dico, ['yearavg'])
datasets = load_datas(dictexps, dictvars, operation=amoc, verbose=True, computeAnom='all', add_rnet=False)

print(datasets)
print('Mean value of AMOC for period 2015-2020 in ssp245 : %s'%np.mean(datasets['ssp245']['msftyz'].values))
print('----------------------------------------------------------------------------------------------')


# -- Some examples of xarray Dataset manipulations
#   - for more details, see : http://xarray.pydata.org/en/stable

dictexps = {}
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', ybeg=2000, yend=2014, number=1)))
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', ybeg=2000, yend=2014, number=2)))

dictvars = {}
dictvars.update(dict_var('tas', 'Amon'))

datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=None, verbose=True)

ds = datasets['historical']

# -- to compute DJF seasonal mean for all variables/members/models
#   - in this case, ds_ has a new coordinate 'season'
ds_ = ds.groupby('time.season').mean(dim='time').sel(season='DJF')
print(ds_)
print('----------------------------------------------------------------------------------------------')

# -- to compute ensemble mean for a specific model
ds_ = ds.sel(model='CNRM-CM6-1').mean(dim='member')
print(ds_)
print('----------------------------------------------------------------------------------------------')

# -- selection by index and/or selection by labels
arr = ds.sel(member=1, model='CNRM-CM6-1').isel(lon=0, lat=0, time=np.arange(0,10))['tas'].values
print(arr)
print('----------------------------------------------------------------------------------------------')


# -- add a variable in the dataset
ds['tas_deg'] = ds['tas'] - 273.15
print('max values : %s, %s'%(np.max(ds['tas_deg'].values),np.max(ds['tas'].values)))
print('----------------------------------------------------------------------------------------------')

# -- Some specific options in load_datas function
#   - module = 'iris' : choose to build iris' object instead of xarray's Dataset
#   - computeAnom = 'all' : add 'var_anom' computed as anomalies against the temporal mean of expe.expe_control
#   - add_rnet = True : add 'rnet' variable in the dataset, computed as : rsdt - rsut - rlut
#   - harmonizeCoords = True : rename typical coords (longitude, latitude, levels) in (lon, lat, plev)


# -- Example to re-use CliMAF facilities (e.g. explore) by using toggle ignore_data_not_found (default : False)
dictexps = {}
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='piClim-control', adds=dict(root='./datas'), ybeg=1850, yend=1851)))
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='piClim-4xCO2', adds=dict(root='./datas'), ybeg=1850, yend=1851)))

datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['yearavg'], ignore_data_not_found=True)
# datasets is a dictionary of xarray's object and unkwown piClim-4xCO2 experiment is not present
print('piClim-control' in datasets, 'piClim-4xCO2' in datasets)

datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['yearavg'])
# datasets is a Python dictionary with CliMAF request for unkwown piClim-4xCO2 experiment
print(datasets['experiment'])

print('----------------------------------------------------------------------------------------------')

# -- ??? Example to use specific period of piControl by using toggle keep_attrs (default : False)

dictexps = {}
eCTL = Expe(project='CMIP6', model='CNRM-CM6-1', name='piControl', ybeg=1850, yend=2349)
dictexps.update(dict_exp(eCTL))
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', number=1, ybeg=2000, yend=2004, expe_control=eCTL)))
dictexps.update(dict_exp(Expe(project='CMIP6', model='CNRM-CM6-1', name='historical', number=4, ybeg=2000, yend=2004, expe_control=eCTL)))

datasets = {}
datasets = load_datas(dictexps, dictvars, operation=cdogen, list_cdops=['fldmean', 'yearavg'], keep_attrs=True, computeAnom='respective')

tas_hist1_2000 = datasets['historical']['tas'].sel(member=1).isel(model=0, time=0, lon=0, lat=0).values
tas_piC_mean = datasets['piControl']['tas'].isel(member=0, model=0, time=np.arange(0, 499), lon=0, lat=0).mean(dim='time').values
anom_tas_hist1_2000 = tas_hist1_2000 - tas_piC_mean
tas_anom_hist1_2000 = datasets['historical']['tas_anom'].sel(member=1).isel(model=0, time=0, lon=0, lat=0).values
print(tas_hist1_2000, tas_piC_mean, anom_tas_hist1_2000, tas_anom_hist1_2000)

offset = 110 # hist_r4 (init date piControl : 19600101)
tas_hist4_2000 = datasets['historical']['tas'].sel(member=4).isel(model=0, time=0, lon=0, lat=0).values
tas_piC_mean = datasets['piControl']['tas'].isel(member=0, model=0, time=np.arange(offset+150, offset+155), lon=0, lat=0).mean(dim='time').values
anom_tas_hist4_2000 = tas_hist4_2000 - tas_piC_mean
tas_anom_hist4_2000 = datasets['historical']['tas_anom'].sel(member=4).isel(model=0, time=0, lon=0, lat=0).values
print(tas_hist4_2000, tas_piC_mean, anom_tas_hist4_2000, tas_anom_hist4_2000)

print('----------------------------------------------------------------------------------------------')

exit()
