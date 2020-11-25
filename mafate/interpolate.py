import numpy as np
import xarray as xr


sorted_dims = ['time', 'plev', u'lat', u'lon']

plev19 = np.array([100000., 92500., 85000., 70000., 60000., 50000., 40000., \
        30000., 25000., 20000., 15000., 10000., 7000., 5000., 3000., \
        2000., 1000., 500., 100.], dtype=np.float32)


def lev2plev(dataset_lev, var_name, \
        coords_p = plev19, \
        lev_name='lev', plev_name='plev', \
        extrapolation=False, \
        new_var_name=None, nc_file_name=None):
    '''
        OK if 'ap', 'b', 'ps', 'var_name' : variables of dataset_lev
    
        dataset : xarray-Dataset
        var_name is a variable of dataset_lev

        coords_p (default : plev19) : set of pressures at which dataset[var_name] is evaluated
        lev_name (default : 'lev')  : coordinate of var_name, ap and b variables
        plev_name(default : 'plev') : name of the new coordinate

        nc_file_name (default : None) : output_file
        new_var_name (default : var_name) : new var name

        Returns :
            xarray-Dataset which contains var_name on coords_p
    '''

    pressure_name ='p'

    # -- Compute model levels pressure
    #       p(x, ...) = ap + b * p(x, ...)
    dataset_lev[pressure_name] = dataset_lev['ap'] + dataset_lev['b']*dataset_lev['ps']

    # -- Compute (interpolate) var on given coords_p
    #       mapping var(x, ..., p(x, ...)) on var(x, ..., coords_p) 
    da_ = interp_xr(dataset_lev[var_name], dataset_lev[pressure_name], coords_p, plev_name, lev_name, extrapolation=extrapolation)
 
    ordered_dims = []
    for dim_ in sorted_dims:
        if dim_ in da_.dims:
            ordered_dims.append(dim_)

    suffix = '_on_p'

    dataset_lev[var_name+suffix] = da_.transpose(*ordered_dims)
    dataset_plev = dataset_lev[[var_name+suffix, 'time_bounds']]

    if new_var_name is None:
        dataset_plev = dataset_plev.rename({var_name+suffix: var_name})
    else:
        dataset_plev = dataset_plev.rename({var_name+suffix: new_var_name})

    dataset_plev[plev_name].attrs = {\
            'name': 'plev', \
            'standard_name': 'air_pressure', \
            'long_name': 'pressure', \
            'units': 'Pa', \
            'positive': 'down' \
            }

    if nc_file_name is not None:
        dataset_plev.to_netcdf(nc_file_name)

    return dataset_plev


def interp_xr(ydata, xdata, xtarget, xtarget_name, input_dim_name, extrapolation=True):
    '''
    Vectorized interp1d_np function
    '''
    if extrapolation:
        interped = xr.apply_ufunc(
                interp1d_np,
                xtarget,
                xdata,
                ydata,
                input_core_dims=[[xtarget_name], [input_dim_name], [input_dim_name]],
                output_core_dims=[[xtarget_name]],
                exclude_dims=set((input_dim_name,)),
                vectorize=True,
                )
        interped[xtarget_name] = xtarget
    else:
        interped = xr.apply_ufunc(
                interp1d_np_noextrapolation,
                xtarget,
                xdata,
                ydata,
                input_core_dims=[[xtarget_name], [input_dim_name], [input_dim_name]],
                output_core_dims=[[xtarget_name]],
                exclude_dims=set((input_dim_name,)),
                vectorize=True,
                )
        interped[xtarget_name] = xtarget
    
    return interped.transpose()


def interp1d_np(x, xdata, ydata, extrapolation=True):
    '''
    Returns the one-d linear interpolant to a function with discrete data points (xdata, ydata), evaluated at x
    '''
    if xdata[-1] < xdata[0]:
        xdata = xdata[::-1]
        ydata = ydata[::-1]
    
    if extrapolation:
        return np.interp(x, xdata, ydata)
    else:
        y = np.interp(x, xdata, ydata)
        xmin, xmax = np.min(xdata), np.max(xdata)
        y[x > xmax] = np.nan
        y[x < xmin] = np.nan
    return y


def interp1d_np_noextrapolation(x, xdata, ydata):
    '''
    '''
    return interp1d_np(x, xdata, ydata, extrapolation=False)
