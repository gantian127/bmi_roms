```{image} _static/logo.png
:align: center
:alt: bmi_roms
:scale: 16%
:target: https://bmi-roms.readthedocs.io/en/latest/
```

[bmi_roms][bmi_roms-github] package is an implementation of the
[Basic Model Interface (BMI)][bmi-docs] for the [ROMS model][roms_model] datasets.
This package wraps the dataset with BMI for data control and query.
This package is not implemented for people to use but is the key element to convert
the ROMS dataset into a data component [pymt_roms][pymt_roms] for
the [PyMT][pymt-docs] modeling framework developed by Community Surface Dynamics
Modeling System ([CSDMS][csdms]).

The current implementation supports 2D, 3D and 4D ROMS output datasets defined with geospatial and/or time dimensions
(e.g., dataset defined with dimensions as [time, s_rho, eta_rho, xi_rho])

# Installation

**Stable Release**

The bmi_roms package and its dependencies can be installed with either *pip* or *conda*,

````{tab} pip
```console
pip install bmi_roms
```
````

````{tab} conda
```console
conda install -c conda-forge bmi_roms
```
````

**From Source**

After downloading the source code, run the following command from top-level folder
to install bmi_roms.

```console
pip install -e .
```

# Quick Start

You can learn more details from the [tutorial notebook][bmi_roms-notebook].

```python
from bmi_roms import BmiRoms
import numpy as np
import matplotlib.pyplot as plt

data_comp = BmiRoms()
data_comp.initialize("config_file.yaml")

# get variable info
for var_name in data_comp.get_output_var_names():
    var_unit = data_comp.get_var_units(var_name)
    var_location = data_comp.get_var_location(var_name)
    var_type = data_comp.get_var_type(var_name)
    var_grid = data_comp.get_var_grid(var_name)
    var_itemsize = data_comp.get_var_itemsize(var_name)
    var_nbytes = data_comp.get_var_nbytes(var_name)
    print(
        f"{var_name=} \n{var_unit=} \n{var_location=} \n{var_type=} \n{var_grid=}"
        f"\n{var_itemsize=} \n{var_nbytes=} \n"
    )

# get time info
start_time = data_comp.get_start_time()
end_time = data_comp.get_end_time()
time_step = data_comp.get_time_step()
time_unit = data_comp.get_time_units()
time_steps = int((end_time - start_time) / time_step) + 1
print(f"{start_time=} \n{end_time=} \n{time_step=} \n{time_unit=} \n{time_steps=} \n")

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

    print(
        f"{var_name=} \n{var_grid=} \n{grid_rank=} \n{grid_size=} \n{grid_shape=}"
        f"\n{grid_spacing=} \n{grid_origin=} \n"
    )

# get variable data
data = np.empty(1026080, "float64")
data_comp.get_value("time-averaged salinity", data)
data_3D = data.reshape([40, 106, 242])

# get lon and lat data
lat = np.empty(25652, "float64")
data_comp.get_value("latitude of RHO-points", lat)

lon = np.empty(25652, "float64")
data_comp.get_value("longitude of RHO-points", lon)

# make a contour plot
fig = plt.figure(figsize=(10, 7))
im = plt.contourf(
    lon.reshape([106, 242]), lat.reshape([106, 242]), data_3D[0], levels=36
)
fig.colorbar(im)
plt.axis("equal")
plt.xlabel("Longitude [degree_east]")
plt.ylabel("Latitude [degree_north]")
plt.title("ROMS model data of time-averaged salinity")

# finalize the data component
data_comp.finalize()
```

```{image} _static/contour_plot.png
```

# Parameter settings

A [configuration file][config_file] is required to initialize an instance of the ROMS
data component. This file includes the following parameters:

* **filename**: Path or URL (e.g., OPeNDAP data url) of the ROMS model data to open.
* **download**: Bool value as True or False to indicate whether to download and save
  the data as a netCDF file with the provided URL. The dataset will be saved in the
  working directory with a file name including the time information (e.g.,
  romsdata_12032023T162045.nc)

<!-- links -->
[bmi-docs]: https://bmi.readthedocs.io
[csdms]: https://csdms.colorado.edu
[config_file]: https://github.com/gantian127/bmi_roms/blob/master/notebooks/config_file.yaml
[roms_model]: https://www.myroms.org/
[pymt-docs]: https://pymt.readthedocs.io
[bmi_roms-github]: https://github.com/gantian127/bmi_roms/
[bmi_roms-notebook]: https://github.com/gantian127/bmi_roms/blob/master/notebooks/bmi_roms.ipynb
[pymt_roms]: https://pymt-roms.readthedocs.io/
