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
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ��Ʈ ��� ���
server_address = (host, port)
conn_sock.bind(server_address)
conn_sock.listen(BACK_LOG)

exit_state = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    while True:

        print("���� �����")
        data_sock, address = conn_sock.accept()
        print(f"��û: {address}")

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
    print(f"Ű��Ʈ �Է¿� ���� ����")
except Exception as e:
    print(f"���� �߻�. {e}")
finally:
    try:
        data_sock.close()
    except Exception as e:
        print("data_sock ��������� �� ����.")

    try:
        conn_sock.close()
    except Exception as e:
        print("conn_sock ��������� �� ����.")
    print("�ڵ� ����")
