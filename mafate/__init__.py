version = '0.3.betafinal'

print('mafate version = '+version)

from .utils import cdogen, amoc26, amoc26_hr, define_climaf_project, dict_exp, dict_var, load_datas

from .varexpe import Expe, Variable

from .dicts import define_climaf_projects, dict_expes_CMIP5_piControl, dict_expes_CMIP5_historical, dict_expes_CMIP5_abrupt4xCO2, dict_expes_historical_CNRMCM, dict_vars_NT, dict_vars_heatc, extract_from_exp, compute_anom_from_control
