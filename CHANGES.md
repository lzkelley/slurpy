Change-Log for slurpy
=====================


# Current
# -------


# v0.1 - 2016/12/13
# -----------------
-   `slurpy/__main__.py`
    -   Primary entry point for the `slurpy` package.  Currently just calls the `sacct.sacct()` method.  In the future will use subcommands (and arguments) to determine which specific functions to delegate to.
-   `slurpy/const.py`
    -   File to contain constants and parameters.
-   `slurpy/sacct.py`
    -   File to handle interactions with the `sacct` command.
    -   `sacct()`
        -   API Method to call and report from the SLURM 'sacct' command.
    -   Includes methods to parse sacct results (`_parse_sacct` and `_parse_sacct_line`), filter the resulting lines based on 'state' (`_filter_lines`) and nicely format the results for printing (`_print_lines_dicts`).
