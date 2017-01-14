# Change-Log for slurpy
# =====================


## To-Do
## -----
-   Add a builtin 'watch' sub-command, to continually re-quiery every N seconds.
-   Look at older history with `sacct --starttime`
-   Add tests.
 

## Current
## -------
-   Added 'CANCELLED' and 'TIMEOUT' states.
-   Added `--verbose` command-line argument to modify results.
-   Added `--summary` command-line argument to summarize all jobs reported by 'sacct'.  Currently returns the counts and optionally the min, max, median elapsed time for each state (if the `--verbose` flag is passed).
-   Added `-p`/`--partition` argument to select a particular partition of the cluster.
-   Added `--cancel` command, to cancel submitted jobs.

-  `setup.py`
    -   Added console entry point to setup script, (and appropriately modified `setup.sh`) to install `slurpy` as a script which is runnable from anywhere via the command line.  Working.
-   `slurpy/__main__.py`
    -   
-   `slurpy/sacct.py`
    -   `summary()` [new-method]
        -   API method to parse 'sacct' command results and summarize succinctly.
        -   Reports number of jobs in each 'state'
        -   If `verbose`, then reports min, max, median elapsed time for each state.
-   `slurpy/utils.py` [new-file]
    -   File for general purpose utility methods.  Currently empty.
    -   `print_lines_dicts()` [new-method]
        -   Method for pretty-printing lines retrieved from 'sacct'.


## v0.1 - 2016/12/13
## -----------------
-   `slurpy/__main__.py`
    -   Primary entry point for the `slurpy` package.  Currently just calls the `sacct.sacct()` method.  In the future will use subcommands (and arguments) to determine which specific functions to delegate to.
-   `slurpy/const.py`
    -   File to contain constants and parameters.
-   `slurpy/sacct.py`
    -   File to handle interactions with the 'sacct' command.
    -   `sacct()`
        -   API Method to call and report from the SLURM 'sacct' command.
    -   Includes methods to parse sacct results (`_parse_sacct` and `_parse_sacct_line`), filter the resulting lines based on 'state' (`_filter_lines`) and nicely format the results for printing (`_print_lines_dicts`).
