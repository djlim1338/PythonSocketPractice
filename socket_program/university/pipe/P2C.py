"""

P2C.py

"""

import os, sys
rd, wd = os.pipe()
pid = os.fork()

if pid:
    os.close(rd)
    w = os.fdopen(wd, 'w')
    w.write("Hello, child!")
    w.close()
    sys.exit(0)
else:
    os.close(wd)
    r = os.fdopen(rd, 'r')
    message = r.read()
    print("message from parent: {}".format(message))
    sys.exit(0)
