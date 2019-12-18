import numpy as np
from .varexpe import Expe, Variable
from .utils import *


def define_climaf_projects():
    '''
    Define a set of CliMAF projects
    '''
    name = 'multiCMIP5'
    root_dirs = []
    root_dirs.append('/cnrm/cmip/cnrm/ESG/CMIP5/output*/*/${model}/${experiment}/*/*/${table}/${realization}/*/${variable}')    
    root_dirs.append('/cnrm/cmip/CMIP5/Atmos/Origin/*/${model}/${experiment}/mon/atmos/${realization}')
    file_patterns = []
    file_patterns.append('${variable}_${table}_${model}_${experiment}_r${member}i1p1_YYYYMM-YYYYMM.nc')
    define_climaf_project(name, root_dirs=root_dirs, file_patterns=file_patterns)


def dict_expes_CMIP5_piControl(project_name='multiCMIP5'):
    '''
    Define a specific dict of Expe-s for CMIP-5 piControl-related studies
    '''
    dict_allexpes = {}
    expe_name = 'piControl'
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='bcc-csm1-1', name=expe_name, ybeg=1, yend=500)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='BNU-ESM', name=expe_name, ybeg=1450, yend=2008)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CanESM2', name=expe_name, ybeg=2015, yend=3010)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CCSM4', name=expe_name, ybeg=250, yend=1300)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CNRM-CM5', name=expe_name, ybeg=1850, yend=2699)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CSIRO-Mk3-6-0', name=expe_name, ybeg=1, yend=500)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='FGOALS-s2', name=expe_name, ybeg=1850, yend=2350)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='GFDL-ESM2M', name=expe_name, ybeg=1, yend=500)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='HadGEM2-ES', name=expe_name, ybeg=1860, yend=2434)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='inmcm4', name=expe_name, ybeg=1860, yend=2349)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='IPSL-CM5A-LR', name=expe_name, ybeg=1800, yend=2799)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MIROC5', name=expe_name, ybeg=2000, yend=2699)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MPI-ESM-LR', name=expe_name, ybeg=1850, yend=2849)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MRI-CGCM3', name=expe_name, ybeg=1851, yend=2350)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='NorESM1-M', name=expe_name, ybeg=700, yend=1200)))
    return dict_allexpes


def dict_expes_CMIP5_historical(project_name='multiCMIP5'):
    '''
    Define a specific dict of Expe-s for CMIP-5 historical-related studies
    '''
    dict_allexpes = {}
    expe_name = 'historical'
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='bcc-csm1-1', name=expe_name, member=[1,2,3], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='BNU-ESM', name=expe_name, member=[1], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CanESM2', name=expe_name, member=[1,2,3,4,5], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CCSM4', name=expe_name, member=[1,2,3,4,5,6], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CSIRO-Mk3-6-0', name=expe_name, member=[1,2,3,4,5,6,7,8,9,10], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='FGOALS-s2', name=expe_name, member=[1,2,3], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='GFDL-ESM2M', name=expe_name, member=[1], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='HadGEM2-ES', name=expe_name, member=[1,2,3,4], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='inmcm4', name=expe_name, member=[1], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='IPSL-CM5A-LR', name=expe_name, member=[1,2,3,4,5,6], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MIROC5', name=expe_name, member=[1,2,3,4], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MPI-ESM-LR', name=expe_name, member=[1], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MRI-CGCM3', name=expe_name, member=[1,2,3], ybeg=1850, yend=2005)))
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='NorESM1-M', name=expe_name, member=[1,2,3], ybeg=1850, yend=2005)))
    return dict_allexpes


def dict_expes_CMIP5_abrupt4xCO2(project_name='multiCMIP5'):
    '''
    Define the specific dict of Expe-s for CMIP-5 abrupt4xCO2-related studies
    '''
    dict_allexpes = {}
    expe_name_CTL = 'piControl'
    expe_name = 'abrupt4xCO2'
    eCTL = Expe(project=project_name, model='bcc-csm1-1', name=expe_name_CTL, ybeg=1, yend=500)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='bcc-csm1-1', name=expe_name, expe_control=eCTL, ybeg=160, yend=309)))
    eCTL = Expe(project=project_name, model='BNU-ESM', name=expe_name_CTL, ybeg=1450, yend=2008)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='BNU-ESM', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='CanESM2', name=expe_name_CTL, ybeg=2015, yend=3010)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CanESM2', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='CCSM4', name=expe_name_CTL, ybeg=250, yend=1300)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CCSM4', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='CNRM-CM5', name=expe_name_CTL, ybeg=1850, yend=2699)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CNRM-CM5', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='CSIRO-Mk3-6-0', name=expe_name_CTL, ybeg=1, yend=500)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='CSIRO-Mk3-6-0', name=expe_name, expe_control=eCTL, ybeg=1, yend=150)))
    eCTL = Expe(project=project_name, model='FGOALS-s2', name=expe_name_CTL, ybeg=1850, yend=2350)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='FGOALS-s2', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='GFDL-ESM2M', name=expe_name_CTL, ybeg=1, yend=500)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='GFDL-ESM2M', name=expe_name, expe_control=eCTL, ybeg=1, yend=150)))
    eCTL = Expe(project=project_name, model='HadGEM2-ES', name=expe_name_CTL, ybeg=1860, yend=2434)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='HadGEM2-ES', name=expe_name, expe_control=eCTL, ybeg=1860, yend=2009)))
    eCTL = Expe(project=project_name, model='inmcm4', name=expe_name_CTL, ybeg=1860, yend=2349)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='inmcm4', name=expe_name, expe_control=eCTL, ybeg=2090, yend=2239)))
    eCTL = Expe(project=project_name, model='IPSL-CM5A-LR', name=expe_name_CTL, ybeg=1800, yend=2799)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='IPSL-CM5A-LR', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='MIROC5', name=expe_name_CTL, ybeg=2000, yend=2699)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MIROC5', name=expe_name, expe_control=eCTL, ybeg=2100, yend=2250)))
    eCTL = Expe(project=project_name, model='MPI-ESM-LR', name=expe_name_CTL, ybeg=1850, yend=2849)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MPI-ESM-LR', name=expe_name, expe_control=eCTL, ybeg=1850, yend=1999)))
    eCTL = Expe(project=project_name, model='MRI-CGCM3', name=expe_name_CTL, ybeg=1851, yend=2350)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='MRI-CGCM3', name=expe_name, expe_control=eCTL, ybeg=1851, yend=2000)))
    eCTL = Expe(project=project_name, model='NorESM1-M', name=expe_name_CTL, ybeg=700, yend=1200)
    dict_allexpes.update(dict_exp(Expe(project=project_name, model='NorESM1-M', name=expe_name, expe_control=eCTL, ybeg=1, yend=150)))
    return dict_allexpes


def dict_expes_historical_CNRMCM(model_name='CNRM-CM6-1', n_member=10, ybeg=1850, yend=2014, yend_piControl=0):
    '''
    Define a specific dict of Expe-s for CNRM-CM6-1 (or CNRM-CM5) historical simulations
    '''
    if model_name == 'CNRM-CM6-1':
        project_name = 'CMIP6'
    elif model_name == 'CNRM-CM5':
        project_name = 'multiCMIP5'
    else:
        return None
    dict_allexpes = {}
    eCTL = None
    if yend_piControl > 0:
        # -- add piControl experiment to the dict of Expe-s
        eCTL = Expe(project=project_name, model=model_name, name='piControl', ybeg=1850, yend=yend_piControl, marker=',', color='silver')
        dict_allexpes.update(dict_exp(eCTL))
    for n in range(n_member):
        dict_allexpes.update(dict_exp(Expe(project=project_name, model=model_name, name='historical', number=n+1, ybeg=ybeg, yend=yend, expe_control=eCTL, marker=',', color='dimgray')))
    return dict_allexpes


def dict_vars_NT():
    '''
    Define the specific dict of Variable-s for N-T plot study
    '''
    dict_vars = {}
    v = Variable(name='tas', table='Amon')
    dict_vars[v.name] = v
    v = Variable(name='rsdt', table='Amon')
    dict_vars[v.name] = v
    v = Variable(name='rsut', table='Amon')
    dict_vars[v.name] = v
    v = Variable(name='rlut', table='Amon')
    dict_vars[v.name] = v
    return dict_vars


def dict_vars_heatc():
    '''
    Define the specific dict of Variable-s for heat contents
    '''
    dict_vars = {}
    v = Variable(name='hc2000', table='HOMOImon')
    dict_vars[v.name] = v
    v = Variable(name='hc700', table='HOMOImon')
    dict_vars[v.name] = v
    v = Variable(name='heatc', table='HOMOImon')
    dict_vars[v.name] = v
    v = Variable(name='hcont300', table='Emon')
    dict_vars[v.name] = v
    return dict_vars
