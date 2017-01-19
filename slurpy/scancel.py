"""Cancel submitted jobs using the 'scancel' SLURM command.

Functions
---------
-   scancel           - Cancel submitted jobs.

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
    # utils.print_lines_dicts(lines, header, args)

    # Extract JobID numbers
    jids = [jj['JobID'] for jj in lines]

    form = utils._calculate_formatting(lines, header)
    for ii, (jj, ll) in enumerate(zip(jids, lines)):
        # print(ii, jj, utils._format_line(ll, form))
        command = ['scancel', jj]
        print("Cancelling job '{}' - '{}'".format(jj, ll['JobName']))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # decome from bytes to strings
        text = p.stdout.read().decode('ascii')
        if text:
            print("\tRecieved: '{}'".format(text))
        # break

    return
