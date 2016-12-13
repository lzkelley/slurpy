"""Interact with the `sacct` SLURM command.
"""
import subprocess
from collections import OrderedDict
import numpy as np

from slurpy.const import META_WIDTH, SACCT_KEYS, SEP_CHAR


def sacct(state):

    lines, header = _parse_sacct()
    lines = _filter_lines(lines, header, state=state)
    _print_lines_dicts(lines, header)

    return


def _parse_sacct():
    """Call the `sacct` command and parse the output.
    """
    # Determine the keys to include in the sacct results (i.e. sacct output format)
    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    # num_keys = len(use_keys)
    keys = ",".join(use_keys)
    # print("Keys: {} - {}".format(num_keys, keys))

    # Get results from `sacct`
    command = ['sacct', '--format', keys]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    # retcode = p.wait()
    # p.wait()

    # Parse results
    # Convert from bytes to string
    raw_lines = text.decode('ascii')
    raw_lines = raw_lines.split('\n')
    header = raw_lines.pop(0)
    header = header.split()

    # Remove the separation line between header and content
    raw_lines = raw_lines[1:]
    lines = []
    for ii, ll in enumerate(raw_lines):
        comps = _parse_sacct_line(ll, header)
        lines.append(comps)

    return lines, header


def _parse_sacct_line(line, header):
    """Parse a single line of results from `sacct` with the given header.
    """
    num_keys = len(header)
    _comps = [line[ii*(META_WIDTH+1):(ii+1)*(META_WIDTH+1)][:-1] for ii in range(num_keys)]
    comps = OrderedDict()
    for key, val in zip(header, _comps):
        comps[key] = val.strip()

    return comps


def _print_lines_dicts(lines, header):
    """Print each line (containing a dict) of `sacct` results.  Format nicely.
    """
    num_keys = len(header)
    # Find the maximum length of each component of each line
    sizes = np.zeros(num_keys, dtype=int)
    for ll in lines:
        for ii, (key, val) in enumerate(ll.items()):
            sizes[ii] = np.maximum(sizes[ii], len(val))

    # pretty print lines
    form = SEP_CHAR.join("{{:>{sz}s}}".format(sz=ss) for ss in sizes)
    print(form.format(*header))
    for ll in lines:
        print(form.format(*ll.values()))

    return


def _filter_lines(lines, header, state=None):
    """Filter the given lines based on some parameter (e.g. state).
    """
    clean = list(lines)
    # Remove 'extern' and 'batch' entries
    clean = [cc for cc in clean
             if not (cc['JobID'].endswith('extern') or cc['JobID'].endswith('batch'))]

    # Make sure filter parameters are included in header
    if state is not None:
        if 'State' not in header:
            print("WARNING: 'State' not in header: '{}'".format(header))
            return clean

        clean = [cc for cc in clean if cc['State'] == state]

    return clean
