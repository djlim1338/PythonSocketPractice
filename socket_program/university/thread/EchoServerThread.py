#
# EchoServerThread.py
# djlim
#

import socket
import threading


class EchoThread(threading.Thread):

    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.ip, self.port = address
        self.csocket = socket
        print(f"새로운 연결 생성 {self.ip}")

    def run(self):
        thread_count = threading.active_count()
        print(f"{thread_count}개의 스레드 실행중...")
        while True:
            data = self.csocket.recv(2048)
            if data:
                print(f"from {self.ip}:{self.port} = {data.decode()}")
                self.csocket.sendall(data)
            else:
                break
        print(f"연결 해제됨 {self.ip}")
        thread_count = threading.active_count()
        print(f"{thread_count}개의 스레드 실행중...")


host = ''
port = 50905
BACKLOG = 5
address = (host, port)

conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conn_sock.bind(address)
conn_sock.listen(BACKLOG)

while True:
    print("연결 대기중")
    data_sock, client_address = conn_sock.accept()
    serviceThread = EchoThread(data_sock, client_address)
    serviceThread.setDaemon(True)
    serviceThread.start()
