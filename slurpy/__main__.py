"""Main entry point for `slurpy` scripts.

Default behavior is to run 'sacct' and print parsed output.
"""
from slurpy import sacct, utils

# Prompt the user to confirm before canceling jobs.
_CANCEL_PROMPT = True
# Default value for the `--start` argument.  Should either be `None`, or a float value that
#    specifies how many days before today to set as the starting value.  For example,
#    If now is `2017-03-28T17:00:00` then the value `-2.5` would set the start time to
#    `2017-03-26T05:00:00`.
_DEFAULT_ARG_START = -7.0


def main(args=None, thread=False):
    if args is None:
        args = _init_argparse()
    log = utils.init_log(args)
    # Attach the log to `args` for convenience
    args.log = log
    log.debug("\nslurpy\n")
    log.debug("RUNNING IN DEBUG MODE\n")
    log.debug("args=\n{}".format(args))

    # Cancel / Kill Jobs
    # ------------------
    if args.cancel:
        log.debug("mode: 'cancel', prompt: '{}'".format(_CANCEL_PROMPT))
        if _CANCEL_PROMPT:
            lines, header = sacct.sacct_results(args)
            # Print the jobs about to be canceled
            if args.verbose:
                log.info("\nCancel would end the following jobs:\n")
                utils.print_lines_dicts(lines, header, args)
                print("")
            prompt = "Are you sure you want to cancel {} jobs?".format(len(lines))
            if not utils.prompt_yes_no(prompt, default='no'):
                log.warning("Exiting.")
                return

        from .import scancel
        log.debug("Running `scancel`.")
        scancel.scancel(args)
        return

    # Information sacct, summary, and squeue operations
    # -------------------------------------------------
    if args.summary:
        log.debug("Running `summary`")
        sacct.summary(args)
    elif args.queue:
        log.debug("Running `squeue`")
        from . import squeue
        squeue.squeue(args)
    else:
        log.debug("Running `sacct`")
        sacct.sacct(args)

    # 'Watch' Output: repeatedly printed
    # ----------------------------------
    # Repeatedly call `main` to keep producing new output
    if (args.watch is not None) and (not thread):
        log.debug("Entering 'watch' mode.")
        import time
        # Start look to keep re-calling this (the `main`) method repeatedly every interval
        while True:
            time.sleep(args.watch)
            # set `thread` to True so that subsequent calls don't start their own loops and timers.
            log.debug("Re-running `main`")
            main(args, thread=True)

    return


def _init_argparse():
    import argparse

    # Determine Default Values
    # ------------------------

    # Default start time
    if _DEFAULT_ARG_START is None:
        def_start = None
    else:
        import datetime
        #    Interpret `_DEFAULT_ARG_START` as a number of days in the past
        dt = datetime.datetime.now() + datetime.timedelta(days=_DEFAULT_ARG_START)
        def_start = dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Construct Argument Parser
    # -------------------------
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose", default=False,
        help="Extended output.")

    parser.add_argument(
        "--DEBUG", action="store_true", dest="debug", default=False,
        help="Lots of output for debugging purposes only.")

    parser.add_argument(
        "--replace", action="store_true", dest="replace", default=False,
        help="Replace failed/canceled/timeout sacct entries with newer ones (if names match).")

    parser.add_argument(
        "--head", nargs='?', dest="head", default=None, const=10,
        help=("Only print first `head` entries (default: 10)"))

    parser.add_argument(
        "--tail", nargs='?', dest="tail", default=None, const=10,
        help=("Only print last  `tail` entries (default: 10)"))

    parser.add_argument(
        "--state", type=str, dest="state", default=None,
        help="state to filter by (e.g. 'RUNNING', 'COMPLETED')")

    parser.add_argument(
        "--start", type=str, dest="start", default=def_start,
        help=("start time for `sacct` quieries in the format "
              "'YYYY-MM-DD[THH:MM[:SS]]' (e.g. `--start 2017-01-01`)."))

    parser.add_argument(
        "--id", type=str, dest="jobid", default=None, nargs='*',
        help=("JobID number to filter by (e.g. `--id 84513996`, `--id 84513996:84514000`"))

    parser.add_argument(
        "--sort", type=str, dest="sort", default=None,
        help=("Sort 'sacct' results by the given parameter field.  "
              "Use `--sort=-KEY` to reverse-sort by 'KEY'."))

    parser.add_argument(
        "--name", type=str, dest="name", default=None,
        help="job name to filter by")

    parser.add_argument(
        "-s", "--summary", action="store_true", dest="summary", default=False,
        help="Print a summary from the current 'sacct' results.")

    parser.add_argument(
        "-w", "--watch", nargs='?', dest="watch", type=int, default=None, const=4,
        help=("Print continuous output refreshed every given internal in seconds (default: 4)"))

    parser.add_argument(
        "--no-clear", action="store_false", dest="clear", default=True,
        help="Clear the screen before printing results.  NOTE: only applies in 'watch' mode.")

    parser.add_argument(
        "-q", "--queue", action="store_true", dest="queue", default=False,
        help="Print the current 'squeue' results.")

    parser.add_argument(
        "-p", "--partition", nargs='?', const="", default=None, dest="partition",
        help="Target a particular 'Partition' of the cluster.")

    # NOTE: this should be changed to a subcommand
    parser.add_argument(
        "--cancel", action="store_true", dest="cancel", default=False,
        help="Cancel submitted SLURM jobs.")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
