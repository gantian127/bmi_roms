# -*- coding: utf-8 -*-
import xarray as xr
import numpy as np

from .errors import DataError


class RomsData:

    """Access data and metadata in a ROMS data file."""

    def __init__(self, filename=None):
        """Make a RomsData object.
        Parameters
        ----------
        filename : str, optional
            Path or URL (e.g., OPeNDAP data url) to the file to open.
        """

        self._filename = None
        self._data = None
        self._var_list = None
        self._grid_list = None
        self._var_info = None
        self._grid_info = None
        self._time_info = None
        self._dim_info = None

        if filename is not None:
            self.open(filename)

    @property
    def data(self):
        return self._data

    @property
    def filename(self):
        return self._filename

    @property
    def grid_info(self):
        return self._grid_info

    @property
    def dim_info(self):
        return self._dim_info

    @property
    def var_info(self):
        return self._var_info

    @property
    def time_info(self):
        return self._time_info

    def open(self, filename):

        """Load a ROMS data file into a xarray DataArray.
        Parameters.
        ----------
        filename : str
            Path or URL to the file to open.
        """

        self._filename = filename
        self._data = xr.open_dataset(self._filename, decode_cf=False)
        self._get_var_grid_list()

        return self.data

    def get_grid_info(self):
        # get dim info
        dim_info = self._get_dim_info()

        # get grid info
        try:
            grid_info = {}
            for index, dim in enumerate(self._grid_list):
                x_name = dim[-1]
                y_name = dim[-2]
                z_name = dim[-3] if len(dim) > 3 else None

                grid_info[index] = {
                    # suppose var is 3 or 4 dim and exclude time dimension to get shape info
                    'shape': tuple([self.data.dims[dim_name] for dim_name in dim[1:]]),
                    'yx_spacing': (dim_info[y_name]['spacing_y'], dim_info[x_name]['spacing_x']),
                    'yx_of_lower_left': (dim_info[y_name]['lower_left_y'], dim_info[x_name]['lower_left_x']),
                    'grid_x': dim_info[x_name]['grid_x'],
                    'grid_y': dim_info[y_name]['grid_y'],
                    'grid_z': dim_info[z_name]['grid_z'] if z_name is not None else 0,
                }

            self._grid_info = grid_info

        except Exception:
            raise DataError('Failed to get the grid information for {} from the dataset.'.format(dim))

        return self.grid_info

    def get_time_info(self):
        try:
            # identify time dim name and suppose there is only one time dimension
            time_name = set([dims[0] for dims in self._grid_list]).pop()
            time_var = self._data.coords[time_name]

            # time values are float in BMI time function
            time_info = {
                'start_time': float(time_var.values[0]),
                'time_step': 0.0 if len(time_var.values) == 1 else
                float(time_var.values[1] - time_var.values[0]),
                'end_time': float(time_var.values[-1]),
                'total_steps': len(time_var.values),
                'time_units': time_var.units,
                'calendar': time_var.calendar,
                'time_value': time_var.values.astype('float'),
            }

            self._time_info = time_info

        except Exception:
            raise DataError('Failed to get the time information from the dataset.')

        return self.time_info

    def get_var_info(self):
        var_info = {}
        try:
            for var_name, grid_id in self._var_list:
                var = self._data.data_vars[var_name]
                var_info[var.long_name] = {
                    'var_name': var_name,
                    'dtype':  str(var.dtype),
                    'itemsize': var.values.itemsize,
                    'nbytes': var.values[0].nbytes,  # current time step nbytes
                    'units': var.units if 'units' in var.attrs else 'N/A',
                    'location': 'node',
                    'grid_id': grid_id,
                }

            self._var_info = var_info

        except Exception:
            raise DataError('Failed to get the variable information for {} from the dataset.'.format(var_name))

        return self.var_info

    def _get_var_grid_list(self):
        var_list = []
        grid_list = []

        # get valid var and grid list
        for var_name in self._data.data_vars.keys():
            var_obj = self._data.data_vars[var_name]
            if len(var_obj.shape) >= 3:  # only get var with 3 or 4 dims TODO include 2D var for lat_u, lon_u 2D
                var_list.append(var_name)
                if var_obj.dims not in grid_list:
                    grid_list.append(var_obj.dims)

        # assign grid id to var list
        for index, var_name in enumerate(var_list):
            var_obj = self._data.data_vars[var_name]
            var_list[index] = [var_name, grid_list.index(var_obj.dims)]

        self._grid_list = tuple(grid_list)
        self._var_list = tuple(var_list)

    def _get_dim_info(self):
        # get unique dim names
        dim_list = list(set([item for sublist in self._grid_list for item in sublist]))

        # get dim info
        if dim_list:
            dim_info = {}
            for dim_name in dim_list:
                if 's_' in dim_name:  # TODO: get actual s_rho and s_w values, current value is layer numer
                    dim_info[dim_name] = {
                        'grid_z': np.arange(1, self._data.dims[dim_name]+1, dtype=float),  # value represent layer number
                    }

                elif 'xi_' in dim_name:  # TODO: get correct lon_u,v,rho values, current value is grid index number
                    if dim_name.replace('xi', 'x') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('xi', 'x')
                        grid_x = self._data.data_vars[coor_var].values[0, :]
                        dim_info[dim_name] = {
                            'grid_x': grid_x,
                            'lower_left_x': grid_x[0],
                            'spacing_x': grid_x[1] - grid_x[0],
                        }
                    elif dim_name.replace('xi', 'lon') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('xi', 'lon')
                        dim_info[dim_name] = {
                            'grid_x': np.arange(1, self._data.data_vars[coor_var].shape[1]+1, dtype=float),
                            'lower_left_x': 1.0,
                            'spacing_x': 1.0,
                        }

                elif 'eta_' in dim_name:  # TODO: get correct lat_u,v,rho values, current value is grid index number
                    if dim_name.replace('eta', 'y') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('eta', 'y')
                        grid_y = self._data.data_vars[coor_var].values[:, 0]
                        dim_info[dim_name] = {
                            'grid_y': grid_y,
                            'lower_left_y': grid_y[0],
                            'spacing_y': grid_y[1] - grid_y[0],
                        }

                    elif dim_name.replace('eta', 'lat') in self._data.data_vars.keys():
                        coor_var = dim_name.replace('eta', 'lat')
                        dim_info[dim_name] = {
                            'grid_y': np.arange(1, self._data.data_vars[coor_var].shape[0]+1, dtype=float),
                            'lower_left_y': 1.0,
                            'spacing_y': 1.0,
                        }

                elif 'Nbed' == dim_name:  # TODO: need to get actual Nbed values, current value is layer number
                    dim_info[dim_name] = {
                        'grid_z': np.arange(1, self._data.dims['Nbed']+1, dtype=float),  # value represent layer number
                    }

            self._dim_info = dim_info

        else:
            raise DataError('Failed to get the dimension information from the dataset.')

        return self.dim_info


