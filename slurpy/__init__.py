"""slurpy: python wrapper for SLURM.
"""
import os
_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_VERSION_PATH = os.path.join(_ROOT_PATH, 'VERSION')


def _get_root_path():
    return str(_ROOT_PATH)

__version__ = open(_VERSION_PATH).read().strip()
__author__ = "Luke Zoltan Kelley"
__email__ = "lkelley@cfa.harvard.edu"
__status__ = "Development"
