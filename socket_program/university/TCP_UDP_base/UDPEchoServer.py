#
# UDPEchoServer.py
# djlim
#

import socket

host = ''
port = 50705
BUFF_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (host, port)
sock.bind(server_address)

try:
    while True:
        print("수신 대기중...")

        message, client_address = sock.recvfrom(BUFF_SIZE)
        print(f"주소[{client_address}] / msg[{message.decode()}]")

        sock.sendto(message, client_address)

except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    sock.close()
    print("종료")
