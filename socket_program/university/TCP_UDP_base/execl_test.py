#!/usr/bin/python3
#
# execl_test.py
# djlim
#

import os

os.execl('/bin/ls', 'ls', '-l')
os.system('/bin/ls -l')
print("제가.. 보이세요..?")