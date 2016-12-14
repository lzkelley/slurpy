"""
"""

META_WIDTH = 50
# PRINT_WIDTH = 30
SEP_CHAR = ", "

SACCT_KEYS = ['JobID', 'jobname', 'State', 'Submit', 'Elapsed',
              'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
              'partition', 'nodelist']

STATE_KEYS = ['PENDING', 'RUNNING', 'COMPLETED', 'FAILED']
