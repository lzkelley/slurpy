"""General purpose utility functions.

Functions
---------
-   print_lines_dicts        - Print each line of `sacct` results.  Format nicely.
-   prompt_yes_no            - Prompt a yes/no question via input() and return their answer.

-   _format_line             -
-   _calculate_formatting    -


"""
import numpy as np

from . const import SEP_CHAR


def print_lines_dicts(lines, header):
    """Print each line (containing a dict) of `sacct` results.  Format nicely.
    """
    # If there are no selected lines, return
    if not len(lines):
        return

    form = _calculate_formatting(lines, header)

    # Print header
    print(form.format(*header))
    # Print each line
    for ll in lines:
        pstr = _format_line(ll, form)
        print(pstr)

    return


def _filter_fields_in_lines(lines, header, keys=None):
    if keys is None:
        return lines

    return clean


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
    form = SEP_CHAR.join("{{: >{sz}s}}".format(sz=ss) for ss in sizes)
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
