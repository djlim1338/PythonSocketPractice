#
# EchoServerThread.py
# djlim
#

import socket
import sys
import threading

import select

host = ''
port = 50000
BUFF_SIZE = 1024
BACKLOG = 5
address = (host, port)

conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conn_sock.setblocking(0)

conn_sock.bind(address)
conn_sock.listen(BACKLOG)

print("서버 실행중..")
print("'exit' 입력시 서버 종료")

rd_list, wr_list, err_list = [sys.stdin, conn_sock], [], []

while True:
    readable, writeable, exception = select.select(rd_list, wr_list, err_list)
    for sock in readable:
        if sock is conn_sock:
            data_sock, client_address = conn_sock.accept()
            rd_list.append(data_sock)
        elif sock is sys.stdin:
            key = input()
            if key == "exit":
                sys.exit(0)
        else:
            data = sock.recv(BUFF_SIZE)
            if not data:
                print(f"{sock.getpeername()}끊김")
                sock.close()
                rd_list.remove(sock)
            else:
                print(f"{sock.getpeername()}로부터 메시지 {data.decode()}")
                sock.sendall(data)

