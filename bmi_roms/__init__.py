from .utils import RomsData
from .bmi import BmiRoms
from .errors import RomsError, DataError
from ._version import get_versions

__all__ = ["RomsData",
           "BmiRoms",
           "DataError",
           "RomsError"
           ]

__version__ = get_versions()['version']
del get_versions
