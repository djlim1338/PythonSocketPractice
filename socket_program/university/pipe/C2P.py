"""

C2P.py

"""

import os, sys
rd, wd = os.pipe()
pid = os.fork()

if pid:
    os.close(wd)
    r = os.fdopen(rd, 'r')
    message = r.read()
    print("message from child: {}".format(message))
    sys.exit(0)
else:
    os.close(rd)
    w = os.fdopen(wd, 'w')
    w.write("Hello, parent!")
    w.close()
    sys.exit(0)
