"""Interact with the `sacct` SLURM command.
"""
import subprocess
from collections import OrderedDict
import numpy as np

from slurpy.const import META_WIDTH, SACCT_KEYS


def sacct(status):

    lines, header = _parse_sacct()
    _print_lines_dicts(lines, header)

    return



    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    keys = ",".join(use_keys)

    command = ['sacct', '--format', keys]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    retcode = p.wait()
    # print("retcode = ", retcode)

    lines = text.split('\n')
    header = lines.pop(0)
    lines = lines[1:]
    for ii, ll in enumerate(lines):
        # print(ii, ll)
        parts = ll.split()
        if 'extern' in parts or 'batch' in parts:
            continue
        # nice_parts = "{:4d}: ".format(ii) + ", ".join('{1:{0:}}'.format(PRINT_WIDTH, pp.strip()) for pp in parts)
        nice_parts = "{:4d}: ".format(ii) + ", ".join('{}'.format(pp.strip()) for pp in parts)
        if status is None or status in parts:
            print(nice_parts)

    return


def _parse_sacct():
    """Call the `sacct` command and parse the output.
    """
    # Determine the keys to include in the sacct results (i.e. sacct output format)
    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    num_keys = len(use_keys)
    keys = ",".join(use_keys)
    print("Keys: {} - {}".format(num_keys, keys))

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
    """
    """
    num_keys = len(header)
    # Find the maximum length of each component of each line
    sizes = np.zeros(num_keys, dtype=int)
    for ll in lines:
        for ii, (key, val) in enumerate(ll.items()):
            sizes[ii] = np.maximum(sizes[ii], len(val))


    # pretty print lines
    for ll in lines:
        form = " ".join("{:{{sz}}>s}".format(sz=ss) for ss in sizes)
        print(form)

    return
