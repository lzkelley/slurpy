"""
"""
from slurpy import sacct


def main():
    args = _init_argparse()
    sacct.sacct(args.state)

    return


def _init_argparse():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--state",
                        type=str, dest="state", default=None,
                        help="state to filter by (e.g. 'RUNNING', 'COMPLETED')")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
