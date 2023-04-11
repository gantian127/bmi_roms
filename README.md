# bmi_roms
[![Documentation Status](https://readthedocs.org/projects/bmi_roms/badge/?version=latest)](https://bmi_roms.readthedocs.io/en/latest/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gantian127/bmi_roms/blob/master/LICENSE.txt)


bmi_roms package is an implementation of the Basic Model Interface ([BMI](https://bmi-spec.readthedocs.io/en/latest/)) for
the [ROMS model](https://www.myroms.org/) datasets. This package wraps the dataset with BMI for 
data control and query. This package is not implemented for people to use but is the key element to convert the ROMS dataset into 
a data component ([pymt_roms](https://pymt-roms.readthedocs.io/)) for 
the [PyMT](https://pymt.readthedocs.io/en/latest/?badge=latest) modeling framework developed 
by Community Surface Dynamics Modeling System ([CSDMS](https://csdms.colorado.edu/wiki/Main_Page)). 

The current implementation supports 2D, 3D and 4D ROMS output datasets defined with geospatial and/or time dimensions 
(e.g., dataset defined with dimensions as [time, s_rho, eta_rho, xi_rho])

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

# get variable grid info 
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
    
    print('var_name: {} \ngrid_id: {}\ngrid_rank: {} \ngrid_size: {} \ngrid_shape: {} \ngrid_spacing: {} \ngrid_origin: {} \n'.format(
        var_name, var_grid, grid_rank, grid_size, grid_shape, grid_spacing, grid_origin))

# get variable data 
data = np.empty(1026080, 'float64')
data_comp.get_value('time-averaged salinity', data)
data_3D = data.reshape([40, 106, 242])

# get lon and lat data
lat = np.empty(25652, 'float64')
data_comp.get_value('latitude of RHO-points', lat)

lon = np.empty(25652, 'float64')
data_comp.get_value('longitude of RHO-points', lon)

# make a contour plot
fig = plt.figure(figsize=(10,7))
im = plt.contourf(lon.reshape([106, 242]), lat.reshape([106, 242]), data_3D[0], levels=36)
fig.colorbar(im)
plt.axis('equal')
plt.xlabel('Longitude [degree_east]')
plt.ylabel('Latitude [degree_north]')
plt.title('ROMS model data of time-averaged salinity')
```

![plot](docs/source/_static/plot.png)





