#
# UDPEchoClient.py
# djlim
#

import socket

#server_host = '203.250.137.147'
#server_host = '203.250.133.86'
server_host = '203.250.133.88'
server_port = 50905
BUFF_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (server_host, server_port)
print(f"연결 요청할 서버: {server_address}")
sock.connect(server_address)

try:
    while True:
        message = input("보낼 msg: ")
        if message.upper() == 'EXIT':
            break
        message = bytes(message, encoding='utf-8')

        bytes_sent = sock.sendto(message, server_address)
        data, address = sock.recvfrom(BUFF_SIZE)
        print(f"서버로부터: {data.decode()}")

except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    sock.close()
    print("종료")
