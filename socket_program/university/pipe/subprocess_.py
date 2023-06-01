"""

subprocess_.py

"""

import subprocess
prog = "/bin/ls"
try:
    proc = subprocess.Popen([prog, "-l"])
except Exception as e:
    print(e)
