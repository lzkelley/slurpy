"""Interact with the `sacct` SLURM command.
"""

import subprocess
from collections import OrderedDict
import numpy as np
import datetime

from . import utils
from slurpy.const import META_WIDTH, SACCT_KEYS, SEP_CHAR, STATE_KEYS


def sacct(state=None):
    """
    """
    lines, header = _parse_sacct()
    lines = _filter_lines(lines, header, state=state)
    utils.print_lines_dicts(lines, header)
    return


def summary(verbose=False, state=None):
    """Construct a summary of jobs described by the sacct command.
    """
    # Call `sacct`, parse results and filter output
    lines, header = _parse_sacct()
    lines = _filter_lines(lines, header, state=state)
    num_states = len(STATE_KEYS)
    # now = datetime.datetime.now()

    # Number of jobs in each state
    state_counts = np.zeros(num_states, dtype=int)
    # Duration of each job in each state
    durations = [[] for ii in range(num_states)]

    # Iterate over each job
    # ---------------------
    for ii, ll in enumerate(lines):
        # Find the state of this job
        state = ll['State']
        try:
            idx = STATE_KEYS.index(state)
        except:
            print("WARNING: state '{}' not in keys".format(state))
            continue

        state_counts[idx] += 1

        # Store the elapsed duration of time
        # Format: `[dd-]hh:mm:ss`
        elap = ll['Elapsed']
        try:
            # Look for days
            dd = elap.split('-')
            if len(dd) > 1:
                elap = dd[-1]
                dd = int(dd[0])
            else:
                dd = 0.0
            hh, mm, ss = [int(ee) for ee in elap.split(':')]
        except:
            print("sacct.summary(): Error - split failed on '{}'".format(elap))
            raise
        # Convert durations to hours and store
        dur = dd*24.0 + hh + mm/60.0 + ss/3600.0
        durations[idx].append(dur)

    # Report results
    for ss, cc, dd in zip(STATE_KEYS, state_counts, durations):
        # Number of jobs in each state
        print("\t'{}': {}".format(ss, cc))
        # If verbose is enabled
        if verbose:
            # min, max, and median elapsed time for each state.
            if len(dd):
                min, max, med = np.min(dd), np.max(dd), np.median(dd)
            else:
                min, max, med = 0.0, 0.0, 0.0
            print("\t\tmin: {:8.4f} [hr], max: {:8.4f} [hr], med: {:8.4f} [hr]".format(min, max, med))

    return


def _parse_sacct():
    """Call the `sacct` command and parse the output.
    """
    # Determine the keys to include in the sacct results (i.e. sacct output format)
    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    keys = ",".join(use_keys)

    # Get results from `sacct`
    command = ['sacct', '--format', keys]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()

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
        # skip blank lines (last one is blank)
        if not len(ll):
            continue
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
