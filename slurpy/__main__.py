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

    parser.add_argument("--status",
                        type=str, dest="status", default="RUNNING",
                        help="Status to filter by (e.g. 'RUNNING', 'COMPLETED')")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
