"""General purpose utility functions.

Functions
---------
-   print_lines_dicts        -

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
