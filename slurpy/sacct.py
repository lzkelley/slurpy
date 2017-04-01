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
import datetime
import numpy as np
import os
# import datetime

from . import utils
from . import const
from slurpy.const import META_WIDTH, SACCT_KEYS, STATE_KEYS


def sacct(args):
    """Call the 'sacct', parse and filter results and print to output.
    """
    args.log.debug("sacct.sacct()")
    lines, header = sacct_results(args)
    args.log.debug("Retrieved header and {} lines.".format(len(lines)))
    utils.print_lines_dicts(lines, header, args)
    return


def sacct_results(args):
    """Call 'sacct', parse and filter the results.
    """
    args.log.debug("sacct.sacct_results()")
    lines, header = _parse_sacct(args)
    # Filter out undesired lines
    lines = _filter_lines(lines, header, args)
    # Sort results
    _sort_lines(lines, header, args)
    return lines, header


def summary(args):
    """Construct a summary of jobs described by the sacct command.
    """
    args.log.debug("sacct.summary()")
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

    # If we are in 'watch' mode (with repeated output), then clear the screen before printing
    #    This should happen here to minimize the delay between clearing and printing
    if (args.watch is not None) and args.clear:
        os.system('cls' if os.name == 'nt' else 'clear')
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
    args.log.debug("sacct._parse_sacct()")
    command = _construct_sacct_command(args)
    # if args.verbose:
    #     print("Running: '{}'\n\t'{}'".format(command, " ".join(command)))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()

    # Parse results
    #   Convert from bytes to string
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


def _construct_sacct_command(args):
    """Construct the command (list of strings) to call 'sacct' (using `subprocess.Popen`).

    NOTE: currently `format` argument does nothing... make it do... something...
    """
    args.log.debug("sacct._construct_sacct_command()")
    # Determine the keys to include in the sacct results (i.e. sacct output format)
    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    keys = ",".join(use_keys)

    # Get results from `sacct`
    command = ['sacct', '--format', keys]

    if args.debug:
        print("command: '{}'".format(command))

    # Add starttime
    if args.start is not None:
        command.extend(['--starttime', args.start])
        if args.debug:
            print("command: '{}'".format(command))

    return command


def _parse_sacct_line(line, header):
    """Parse a single line of results from `sacct` with the given header.
    """
    num_keys = len(header)
    # Break up in 'sacct'-output line based on constant number-of-character sections for each key
    _comps = [line[ii*(META_WIDTH+1):(ii+1)*(META_WIDTH+1)][:-1] for ii in range(num_keys)]
    comps = OrderedDict()
    # Each line is a dict of key: value pairs, where the key is from the header line
    for key, _val in zip(header, _comps):
        val = _val.strip()
        if const.REFORMAT_TIMES and key in const.SACCT_KEYS_TIMES:
            match = const._REGEX_TIMES_PATTERN.match(val)
            if match is not None and len(match.groups()) == 2:
                val = const.REFORMAT_TIMES_SEP_CHAR.join(match.groups())
        comps[key] = val

    return comps


def _sort_lines(lines, header, args):
    """Sort the lines based on the `args.sort` parameter---matching one of the header keys.
    """
    args.log.debug("sacct._sort_lines()")
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
    lines.sort(key=lambda item: item[sort], reverse=rev)
    return None


def _filter_lines(lines, header, args):
    """Filter the given lines based on some parameter (e.g. state).
    """
    args.log.debug("sacct._filter_lines()")
    clean = list(lines)
    num = len(clean)
    args.log.debug("filtering from '{}' lines".format(num))

    # Remove 'extern' and 'batch' entries
    clean = [cc for cc in clean
             if not (cc['JobID'].endswith('extern') or cc['JobID'].endswith('batch'))]
    args.log.debug("{}/{} interesting lines".format(len(clean), num))

    def _log(cln, num, str):
        args.log.info("{}/{} {}".format(len(cln), num, str))

    # Filter by 'State'
    if args.state is not None:
        _num = len(clean)
        clean = _filter_by(clean, args.state, 'State', header)
        _log(clean, _num, "selecting for `State`")

    # Filter by 'Partition'
    if args.partition is not None:
        _num = len(clean)
        clean = _filter_by(clean, args.partition, 'Partition', header)
        _log(clean, _num, "selecting for `Partition`")

    # Filter by job name
    if args.name is not None:
        _num = len(clean)
        clean = _filter_by_name(clean, args.name, header)
        _log(clean, _num, "selecting for `JobName`")

    # Filter by job ID number
    if args.jobid is not None:
        _num = len(clean)
        clean = _filter_by_jobid(clean, args.jobid, header)
        _log(clean, _num, "selecting for `JobID`")

    # Filter by start-time
    if args.start is not None:
        _num = len(clean)
        clean = _filter_by_time(clean, args.start, header, args.log)
        _log(clean, _num, "selecting for `Start`")

    return clean


def _filter_by(line, var, key, header):
    if key in header:
        clean = [cc for cc in line if cc[key] == var]
        return clean

    print("WARNING: '{}' not in header: '{}'".format(key, header))
    return line


def _filter_by_jobid(lines, idstr, header):
    """Filter out lines with JobID numbers matching the input specification.

    Currently the `idstr` specification can be:
    - one or multiple ID numbers (comma or space separated)
    - An interval of ID numbers in the form `LO_ID : HI_ID` (spaces are optional).

    Arguments
    ---------
    lines : (N,) list of dict
    idstr : str
        Specification of which ID numbers to include.
    header : dict

    Returns
    -------
    clean : (M,) list of dict

    """
    _ids = " ".join(idstr)

    # Parse the specification string for which jobID numbers to include
    id_list = None
    id_lo = None
    id_hi = None

    # Look for a range of values using ':', e.g. `84513996 : 84514000`
    _ids = [ss.strip() for ss in _ids.split(':')]
    if len(_ids) == 2:
        id_lo = int(_ids[0])
        id_hi = int(_ids[1])
        # print("id_lo : '{}'".format(id_lo))
        # print("id_hi : '{}'".format(id_hi))
    elif len(_ids) == 1:
        id_list = [tt for ss in _ids[0].split() for tt in ss.split(',')]
        # Clean up each element and remove empty ones
        id_list = [tt.strip() for tt in id_list if len(tt.strip()) > 0]
        # print("id_list : '{}'".format(id_list))
    else:
        raise ValueError("Could not parse input jobids '{}'".format(idstr))

    clean = [nn for nn in lines if (id_list is None) or (nn['JobID'] in id_list)]
    clean = [nn for nn in clean if (id_lo is None) or (int(nn['JobID']) >= id_lo)]
    clean = [nn for nn in clean if (id_hi is None) or (int(nn['JobID']) <= id_hi)]
    return clean


def _filter_by_name(lines, name, header):
    if name is None:
        return lines
    clean = [nn for nn in lines if name in nn['JobName']]
    return clean


def _filter_by_time(lines, start, header, log):
    log.debug("sacct._filter_by_time()")

    if start is None:
        log.debug("`start` is None, returning all")
        return lines

    # If it looks like there are times included
    if len(start.split(" ")) == 2:
        form = "%Y-%m-%d %H:%M:%S"
    elif len(start.split("T")) == 2:
        form = "%Y-%m-%dT%H:%M:%S"
    else:
        form = "%Y-%m-%d"

    try:
        dt = datetime.datetime.strptime(start, form)
        log.debug("`start` = '{}' ==> `dt` = '{}'".format(start, dt))
    except:
        log.error("Could not format `start`='{}', with `form`='{}'".format(start, form))
        return lines

    clean = [nn for nn in lines
             if datetime.datetime.strptime(nn['Start'], "%Y-%m-%d %H:%M:%S") > dt]
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
