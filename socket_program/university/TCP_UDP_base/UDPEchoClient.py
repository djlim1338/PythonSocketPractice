#
# UDPEchoClient.py
# djlim
#

import socket

server_host = '203.250.133.86'
#server_host = '192.168.0.7'
#server_host = '127.0.0.1'
server_port = 50705
#server_port = 69
BUFF_SIZE = 1024
TIME_OUT = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIME_OUT)

server_address = (server_host, server_port)

try:
    while True:
        message = input("보낼 msg: ")
        if message.upper() == 'EXIT':
            break
        message = bytes(message, encoding='utf-8')
        #message = bytearray(message)
        try:
            bytes_sent = sock.sendto(message, server_address)
        except Exception as e:
            print(f"{e}")
        data, address = sock.recvfrom(BUFF_SIZE)
        print(f"서버[{address}]로부터: {data.decode()}")

except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    sock.close()
    print("종료")
