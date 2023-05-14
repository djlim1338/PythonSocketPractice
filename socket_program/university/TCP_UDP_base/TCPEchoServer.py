#
# TCPEchoServer.py
# djlim
#

import socket

host = ''
port = 50905
BUFF_SIZE = 1024
BACK_LOG = 5

conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 즉시 사용
server_address = (host, port)
conn_sock.bind(server_address)
conn_sock.listen(BACK_LOG)

exit_state = False

try:
    while True:

        print("연결 대기중")
        data_sock, address = conn_sock.accept()
        print(f"요청: {address}")
        
        while True:
            print("수신 대기중...")
            message = data_sock.recv(BUFF_SIZE)

            if message.decode().upper() == 'EXITS':
                exit_str = "종료가 감지되었습니다. 서버가 종료됩니다."
                print(exit_str)
                data_sock.sendall(exit_str.encode())
                exit_state = True
                break

            if message:
                print(f"받은 메시지: {message.decode()}")
                data_sock.sendall(message)
            else:
                print(f"연결 끊김[{address}]")
                break
        if exit_state:
            break

except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    try:
        data_sock.close()
    except Exception as e:
        print("data_sock 만들어지기 전 종료.")

    try:
        conn_sock.close()
    except Exception as e:
        print("conn_sock 만들어지기 전 종료.")
    print("코드 종료")
