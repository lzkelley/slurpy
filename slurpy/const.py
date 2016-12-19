"""
"""

META_WIDTH = 50
SEP_CHAR = ", "

SACCT_KEYS = ['JobID', 'jobname', 'State', 'Submit', 'Elapsed',
              'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
              'partition', 'nodelist']

SQUEUE_KEYS = ['account', 'arrayjobid', 'arraytaskid', 'command', 'cores',
               'deadline', 'endtime', 'exit_code', 'groupid', 'groupname',
               'jobid', 'maxcpus', 'maxnodes', 'name', 'minmemory',
               'numcpus', 'numnodes', 'partition', 'starttime', 'submittime',
               'timeused', 'timeleft', 'timelimit', 'username']

DEF_PARTITIONS = ['hernquist', 'itccluster']

STATE_KEYS = ['PENDING', 'RUNNING', 'COMPLETED', 'FAILED']
