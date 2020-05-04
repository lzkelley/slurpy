"""
"""

import re


META_WIDTH = 50
COLUMN_SPACING = 2
SEP_CHAR = " "
# Change time-strings as returned by sacct into a different format
REFORMAT_TIMES = True
REFORMAT_TIMES_SEP_CHAR = " "

# SACCT_KEYS = ['JobID', 'JobName', 'State', 'Submit', 'Start', 'Elapsed',
#               'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
#               'partition', 'nodelist']
SACCT_KEYS = ['JobID', 'JobName', 'State', 'Submit', 'Start', 'Elapsed',
              'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
              'partition']

SACCT_KEYS_TIMES = ['Submit', 'Start', 'Elapsed']

SACCT_KEYS_PRINT = ['JobID', 'JobName', 'State', 'Submit', 'Start', 'Elapsed',
                    'partition']

SQUEUE_KEYS = ['account', 'arrayjobid', 'arraytaskid', 'command', 'cores',
               'deadline', 'endtime', 'exit_code', 'groupid', 'groupname',
               'jobid', 'maxcpus', 'maxnodes', 'name', 'minmemory',
               'numcpus', 'numnodes', 'partition', 'starttime', 'submittime',
               'timeused', 'timeleft', 'timelimit', 'username']

DEF_PARTITIONS = ['hernquist', 'itccluster']

STATE_KEYS = ['PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT']
STATE_KEYS_FAILED = ['FAILED', 'CANCELLED', 'TIMEOUT']
STATE_KEYS_OKAY = ['PENDING', 'RUNNING', 'COMPLETED']

REGEX_TIMES = '(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})'


# Constructed / Calculated constants
# ----------------------------------
_REGEX_TIMES_PATTERN = re.compile(REGEX_TIMES)
