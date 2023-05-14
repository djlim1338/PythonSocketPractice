#
# SocketServer.py
# djlim
#

import socket


class SocketServer:
    _BUF_SIZE = 1024

    def __init__(self, host, port, protocol):
        self._host = host  # host IP
        self._port = port  # service port
        self._protocol = protocol.upper()
        self._sockAddr = (self._host, self._port)  # address 튜플. bind 인수는 튜플로 넣음
        if self._protocol == 'UDP':
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket
        elif self._protocol == 'TCP':
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)  # socket 기본
        return

    def socket_bind(self):  # 주로 서버가 자신의 주소를 설정할 때. 클라이언트는 보통 사용하지 않음 TCP, UDP
        self._sock.bind(self._sockAddr)
        print(f"\nsocket bind start!\nIP={self._host}\nPORT={self._port}\nprotocol={self._protocol}\n")
        return

    def socket_listen(self, number):  # passive open 상태로 천이. TCP
        if self._protocol == 'UDP':
            print("The udp protocol does not use listen.")
        elif self._protocol == 'TCP':
            self._sock.listen(number)
            print("socket listen success.")
        return

    def socket_recv(self):
        return self._sock.recv(self._BUF_SIZE)

    def socket_recvfrom(self):
        return self._sock.recvfrom(self._BUF_SIZE)

    def socket_send(self, msg):
        send_data = bytes(msg, encoding='utf-8')
        self._sock.send(send_data)
        return

    def socket_sendto(self, msg, addr):
        send_data = bytes(msg, encoding='utf-8')
        self._sock.sendto(send_data, addr)
        return

    def socket_accept(self):
        return self._sock.accept()

    def socket_close(self):
        self._sock.close()
        return