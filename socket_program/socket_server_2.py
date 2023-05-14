import socket

host = ''
port = 50905
BUFF_SIZE = 1024

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    sock.bind(server_address)

    while True:
        print('수신 대기중...')

        message, client_address = sock.recvfrom(BUFF_SIZE)
        print(f"msg:[[{message.decode()}], address:[{client_address}]")
        sock.sendto(message, client_address)
except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    sock.close()
    print("종료")
