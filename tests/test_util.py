import os
import warnings

import xarray
import numpy as np
import pytest

from bmi_roms import RomsData


def test_open_data_with_url():
    try:
        url = 'https://tds.marine.rutgers.edu/thredds/dodsC/roms/doppio/2017_da/avg/runs/Averages_RUN_2023-03-31T00:00:00Z?s_rho[0:1:39],lon_rho[0:1:105][0:1:241],lat_rho[0:1:105][0:1:241],ocean_time[0:1:0],time[0:1:5],zeta[0:1:5][0:1:105][0:1:241],salt[0:1:5][0:1:39][0:1:105][0:1:241]'
        xarray.open_dataset(url)
    except Exception:
        url = None
        warnings.warn("The OPeNDAP url is not valid. Skip test_load_data_with_url().")

    if url is not None:
        roms_data = RomsData()
        roms_data.open(url, download=True)
        assert isinstance(roms_data.data, xarray.core.dataset.Dataset)
        assert os.path.isfile(roms_data.download_file)
        os.remove(roms_data.download_file)


def test_open_data_with_file():
    test_file = 'example.nc'
    if os.path.isfile(test_file):
        roms_data = RomsData()
        roms_data.open(test_file)
        assert isinstance(roms_data.data, xarray.core.dataset.Dataset)
    else:
        raise warnings.warn("Not able to get the test file. Skip test_open_data_with_file()")


def test_get_grid_info():
    test_file = 'example.nc'
    if os.path.isfile(test_file):
        roms_data = RomsData()
        grid_info_1 = roms_data.get_grid_info()
        assert grid_info_1 is None

        roms_data.open(test_file)
        grid_info_2 = roms_data.get_grid_info()
        assert isinstance(roms_data.data, xarray.core.dataset.Dataset)
        assert len(grid_info_2) == 2
        assert grid_info_2[1]['type'] == 'rectilinear'
        assert grid_info_2[1]['shape'] == (40, 106, 242)
        assert grid_info_2[1]['grid_spacing'] == (1.0, 1.0, 1.0)
        assert grid_info_2[1]['grid_origin'] == (0.0, 0.0, 0.0)
        assert len(grid_info_2[1]['grid_x']) == 242
        assert len(grid_info_2[1]['grid_y']) == 106
        assert len(grid_info_2[1]['grid_z']) == 40

    else:
        raise warnings.warn("Not able to get the test file. Skip test_get_grid_info()")


def test_get_var_info():
    test_file = 'example.nc'
    if os.path.isfile(test_file):
        roms_data = RomsData()
        var_info_1 = roms_data.get_var_info()
        assert var_info_1 is None

        roms_data.open(test_file)
        var_info_2 = roms_data.get_var_info()
        var = var_info_2['time-averaged salinity']
        assert var['var_name'] == 'salt'
        assert var['dtype'] == 'float64'
        assert var['itemsize'] == 8
        assert var['nbytes'] == 8208640
        assert var['units'] == 'N/A'
        assert var['location'] == 'node'
        assert var['grid_id'] == 1

    else:
        raise warnings.warn("Not able to get the test file. Skip test_get_var_info()")


def test_get_time_info():
    test_file = 'example.nc'
    if os.path.isfile(test_file):
        roms_data = RomsData()
        time_info_1 = roms_data.get_time_info()
        assert time_info_1 is None

        roms_data.open(test_file)
        time_info_2 = roms_data.get_time_info()

        assert time_info_2['start_time'] == 47436.0
        assert time_info_2['end_time'] == 47556.0
        assert time_info_2['time_step'] == 24
        assert time_info_2['total_steps'] == 6
        assert time_info_2['time_units'] == 'hours since 2017-11-01 00:00:00.000 UTC'
        assert time_info_2['calendar'] == 'proleptic_gregorian'
