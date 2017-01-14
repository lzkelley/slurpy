"""Cancel submitted jobs using the 'scancel' SLURM command.
"""

import subprocess
from collections import OrderedDict
import numpy as np
import datetime

from . import utils
from . import sacct
# from slurpy.const import META_WIDTH, SACCT_KEYS, SEP_CHAR, STATE_KEYS


def scancel(args):
    """Cancel submitted jobs.
    """
    # Get filtered job information
    lines, header = sacct.sacct_results(args)
    utils.print_lines_dicts(lines, header)

    # Extract JobID numbers
    jids = [jj['JobID'] for jj in lines]

    return
