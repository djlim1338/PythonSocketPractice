

# socket_client.py
# djlim
# 2023/03/27 ~
# socket test code

import socket


class SocketObj:
    _BUF_SIZE = 1024

    def __init__(self, protocol):
        self._protocol = protocol.upper()
        if self._protocol == 'UDP':
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=0)  # socket
        elif self._protocol == 'TCP':
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)  # socket
        return

    def socket_connect(self, server_ip, port):
        self._sock.connect((server_ip, port))
        print(f"server connect. ip[{server_ip}], port[{port}], protocol[{self._protocol}]")
        return

    def socket_close(self):
        self._sock.close()
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

    def socket_listen(self, connNum):
        self._sock.listen(connNum)


if __name__ == "__main__":
    try:
        #server_host = '203.250.133.86'
        server_host = '192.168.0.9'
        server_port = 50905
        sob = SocketObj('UDP')
        server_addr = (server_host, server_port)
        sob.socket_connect(server_host, server_port)
        #sob.socket_connect('203.250.137.174', 9900)
        #sob.socket_connect('127.0.0.1', 50905)
        while True:
            sendData = input("보낼 메시지 = ")
            if sendData == 'exit':
                break
            sob.socket_sendto(sendData, server_addr)
            #data, address = sob.socket_recvfrom()
            #print(f"{data.decode()}")
    except Exception as e:
        print(f"오류 발생. {e}")
    finally:
        sob.socket_close()
        print("종료")
