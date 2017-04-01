"""General purpose utility functions.

Functions
---------
-   print_lines_dicts        - Print each line of `sacct` results.  Format nicely.
-   prompt_yes_no            - Prompt a yes/no question via input() and return their answer.

-   _format_line             -
-   _calculate_formatting    -


"""
import os
import numpy as np
import logging
from collections import OrderedDict

from zcode import inout as zio

from . import const


def print_lines_dicts(_lines, _header, args):
    """Print each line (containing a dict) of `sacct` results.  Format nicely.
    """
    # If there are no selected lines, return
    if not len(_lines):
        return

    # Filter out which keys are printed
    # ---------------------------------
    # If verbose print all keys (`keys = None`)
    if args.verbose:
        keys = None
    else:
        keys = const.SACCT_KEYS_PRINT
    lines, header = _filter_fields_in_lines(_lines, _header, keys=keys)

    # Only include the first/last some-number of lines
    if args.head is not None or args.tail is not None:
        hh = int(args.head) if (args.head is not None) else None
        tt = int(args.tail) if (args.tail is not None) else None
        num_lines = len(lines)
        lines = [ll for ii, ll in enumerate(lines)
                 if ((hh is None or ii < hh) or
                     (tt is None or ii >= num_lines - tt))]

    # Calculate the proper formatting specification string
    form = _calculate_formatting(lines, header)

    # If we are in 'watch' mode (with repeated output), then clear the screen before printing
    #    This should happen here to minimize the delay between clearing and printing
    if (args.watch is not None) and args.clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    # Print header
    print(form.format(*header))
    # Print each line
    for ll in lines:
        pstr = _format_line(ll, form)
        print(pstr)

    return


def _filter_fields_in_lines(lines, header, keys=None):
    """Select only the desired `keys` from the given header and each line of lines.
    """
    if keys is None:
        return lines, header

    # Find which elements of `header` are desired (i.e. in keys)
    clean_header = [hh for hh in header if hh in keys]
    if len(clean_header) == 0:
        raise ValueError("None of the header values ('{}') are targeted in keys ('{}')".format(
            header, keys))

    # Create a new list of dict including only the target keys of each line
    clean_lines = [OrderedDict((hh, ll[hh]) for hh in clean_header)
                   for ll in lines]
    return clean_lines, clean_header


def _format_line(line, form):
    return form.format(*line.values())


def _calculate_formatting(lines, header):
    """Construct an appropriately formatted string to print lines.
    """
    lines = np.atleast_1d(lines)

    # Find the maximum length of each component of each line
    #    Start with the size of the header values
    sizes = [len(hh) for hh in header]
    for ll in lines:
        for ii, (key, val) in enumerate(ll.items()):
            sizes[ii] = np.maximum(sizes[ii], len(val))

    # Create nice formatting string
    sep = const.SEP_CHAR + " "*const.COLUMN_SPACING
    form = sep.join("{{: >{sz}s}}".format(sz=ss) for ss in sizes)
    return form


def prompt_yes_no(question, default="no"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    From: http://code.activestate.com/recipes/577058/
    """
    import sys
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '{}'".format(default))

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def init_log(args):
    """Initialize a `logging.Logger` object for general output.

    Arguments
    ---------
    args : argparse arguments
        Input arguments, determines the logging level based on `args.debug` and `args.verbose`.

    Returns
    -------
    log : `logging.Logger`
        Logging instance.

    """
    # Determine output level for stream-log
    if args.debug:
        str_lvl = logging.DEBUG
    elif args.verbose:
        str_lvl = logging.INFO
    else:
        str_lvl = logging.WARNING

    log = zio.get_logger(
        'slurpy_log', level_stream=str_lvl, level_file=None, tofile=None, tostr=True)
    return log
