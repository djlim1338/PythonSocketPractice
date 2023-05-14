#!/usr/bin/env python3
#
# EchoServerFork.py
# djlim
#
#

import os
import sys
import errno
import signal
import socket

host = '203.250.133.88'
port = 50905
BUFF_SIZE = 1024
BACK_LOG = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (host, port)
print(f"연결할 서버 {server_address}")
sock.connect(server_address)

try:
    message = input("서버로 보낼 메시지 입력: ")
    #while message != "quit":
    while message != "exit":
        try:
            data = bytes(message, encoding='utf-8')
            sock.sendall(data)
            data = sock.recv(BUFF_SIZE)
            print(f"서버로부터 : {data.decode()}")
        except Exception as e:
            print(f"오류 발생 {e}")
            sys.exit(0)
        message = input("서버로 보낼 메시지 입력: ")

except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    try:
        sock.close()
    except Exception as e:
        print("data_sock 만들어지기 전 종료.")
