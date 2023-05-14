import socket

#host = '203.250.133.68'
host = '127.0.0.1'
port = 50905
BUFF_SIZE = 1024

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)



    while True:
        message = input("메시지 입력: ")
        message = bytes(message, encoding='utf-8')

        bytes_send = sock.sendto(message, server_address)
        data, address = sock.recvfrom(BUFF_SIZE)
        print(f"서버로부터: {data.decode()}")
except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    sock.close()
    print("종료")