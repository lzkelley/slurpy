"""
"""

import subprocess

KEYS = ['JobID', 'jobname', 'state', 'submit', 'elapsed',
        'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
        'partition', 'nodelist']

META_WIDTH = 50
PRINT_WIDTH = 30


def main():
    args = _init_argparse()

    use_keys = [kk + "%{}".format(META_WIDTH) for kk in KEYS]
    keys = ",".join(use_keys)
    # print(keys)
    # return

    command = ['sacct', '--format', keys]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    retcode = p.wait()
    # print("retcode = ", retcode)

    lines = text.split('\n')
    header = lines.pop(0)
    lines = lines[1:]
    for ii, ll in enumerate(lines):
        # print(ii, ll)
        parts = ll.split()
        # nice_parts = "{:4d}: ".format(ii) + ", ".join('{1:{0:}}'.format(PRINT_WIDTH, pp.strip()) for pp in parts)
        nice_parts = "{:4d}: ".format(ii) + ", ".join('{}'.format(pp.strip()) for pp in parts)
        if args.status in parts and 'extern' not in parts and 'batch' not in parts:
            # print(ii, ll)
            print(nice_parts)

    return


def _init_argparse():
    import argparse
    parser = argparse.ArgumentParser()

    # parser.add_argument("-e", "--evolve",
    #                     action="store_true", dest="evolve", default=False,
    #                     help="Evolve the binaries over time.")
    # parser.add_argument("-a", "--analyze",
    #                     action="store_true", dest="analyze", default=False,
    #                     help="Analyze the binaries after evolution.")
    # parser.add_argument("-p",
    #                     action="store_true", dest="plot", default=False,
    #                     help="Plot (default) results of analysis and evolution.")
    # parser.add_argument("--plot",
    #                     type=int, nargs='*', dest="plot", default=False,
    #                     help="Plot results of analysis and evolution.")
    parser.add_argument("--status",
                        type=str, dest="status", default="RUNNING",
                        help="Status to filter by (e.g. 'RUNNING', 'COMPLETED')")
    # parser.add_argument("-o", "--out",
    #                     type=str, dest="output", default=None,
    #                     help="Output directory")
    # parser.add_argument("--sets",
    #                     type=str, dest="sets", default=None,
    #                     help="Name for configuration file from which to take settings.")
    # parser.add_argument("--name",
    #                     type=str, dest="name", default=None,
    #                     help="Name of this simulation run, for output directory etc.")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
