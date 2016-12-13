"""
"""

META_WIDTH = 50
# PRINT_WIDTH = 30
SEP_CHAR = ", "

SACCT_KEYS = ['JobID', 'jobname', 'state', 'submit', 'elapsed',
              'AveVMSize', 'MaxVMSize', 'ReqMem', 'AveDiskRead', 'AveDiskWrite',
              'partition', 'nodelist']

STATUS_KEYS = ['RUNNING', 'COMPLETED', 'FAILED']
