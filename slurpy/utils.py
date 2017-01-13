"""General purpose utility functions.
"""
import numpy as np

from . const import SEP_CHAR


def print_lines_dicts(lines, header):
    """Print each line (containing a dict) of `sacct` results.  Format nicely.
    """
    # If there are no selected lines, return
    if not len(lines):
        return

    num_keys = len(header)
    # Find the maximum length of each component of each line
    #    Start with the size of the header values
    sizes = [len(hh) for hh in header]
    for ll in lines:
        for ii, (key, val) in enumerate(ll.items()):
            sizes[ii] = np.maximum(sizes[ii], len(val))

    # Create nice formatting string
    form = SEP_CHAR.join("{{: >{sz}s}}".format(sz=ss) for ss in sizes)
    # Print header
    print(form.format(*header))
    # Print each line
    for ll in lines:
        # print(len(ll), num_keys)
        print(form.format(*ll.values()))

    return
