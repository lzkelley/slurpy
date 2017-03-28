# Change-Log for slurpy
# =====================


## To-Do
## -----
-   Add a builtin 'watch' sub-command, to continually re-quiery every N seconds.
-   Look at older history with `sacct --starttime`
-   Add tests.
-   Change '--cancel' to 'cancel' subcommand.
-   Finish developing '--queue' argument.
-   Filter jobs by submission time, or job ID number
-   Make filter arguments accept lists (e.g. for name or state)


## Current
## -------
-   Added `--name` argument, 'sacct' results now filtered by job-name.
    -   Currently uses only a case-sensitive check, using 'in' (i.e. if the filtering parameter is inside the job-name, then it passes the check).
-   Added `--sort` argument to sort 'sacct' results by the given field.
    -   New method `sacct._sort_lines()` does this, called from `sacct.sacct_results()`.
-   Added `--id` argument to filter by 'JobID' number.  Also works for canceling jobs.
    -   New method `sacct._filter_by_jobid()` does the filtering by parsing the command-line argument specification string.  This is called by `sacct._filter_lines()`.
-   By default, reformat the times-strings output by sacct (replace 'T' separator with optional alternative character.  Set by parameters in `const.py`, with code in `sacct._parse_sacct_line()`.
-   By default, printed output now only shows a subset of available parameters.  Use '--verbose' to include all of them.
    -   New method `utils._filter_fields_in_lines()` is called from within `utils.print_lines_dicts()`.
-   `slurpy/sacct.py`
    -   `_construct_sacct_command()`
        -   New internal method to construct the sacct command to be called, allow optional arguments, etc.
-   `slurpy/__main__.py`
    -   Added the `_DEFAULT_ARG_START` internal parameter which determines the default value for the `--start` argument.  I set the current value to '-7.0', meaning the default start time is seven days in the past from whenever `slurpy` is run.


## v0.2 - 2017/01/14
## -----------------
-   Added 'CANCELLED' and 'TIMEOUT' states.
-   Added `--verbose` command-line argument to modify results.
-   Added `--summary` command-line argument to summarize all jobs reported by 'sacct'.  Currently returns the counts and optionally the min, max, median elapsed time for each state (if the `--verbose` flag is passed).
-   Added `-p`/`--partition` argument to select a particular partition of the cluster.
-   Added `--cancel` command, to cancel submitted jobs.
    -   When the (hardcoded) `_CANCEL_PROMPT` is set to True, then '__main__' will prompt the user to confirm that they want to cancel the jobs.  If `verbose` is enabled, it will also print the jobs about to be canceled.

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
    -   `prompt_yes_no` [new-method]
        -   Prompt the user for a y/n answer for an arbitrary question, take5n from [Recipe 57708](http://code.activestate.com/recipes/577058/).


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
