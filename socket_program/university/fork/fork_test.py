#
# fork_test.py
# djlim
# fork()는 win
#

import os
import sys
import time

new_pid = os.fork()

if new_pid == 0:
    pid = os.getpid()
    ppid = os.getppid()
    print(f"자식 프로세스 PID:{pid} / PPID:{ppid}")
else:
    pid = os.getpid()
    ppid = os.getppid()
    print(f"부모 프로세스 PID:{pid} / PPID:{ppid}")
time.sleep(15)
sys.exit(0)
