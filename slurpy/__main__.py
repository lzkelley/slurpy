"""
"""
from slurpy import sacct


def main():
    args = _init_argparse()
    sacct.sacct(args.status)

    return


def _init_argparse():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--status",
                        type=str, dest="status", default="RUNNING",
                        help="Status to filter by (e.g. 'RUNNING', 'COMPLETED')")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
