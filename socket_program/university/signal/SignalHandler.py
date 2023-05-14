#!/usr/bin/python
#
# SignalHandler.py
# djlim
# 60page
#

import signal
import time

count = 0


def handler(signum, frame):
    global count
    count += 1
    print(f'Signal handler called with signal{signum} count({count})')
    if count >= 3:
        print(f'Signal handler reset!!')
        signal.signal(signal.SIGINT, signal.SIG_DFL)


signal.signal(signal.SIGINT, handler)

while True:
    print("waiting...")
    time.sleep(3)
