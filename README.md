# bmi_roms
[![Documentation Status](https://readthedocs.org/projects/bmi_era5/badge/?version=latest)](https://bmi_era5.readthedocs.io/en/latest/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gantian127/bmi_era5/blob/master/LICENSE.txt)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gantian127/bmi_era5/master?filepath=notebooks%2Fbmi_era5.ipynb)


bmi_roms package is an implementation of the Basic Model Interface ([BMI](https://bmi-spec.readthedocs.io/en/latest/)) for
the [ROMS model](https://confluence.ecmwf.int/display/CKB/ERA5) datasets. This package wraps the dataset with BMI for 
data control and query. This package is not implemented for people to use but is the key element to convert the ROMS dataset into 
a data component ([pymt_roms](https://pymt-era5.readthedocs.io/)) for 
the [PyMT](https://pymt.readthedocs.io/en/latest/?badge=latest) modeling framework developed 
by Community Surface Dynamics Modeling System ([CSDMS](https://csdms.colorado.edu/wiki/Main_Page)). 
 
If you have any suggestion to improve the current function, please create a github issue 
[here](https://github.com/gantian127/bmi_roms/issues).

## Get Started

#### Install package

##### Stable Release

The bmi_roms package and its dependencies can be installed with pip
```
$ pip install bmi_roms
```

or conda
```
$ conda install -c conda-forge bmi_roms 
```

##### From Source

After downloading the source code, run the following command from top-level folder 
(the one that contains setup.py) to install bmi_roms.
```
$ pip install -e .
```

#### Demonstration of how to use BmiRoms

Learn more details from the [tutorial notebook](https://github.com/gantian127/bmi_roms/blob/master/notebooks/bmi_roms.ipynb) 
provided in this package.

```python
from bmi_roms import BmiRoms
import numpy as np
import matplotlib.pyplot as plt

data_comp = BmiRoms()
data_comp.initialize('config_file.yaml')

# get variable info
for var_name in  data_comp.get_output_var_names():
    var_unit = data_comp.get_var_units(var_name)
    var_location = data_comp.get_var_location(var_name)
    var_type = data_comp.get_var_type(var_name)
    var_grid = data_comp.get_var_grid(var_name)
    var_itemsize = data_comp.get_var_itemsize(var_name)
    var_nbytes = data_comp.get_var_nbytes(var_name)
    
    print('variable_name: {} \nvar_unit: {} \nvar_location: {} \nvar_type: {} \nvar_grid: {} \nvar_itemsize: {}' 
            '\nvar_nbytes: {} \n'. format(var_name, var_unit, var_location, var_type, var_grid, var_itemsize, var_nbytes))

# get time info
start_time = data_comp.get_start_time()
end_time = data_comp.get_end_time()
time_step = data_comp.get_time_step()
time_unit = data_comp.get_time_units()
time_steps = int((end_time - start_time)/time_step) + 1
print('start_time:{} \nend_time:{} \ntime_step:{} \ntime_unit:{} \ntime_steps:{} \n'.format(
    start_time, end_time, time_step, time_unit, time_steps))

# get grid info 
for var_name in data_comp.get_output_var_names():
    var_grid = data_comp.get_var_grid(var_name)
    
    grid_rank = data_comp.get_grid_rank(var_grid) 
    grid_size = data_comp.get_grid_size(var_grid)
    
    grid_shape = np.empty(grid_rank, int)
    data_comp.get_grid_shape(var_grid, grid_shape)
    
    grid_spacing = np.empty(grid_rank)
    data_comp.get_grid_spacing(var_grid, grid_spacing)
    
    grid_origin = np.empty(grid_rank)
    data_comp.get_grid_origin(var_grid, grid_origin)
    
    print('grid_id: {}\ngrid_rank: {} \ngrid_size: {} \ngrid_shape: {} \ngrid_spacing: {} \ngrid_origin: {} \n'.format(
        var_grid, grid_rank, grid_size, grid_shape, grid_spacing, grid_origin))

# get variable data
data = np.empty(grid_size, var_type)
data_comp.get_value(var_name, data)
data_2D = data.reshape(grid_shape) if grid_rank ==2 else data.reshape(grid_shape)[0]

# plot data
plt.figure(figsize=(12,4))
im = plt.imshow(data_2D, origin='lower')
cbar = plt.colorbar(im)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('ROMS model data of {}'.format(var_name))
```

![plot](docs/source/_static/plot.png)





