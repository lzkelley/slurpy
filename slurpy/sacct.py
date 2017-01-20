"""Interact with the `sacct` SLURM command.

Functions
---------
-   sacct                 -
-   sacct_results         -
-   summary               -


-   _parse_sacct          -
-   _parse_sacct_line     -
-   _filter_lines         -
-   _filter_by            -
-   _parse_state_value    - Retrieve the index corresponding to the given state.
"""

import subprocess
from collections import OrderedDict
import numpy as np
import datetime

from . import utils
from slurpy.const import META_WIDTH, SACCT_KEYS, SEP_CHAR, STATE_KEYS


def sacct(args):
    """Call the 'sacct', parse and filter results and print to output.
    """
    lines, header = sacct_results(args)
    utils.print_lines_dicts(lines, header, args)
    return


def sacct_results(args):
    """Call 'sacct', parse and filter the results.
    """
    lines, header = _parse_sacct(args)
    # Filter out undesired lines
    lines = _filter_lines(lines, header, state=args.state, partition=args.partition, name=args.name)
    # Sort results
    _sort_lines(lines, header, args)
    return lines, header


def summary(args):
    """Construct a summary of jobs described by the sacct command.
    """
    verbose = args.verbose
    # Call `sacct`, parse results and filter output
    lines, header = sacct_results(args)
    num_states = len(STATE_KEYS)

    # Number of jobs in each state
    state_counts = np.zeros(num_states, dtype=int)
    # Duration of each job in each state
    durations = [[] for ii in range(num_states)]

    # Iterate over each job
    # ---------------------
    for ii, ll in enumerate(lines):
        # Find the state of this job
        state, idx = _parse_state_value(ll['State'])
        # If 'state' is unrecognized, 'None' is returned; skip
        if state is None:
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


def _parse_sacct(args):
    """Call the `sacct` command and parse the output.
    """
    command = _construct_sacct_command()
    # if args.verbose:
    #     print("Running: '{}'\n\t'{}'".format(command, " ".join(command)))
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


def _construct_sacct_command(format=None, starttime=None):
    """Construct the command (list of strings) to call 'sacct' (using `subprocess.Popen`).

    NOTE: currently 'format' does nothing... make it do... something...
    """
    # Determine the keys to include in the sacct results (i.e. sacct output format)
    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    keys = ",".join(use_keys)

    # Get results from `sacct`
    command = ['sacct', '--format', keys]
    return command


def _parse_sacct_line(line, header):
    """Parse a single line of results from `sacct` with the given header.
    """
    num_keys = len(header)
    # Break up in 'sacct'-output line based on constant number-of-character sections for each key
    _comps = [line[ii*(META_WIDTH+1):(ii+1)*(META_WIDTH+1)][:-1] for ii in range(num_keys)]
    comps = OrderedDict()
    # Each line is a dict of key: value pairs, where the key is from the header line
    for key, val in zip(header, _comps):
        comps[key] = val.strip()

    return comps


def _sort_lines(lines, header, args):
    """Sort the lines based on the `args.sort` parameter---matching one of the header keys.
    """
    # No sort parameter, do not sort
    if args.sort is None:
        return lines

    sort = args.sort
    rev = False
    # If the sort parameter starts with '-', then reverse the sorting order
    if sort.startswith('-'):
        rev = True
        sort = sort[1:]

    # Sort each line by the target key
    lines.sort(key=lambda item:item[sort], reverse=rev)
    return None

def _filter_lines(lines, header, state=None, partition=None, name=None):
    """Filter the given lines based on some parameter (e.g. state).
    """
    clean = list(lines)
    # Remove 'extern' and 'batch' entries
    clean = [cc for cc in clean
             if not (cc['JobID'].endswith('extern') or cc['JobID'].endswith('batch'))]

    # Filter by 'State'
    clean = _filter_by(clean, state, 'State', header)
    # Filter by 'Partition'
    clean = _filter_by(clean, partition, 'Partition', header)

    # Filter by job name
    if name is not None:
        clean = _filter_by_name(clean, name, header)

    return clean


def _filter_by(line, var, key, header):
    # If the filtering parameter is given (not None), and the key is in the header
    if var is None:
        return line

    if key in header:
        clean = [cc for cc in line if cc[key] == var]
        return clean

    print("WARNING: '{}' not in header: '{}'".format(key, header))
    return line


def _filter_by_name(lines, name, header):
    if name is None:
        return lines
    clean = [nn for nn in lines if name in nn['JobName']]
    return clean


def _parse_state_value(state):
    """Retrieve the index corresponding to the given state (as returned by 'sacct').

    The 'CANCELLED' state needs special filtering.
    """

    # Handle 'CANCELLED' specially
    #    e.g. 'CANCELLED by 56895'
    if state.lower().startswith('cancelled'):
        state = state.split(' by ')[0]

    try:
        idx = STATE_KEYS.index(state)
    except:
        print("WARNING: state '{}' not in keys".format(state))
        return None, None

    return state, idx
