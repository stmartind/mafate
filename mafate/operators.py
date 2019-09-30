from climaf.api import *
import copy
from .utils import cdogen

def amoc26(climaf_dico, list_cdops) :
    '''
    Compute AMOC at 26N (standard resolution, CMIP6 grid)
    '''
    dsc  = ds(**climaf_dico)
    x = ccdo(cslice(cslice(dsc, dim='j-mean', min=190, max=190), dim='basin', min=2, max=2), operator='vertmax')
    return cdogen(x, list_cdops)


def amoc26_cm5(climaf_dico, list_cdops):
    '''
    Compute AMOC at 26N (standard resolution, CMIP5 grid)
    '''
    dsc  = ds(**climaf_dico)
    x = ccdo(cslice(cslice(dsc, dim='lat', min=190, max=190), dim='basin', min=3, max=3), operator='vertmax')
    return cdogen(x, list_cdops)


def amoc26_hr(climaf_dico, list_cdops):
    '''
    Compute AMOC at 26N (high resolution)
    '''
    dsc  = ds(**climaf_dico)
    x = ccdo(cslice(cslice(dsc, dim='j-mean', min=636, max=636), dim='basin', min=2, max=2), operator='vertmax')
    return cdogen(x, list_cdops)


def ACC(climaf_dico, list_cdops) :
    dsc  = ds(**climaf_dico)
    x = fdiv(cslice(dsc, dim='line', min=5, max=5), 1026*1e6)
    return cdogen(x, list_cdops)


derive('*', 'hfnet', 'plus', 'hfls','hfss')
derive('*', 'rss',   'minus', 'rsds','rsus')
derive('*', 'rls',   'minus', 'rlds','rlus')
derive('*', 'rnet',  'plus', 'rls','rss')
derive('*', 'sfnet',  'minus', 'rnet','hfnet')

def land(climaf_dico, list_cdops) :
    dsc  = ds(**climaf_dico)
    cdf = copy.copy(climaf_dico)
    cdf.pop('variable')
    cdf.pop('table')
    cdf.pop('period')
    cdf.pop('experiment')
    cdf.pop('project') # un peu fort et ne permettra pas de traiter d autres modeles mais permet de passer le spin-up
    # je prend sur piControl sinon il n est pas toujours defini
    dsw = fdiv(ds(project='CMIP6', period='fx', variable='sftlf', table='fx', experiment='piControl', **cdf), 100.)
    #wsum = cdogen(dsw, ['fldsum'])
    #dsw = fdiv(dsw, float(cscalar(wsum)))
    x = fmul(dsc,dsw)
    return cdogen(x, list_cdops)

def ocean(climaf_dico, list_cdops) :
    dsc  = ds(**climaf_dico)
    cdf = copy.copy(climaf_dico)
    cdf.pop('variable')
    cdf.pop('table')
    cdf.pop('period')
    cdf.pop('experiment')
    cdf.pop('project')
    # je prend sur piControl sinon il n est pas toujours defini
    dsw = fmul(fsub(fdiv(ds(project='CMIP6',period='fx', variable='sftlf', table='fx', experiment='piControl', **cdf), 100.), 1.), -1.)
    x = fmul(dsc,dsw)
    return cdogen(x, list_cdops)



#define regions
region = dict( PACTROP = (-30,30,120,300), PACTROPS = (-30,30,220,250), TROP=(-30,30,0,360), \
               AMAZON=(-3,3,290,330), ATLN=(50,65,280,360), ARC=(65,90,0,360), LAB=(50,70,300,330))
class creg(object) :
    def __init__(self,name) :
       self.lat1 = region[name][0]
       self.lat2 = region[name][1]
       self.lat  = region[name][0:2]
       self.lon1 = region[name][2]
       self.lon2 = region[name][3]
       self.lon  = region[name][2:4]
       self.llbox = region[name][2:4]+region[name][0:2]
       
