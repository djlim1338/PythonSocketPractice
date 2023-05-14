#
# ZombieCollect.py
# djlim
# 61page
#

import os
import sys
import signal
import time


def collect_zombie(signum, frame):
    print("SIGCHLD dilivered...")
    time.sleep(5)
    pid, status = os.waitpid(-1, os.WNOHANG)
    print("zombie process remove")


signal.signal(signal.SIGCHLD, collect_zombie)
pid = os.fork()

if pid == 0:
    print("child process running...")
    time.sleep(5)
    print("child process exiting...")
    os._exit(0)

time.sleep(15)
print("parent process exiting...")
sys.exit(0)
