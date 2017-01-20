"""
"""

META_WIDTH = 50
COLUMN_SPACING = 2
SEP_CHAR = ", "

SACCT_KEYS = ['JobID', 'JobName', 'State', 'Submit', 'Start', 'Elapsed',
              'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
              'partition', 'nodelist']

SACCT_KEYS_PRINT = ['JobID', 'JobName', 'State', 'Submit', 'Start', 'Elapsed',
                    'partition']

SQUEUE_KEYS = ['account', 'arrayjobid', 'arraytaskid', 'command', 'cores',
               'deadline', 'endtime', 'exit_code', 'groupid', 'groupname',
               'jobid', 'maxcpus', 'maxnodes', 'name', 'minmemory',
               'numcpus', 'numnodes', 'partition', 'starttime', 'submittime',
               'timeused', 'timeleft', 'timelimit', 'username']

DEF_PARTITIONS = ['hernquist', 'itccluster']

STATE_KEYS = ['PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT']
