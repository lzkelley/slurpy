"""General purpose utility functions.

Functions
---------
-   print_lines_dicts        - Print each line of `sacct` results.  Format nicely.
-   prompt_yes_no            - Prompt a yes/no question via input() and return their answer.

-   _format_line             -
-   _calculate_formatting    -


"""
import numpy as np
from collections import OrderedDict

from . import const
# from . const import SEP_CHAR


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

    # Calculate the proper formatting specification string
    form = _calculate_formatting(lines, header)

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

    num_keys = len(header)
    # Find the maximum length of each component of each line
    #    Start with the size of the header values
    sizes = [len(hh) for hh in header]
    for ll in lines:
        for ii, (key, val) in enumerate(ll.items()):
            sizes[ii] = np.maximum(sizes[ii], len(val))

    # Create nice formatting string
    form = const.SEP_CHAR.join("{{: >{sz}s}}".format(sz=ss) for ss in sizes)
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
