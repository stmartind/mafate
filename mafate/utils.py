from climaf.api import *
import xarray as xr
import numpy as np
from .varexpe import Expe, Variable
import datetime, string
import sys


def cdogen(x, list_cdops):
    '''
    Apply successively a list of cdo operations, list_cdops
    '''
    if list_cdops is None:
        return x
    else:
        for op in list_cdops:
            x = ccdo(x, operator=op)
        return x


def define_climaf_project(name, facets=['model', 'experiment', 'member', 'realization', 'variable', 'table', 'gridtype'], root_dirs=[], file_patterns=[]):
    '''
    Define a new CliMAF project by setting :
      - a name (string) 
      - facets (list)
      - a data localization : full combination of root_dirs (list) and file_patterns (list)
    '''
    cproject(name, *facets)
    dataloc(project = name, organization = 'generic', url = [d+'/'+f for d in root_dirs for f in file_patterns])


def dict_exp(my_expe):
    '''
    Define a dict of one single Expe my_expe
    '''
    dict_expe = {}
    dict_expe[my_expe.expid()] = my_expe
    return dict_expe


def dict_var(name, table='*', grid='gr'):
    '''
    Define a dict of one single variable with name, table and grid
    '''
    dict_vars = {}
    v = Variable(name=name, table=table, grid=grid)
    dict_vars[v.name] = v
    return dict_vars


def extract_from_exp(datasets, expe, member=None ):
    '''
    Get dataset from a single expe
    '''
    if expe is None:
        return None
    else:
        if member is None : member = expe.number
        return datasets[expe.name].sel(model=expe.model, member=member)


def get_time(dataset, time_dims=['time_counter', 'time'], attrs='year'):
    '''
    '''
    for dim_name in time_dims:
        if dim_name in dataset.dims:
            break 
    try:
        if attrs == 'year':
            data_x = dataset[dim_name].dt.year
        else:
            print('to be coded later...')
    except:
        if attrs == 'year':
            data_x = list(elt.year for elt in dataset[dim_name].values)
        else:
            print('to be coded later...')
    return data_x


def addnyears(datasets, dictexpes):
    '''
    '''
    for exp in list(dictexpes.values()):
        ds_ = datasets[exp.name]
        if 'n_years' not in list(ds_.coords):
            ds_ = ds_.assign_coords(n_years = ('model', np.arange(len(ds_.model))))
        ds_.n_years.loc[dict(model=exp.model)] = exp.yend - exp.ybeg + 1
        datasets[exp.name] = ds_


def compute_anom_from_control(datasets, dictexpes, dictvars, dimtim, computeAnom, ignore_data_not_found):
    '''
    '''
    for var in list(dictvars.values()):
        for exp in list(dictexpes.values()):
            compute_anom_from_control_varexpe(datasets, var, exp, dimtim, computeAnom, ignore_data_not_found)


def compute_anom_from_control_varexpe_allperiod(datasets, var, expe, dimtim):
    '''
    '''
    ds_exp = extract_from_exp(datasets, expe)
    ds_ctl = extract_from_exp(datasets, expe.expe_control)
    if var.name+'_anom' not in datasets[expe.name].variables:
        datasets[expe.name][var.name+'_anom'] = xr.full_like(datasets[expe.name][var.name], fill_value=None)
    time_name = None
    for name in dimtim:
        if name in ds_ctl[var.name].dims:
            time_name = name
    datasets[expe.name][var.name+'_anom'].loc[dict(model=expe.model, member=expe.number)] = datasets[expe.name][var.name].loc[dict(model=expe.model, member=expe.number)] - ds_ctl[var.name].mean(dim=time_name)


def compute_anom_member_from_picontrol_varexpe(datasets, var, expe, ignore_data_not_found):
    ''' 
    Cas specifique ou le control varie par sa date de debut pas par son numero de membre...
    '''
    ds_exp = extract_from_exp(datasets, expe)
    attrs = datasets[expe.name].attrs
    parent_time_units = attrs['parent_time_units'].split()
    time_unit_ctl = datetime.datetime.strptime(string.join(parent_time_units[2:4]),'%Y-%m-%d %X')
    time_start_expe_delta_in_ctl = datetime.timedelta(float(attrs['branch_time_in_parent_%s'%expe.expid()]))
    time_start_expe_in_ctl = time_unit_ctl + time_start_expe_delta_in_ctl
    exp_time = get_time(datasets[expe.name])
    pi_End_year = time_start_expe_in_ctl.year + exp_time[-1] - 1850
    pi_Start_sel = time_start_expe_in_ctl.year + exp_time[0] - 1850
    ds_ctl = extract_from_exp(datasets, expe.expe_control, 1)
    Ctrl = ds_ctl[var.name].sel(time=slice(datetime.datetime(pi_Start_sel,1,1), datetime.datetime(pi_End_year,12,31)), drop=True)
    Data = datasets[expe.name][var.name].sel(model=expe.model, member=expe.number)
    try : Data, Ctrl = xr.align(Data, Ctrl, join='left')
    except : 
        if ignore_data_not_found : return
        else : sys.exit("Ctrl read period does not encompass the experiment %s corresponding period in piControl"%expe.expid())
    if var.name+'_anom' not in datasets[expe.name].variables:
        datasets[expe.name][var.name+'_anom'] = xr.full_like(datasets[expe.name][var.name], fill_value=None)
    datasets[expe.name][var.name+'_anom'].loc[dict(model=expe.model, member=expe.number)] = Data - Ctrl.mean(dim='time')


def compute_anom_from_control_varexpe(datasets, var, expe, dimtim, computeAnom, ignore_data_not_found):
    '''
    '''
    if computeAnom == 'all':
        compute_anom_from_control_varexpe_allperiod(datasets, var, expe, dimtim)
    elif computeAnom == 'respective':
        if expe.expe_control is not expe:
            if expe.expe_control.name == 'piControl':
                # Cas specifique ou on prend une periode differente du piControl = qui correspond a celle de l'historique
                compute_anom_member_from_picontrol_varexpe(datasets, var, expe, ignore_data_not_found)
            else:
                print("When using computeAnom == 'respective' you have to indicate a expe_control.name == 'piControl'")
        else:
            compute_anom_from_control_varexpe_allperiod(datasets, var, expe, dimtim)
    else:
        print('computeAnom not known')


def harmonizingCoords(ds):
    '''
    Auxiliary function to standardize coordinate names
    '''
    _levs = ['levels', 'level', 'pstd', 'lev']
    _lats = ['latitude']
    _lons = ['longitude']
    _time = ['time_counter']
    lev_ = 'plev'
    lat_ = 'lat'
    lon_ = 'lon'
    tim_ = 'time'
    ds = renameCoords(ds, _levs, lev_)
    ds = renameCoords(ds, _lats, lat_)
    ds = renameCoords(ds, _lons, lon_)
    ds = renameCoords(ds, _time, tim_)    
    return ds


def renameCoords(ds, liste, name):
    '''
    '''
    for xname in liste:
        if xname in ds:
            ds = ds.rename({xname:name})
    return ds


def updated_attrs(attrs_org, ds_src, key_attrs, list_attrs=['branch_time_in_parent']):
    '''
    Returns a updated value of the 'attributes' dict, attrs_org
    Get values of list_attrs in ds_src
    '''
    attrs_new = attrs_org
    attrs_src = ds_src.attrs
    for att_ in list_attrs:
        if att_ in attrs_src.keys():
            attrs_new[att_+'_'+key_attrs] = attrs_src[att_]
    return attrs_new


def dropCoords(ds, lst_to_drop):
    '''
    '''
    for coord_ in lst_to_drop:
        if coord_ in ds.coords.keys():
            ds = ds.drop(coord_)
    return ds


def dropVars(ds, lst_to_drop):
    '''
    '''
    for var_ in lst_to_drop:
        if var_ in list(ds.data_vars.keys()):
            ds = ds.drop(var_)
    return ds


def open_and_expand_dataset(my_file, dict_add_dims, module, harmonizeCoords, dropList, var=None):
    '''
    Auxiliary function to extend the use of xarray function open_dataset
    Add new dimensions defined by dict_add_dims
    '''
    if module == 'xarray':
        xds = xr.open_dataset(my_file)
        if dropList is not None:
            xds = dropCoords(xds, dropList)
            xds = dropVars(xds, dropList)
        if harmonizeCoords:
            xds = harmonizingCoords(xds)
    if module == 'iris':
        import iris
        xds = iris.load(my_file)
        xds[0].attributes = {}
        xds[0].rename(var.varid())
    for d in list(dict_add_dims.keys()):
        if module == 'xarray':
            xds = xds.expand_dims(d)
            xds[d] = dict_add_dims[d]
        if module == 'iris':
            import iris
            newdim = iris.coords.AuxCoord(dict_add_dims[d], long_name=d)
            xds[0].add_aux_coord(newdim)
    return xds


def convert_climaf_dataset(datasets, var, exp, climaf_dico, operation, list_cdops, dir_target, module, writeFiles, suffFiles, harmonizeCoords, dropList, verbose, ignore_data_not_found, keep_attrs):
    '''
    Auxiliary function to convert a CliMAF dataset/object to :
        - either a target file
        - either a xarray dataset or a iris object
    '''
    exp_id = exp.expid()
    climaf_ds = ds(**climaf_dico)
    if climaf_ds is not None:
        if verbose:
            if hasattr(climaf_ds, 'listfiles'):
                print('Loading data from files : ', climaf_ds.listfiles())
            else:
                print('Loading data from CliMAF dataset : ', climaf_ds)
        if writeFiles:
            if operation == cdogen:
                if list_cdops is None:
                    target_file = dir_target+'/'+var.varid()+'_'+var.table+'_'+exp.period(norm=True)+'_'+exp_id+suffFiles
                    try : cfile(climaf_ds, target=target_file)
                    except : 
                        print('CliMAF could not find the expected data, use explore fonction on the returned dictionary')
                        return climaf_dico
                else:
                    reftime = None
                    substr = 'settaxis'
                    if any(substr in s for s in list_cdops):
                        reftime = int([s for s in list_cdops if substr in s][0][9:13])
                    target_file = dir_target+'/'+var.varid()+'_'+var.table+'_'+exp.period(norm=True, reftime=reftime)+'_'+exp_id+suffFiles                    
                    try : cfile(operation(climaf_ds, list_cdops), target=target_file)
                    except : 
                        print('CliMAF could not find the expected data, use explore fonction on the returned dictionary')
                        return climaf_dico
            else:
                print(operation, ' not known...')
                return
        else:
            if operation == cdogen :
               climaf_ds = operation(climaf_ds, list_cdops)
            else :
               climaf_ds = operation(climaf_dico)
            try : climaf_interpret = cfile(climaf_ds)
            except :
              if ignore_data_not_found :
                  print('CliMAF could not find the data for %s'%climaf_dico)
                  return
              else :
                  print('CliMAF could not find the expected data, use explore fonction on the returned dictionary')
                  return climaf_dico
            xds = open_and_expand_dataset(climaf_interpret, {'model':[exp.model], 'member':np.array([exp.number])}, module, harmonizeCoords, dropList, var)
            if verbose:
                print('Loading data for expid::%s and for varid::%s'%(exp.expid(), var.varid()))
            if exp.name in datasets:
                if module == 'xarray':
                    if keep_attrs:
                        attrs = datasets[exp.name].attrs
                    datasets[exp.name] = xr.merge([datasets[exp.name], xds])
                    if keep_attrs:
                        datasets[exp.name].attrs = updated_attrs(attrs, xds, exp.expid())
                if module == 'iris':
                    import iris
                    datasets[exp.name] = (datasets[exp.name] + xds).merge()
            else:
                datasets[exp.name] = xds
                if keep_attrs:
                    datasets[exp.name].attrs = updated_attrs(datasets[exp.name].attrs, xds, exp.expid())
    else:
        print('Data not found for expid::%s and for varid::%s'%(exp.expid(), var.varid()))


def load_datas(dictexpes, dictvars, operation=cdogen, list_cdops=None, dir_target='.', module='xarray', writeFiles=False, suffFiles='.nc', dropList=None, \
        computeAnom=None, add_rnet=True, add_nyears=False, harmonizeCoords=False, verbose=False, ignore_data_not_found=False, keep_attrs=False, dimtim=['time','time_counter']):
    '''
    Get data from : 
    - a specific dict of Expe-s : dictexpes
    - a specific dict of Var-s : dictvars

    Apply a list of cdo operation (list_cdops) to data

    Rq : the option dir_target/writeFiles is temporary (it is only used to quickly copy the CliMAF cache : use for lx and px PCs)

    > Return a dictionary of xarray's Dataset or iris's object indexed by the experiment name:
        All the models/members/variables are grouped in a single Dataset for each experiment

        computeAnom = 'all' : compute the anomaly to the period of ref experiment indicated, ie the same reference period for all members 
        computeAnom = 'respective' : compute the anomaly to the respective period in the ref experiment, ie period depends members start date in parent 
    '''
    my_datasets = {}
    for var in list(dictvars.values()):
        for exp in list(dictexpes.values()):
            m = exp.number
            dicof = dict(project=exp.project, variable=var.name, table=var.table, grid=var.grid, gridtype=var.grid, model=exp.model, experiment=exp.name, \
                    realization='r'+str(m)+exp.realization, member=m, period=exp.period(), **exp.adds)
            dico = convert_climaf_dataset(my_datasets, var, exp, dicof, operation, list_cdops, dir_target, module, writeFiles, suffFiles, harmonizeCoords, dropList, verbose, ignore_data_not_found, keep_attrs)
            if dico is not None:
                return dico
    if writeFiles:
        return
    if computeAnom is not None :
        compute_anom_from_control(my_datasets, dictexpes, dictvars, dimtim, computeAnom, ignore_data_not_found)
    if add_nyears:
        addnyears(my_datasets, dictexpes)
    if add_rnet:
        for e_ in list(my_datasets.keys()):
            ds_ = my_datasets[e_]
            # -- add new var 'rnet' from rsdt, rsut and rlut values
            if 'rsdt' in ds_.variables:
                ds_['rnet'] = ds_['rsdt'] - ds_['rsut'] - ds_['rlut']
                if computeAnom is not None:
                    ds_['rnet_anom'] = ds_['rsdt_anom'] - ds_['rsut_anom'] - ds_['rlut_anom']
    return my_datasets
