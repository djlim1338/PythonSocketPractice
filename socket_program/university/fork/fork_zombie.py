#! /usr/bin/python3

import os
import time
import sys

new_pid = os.fork()

if new_pid == 0:
    pass