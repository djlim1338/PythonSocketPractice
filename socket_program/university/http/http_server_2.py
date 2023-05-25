"""

http_server.py

"""

import socket
import sys
import os
import signal
import errno


def shutdownServer(signum, frame):
    print("server shutdown ...")
    sys.exit(0)


def collectZombie(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except:
            break
def doHTTPService(sock) :
    try :
        reqMessage = sock.recv(RECV_BUFF)
    except ConnectionResetError as e :
        sock.close()
        return
    if reqMessage :
        msgString = bytes.decode(reqMessage)
        print(msgString)
        # split message into lines
        lines = msgString.split('\r\n')
        # get the first line (request line)
        reqLine = lines[0]
        # parse the request line into fields
        fields = reqLine.split(' ')
        method = fields[0]
        reqURL = fields[1]
        ver = fields[2]
        print('requested URL: {}'.format(reqURL))
    else : # client closed the connection
        sock.close()
        return

    if reqURL == '/':
        open_file = open("/index.html", "r", encoding = "utf-8")
    else:
        statusLine = 'HTTP/1.1 200 OK\r\n'
        headerLine1 = 'Server: vshttpd 0.1\r\n'
        headerLine2 = 'Connection: close\r\n\r\n'
    sock.sendall(statusLine.encode())
    sock.sendall(headerLine1.encode())
    sock.sendall(headerLine2.encode())
    while True:
        responseBody = open_file.readline()
        sock.sendall(responseBody.encode())
    sock.close()
# end of doHTTPService()

HOST_IP = '203.250.133.88'
PORT = 50000
#PORT = int(sys.argv[1])
BACKLOG = 5
RECV_BUFF = 10000
signal.signal(signal.SIGINT, shutdownServer)
signal.signal(signal.SIGCHLD, collectZombie)

try :
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 즉시 사용
except :
    print("failed to create a socket")
    sys.exit(1)

try: # user provided port may be unavaivable
    connSock.bind((HOST_IP, PORT))
except Exception as e:
    print("failed to acquire sockets for port {}".format(PORT))
    sys.exit(1)

print("server running on port {}".format(PORT))
print("press Ctrl+C (or $kill -2 pid) to shutdown the server")

connSock.listen(BACKLOG)
while True:
    print("waiting a new connection...")
    try :
        dataSock, addr = connSock.accept()
        print("got a connection request from: {}".format(addr))
    except IOError as e :
        code, msg = e.args
        if code == errno.EINTR :
            continue
        else :
            raise

    pid = os.fork()
    if pid == 0 :
        doHTTPService(dataSock)
        sys.exit(0)

    dataSock.close()
