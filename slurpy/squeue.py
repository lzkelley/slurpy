"""Methods for interacting with the SLURM `squeue` command.
"""

import subprocess
from collections import OrderedDict
import numpy as np
import datetime

from . import utils
from slurpy.const import META_WIDTH, SQUEUE_KEYS, SEP_CHAR, STATE_KEYS


def squeue(queue=None):
    lines, header = _parse_squeue()
    # lines = _filter_lines(lines, header, state=state)
    utils.print_lines_dicts(lines, header)
    return


def _parse_squeue():
    """Call the `squeue` command and parse the output.
    """
    # Determine the keys to include in the sacct results (i.e. sacct output format)
    use_keys = [kk + ":{}".format(META_WIDTH) for kk in SQUEUE_KEYS]
    # num_keys = len(use_keys)
    keys = "\"" + ",".join(use_keys) + "\""
    # keys = "username,jobid,name,timeleft"
    # print("'{}'".format(keys))
    # print("Keys: {} - {}".format(num_keys, keys))

    # Get results from `sacct`
    # _com = "squeue"
    _com = "/usr/bin/squeue"
    command = [_com, '--Format=' + keys]
    # command = command[0] + " " + command[1] + command[2]
    # command = "/usr/bin/squeue"
    print("Calling:\n", command, "\n")
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    # print(text)
    retcode = p.wait()
    if retcode:
        print("retcode = '{}'".format(retcode))

    # Parse results
    # Convert from bytes to string
    raw_lines = text.decode('ascii')
    raw_lines = raw_lines.split('\n')
    header = raw_lines.pop(0)
    header = header.split()
    print("header:\n", header)
    print()

    # Remove the separation line between header and content
    raw_lines = raw_lines[1:]
    lines = []
    for ii, ll in enumerate(raw_lines):
        # skip blank lines (last one is blank)
        if not len(ll):
            continue
        comps = _parse_squeue_line(ll, header)
        lines.append(comps)

    return lines, header


def _parse_squeue_line(line, header):
    """Parse a single line of results from `sacct` with the given header.
    """
    num_keys = len(header)
    _comps = [line[ii*(META_WIDTH+1):(ii+1)*(META_WIDTH+1)][:-1] for ii in range(num_keys)]
    comps = OrderedDict()
    for key, val in zip(header, _comps):
        comps[key] = val.strip()

    return comps
