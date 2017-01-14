"""Main entry point for `slurpy` scripts.

Default behavior is to run 'sacct' and print parsed output.
"""
from slurpy import sacct, squeue, scancel


def main():
    args = _init_argparse()
    if args.summary:
        sacct.summary(args)
        return
    if args.queue:
        squeue.squeue(args)
        return
    if args.cancel:
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
