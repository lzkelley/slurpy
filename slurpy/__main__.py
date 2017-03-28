"""Main entry point for `slurpy` scripts.

Default behavior is to run 'sacct' and print parsed output.
"""
from slurpy import sacct, squeue, scancel, utils

# Prompt the user to confirm before canceling jobs.
_CANCEL_PROMPT = True


def main():
    args = _init_argparse()
    if args.summary:
        sacct.summary(args)
        return
    if args.queue:
        squeue.squeue(args)
        return
    if args.cancel:
        if _CANCEL_PROMPT:
            lines, header = sacct.sacct_results(args)
            # Print the jobs about to be canceled
            if args.verbose:
                print("\nCancel would end the following jobs:\n")
                utils.print_lines_dicts(lines, header, args)
                print("")
            prompt = "Are you sure you want to cancel {} jobs?".format(len(lines))
            if not utils.prompt_yes_no(prompt, default='no'):
                print("Exiting.")
                return

        scancel.scancel(args)
        return

    sacct.sacct(args)
    return


def _init_argparse():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", default=False,
                        help="Extended output.")

    parser.add_argument("--state",
                        type=str, dest="state", default=None,
                        help="state to filter by (e.g. 'RUNNING', 'COMPLETED')")

    parser.add_argument("--start",
                        type=str, dest="start", default=None,
                        help="start time for `sacct` quieries (e.g. `--start 2017-01-01`).")

    parser.add_argument("--id",
                        type=str, dest="jobid", default=None, nargs='*',
                        help=("JobID number to filter by "
                              "(e.g. `--id 84513996`, `--id 84513996:84514000`"))

    parser.add_argument("--sort",
                        type=str, dest="sort", default=None,
                        help=("Sort 'sacct' results by the given parameter field.  "
                              "Use `--sort=-KEY` to reverse-sort by 'KEY'."))

    parser.add_argument("--name",
                        type=str, dest="name", default=None,
                        help="job name to filter by")

    parser.add_argument("--summary",
                        action="store_true", dest="summary", default=False,
                        help="Print a summary from the current 'sacct' results.")

    parser.add_argument("-q", "--queue",
                        action="store_true", dest="queue", default=False,
                        help="Print the current 'squeue' results.")

    parser.add_argument("-p", "--partition",
                        nargs='?', const="", default=None, dest="partition",
                        help="Target a particular 'Partition' of the cluster.")

    # NOTE: this should be changed to a subcommand
    parser.add_argument("--cancel",
                        action="store_true", dest="cancel", default=False,
                        help="Cancel submitted SLURM jobs.")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
