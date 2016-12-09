"""Interact with the `sacct` SLURM command.
"""
import subprocess

from slurpy.const import META_WIDTH, SACCT_KEYS


def sacct(status):

    use_keys = [kk + "%{}".format(META_WIDTH) for kk in SACCT_KEYS]
    keys = ",".join(use_keys)

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
        if status in parts and 'extern' not in parts and 'batch' not in parts:
            # print(ii, ll)
            print(nice_parts)

    return
