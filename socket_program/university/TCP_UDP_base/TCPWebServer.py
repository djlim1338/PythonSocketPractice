#
# TCPWebServer.py
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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    while True:

        print("연결 대기중")
        data_sock, address = conn_sock.accept()
        print(f"요청: {address}")

        data = data_sock.recv(BUFF_SIZE)
        data = data.decode()
        print('receive >> ' + data)

        header = 'HTTP/1.0 200 0K\r\n'
        html2 = """
        Content-Type: text/html; charset=utf-8
        Accept-Ranges: bytes
        Vary: Accept-Encoding
        <!DOCTYPE html>
        """

        html = """
        <HTML><BODY>
        <H1> Hello, World! </H1>
        </BODY></HTML>
        """

        data_sock.send((header + html).encode('utf-8'))
        data_sock.close()

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
