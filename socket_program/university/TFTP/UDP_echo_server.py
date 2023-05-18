"""

UDP_echo_server.py
djlim

"""

#from TFTP_lib import *
import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 생성
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ''
port = 50069
#port = 50705
BACKLOG = 5

BUFF_SIZE = 1024

address = (host, port)
sock.bind(address)


def thread_process(in_message, in_client_address):
    serve_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serve_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print(f"client = {in_client_address}")
    serve_sock.sendto(in_message, in_client_address)

    serve_sock.close()


if __name__ == "__main__":
    print("server starting...")
    try:
        while True:
            message, client_address = sock.recvfrom(BUFF_SIZE)
            print(f"send from[{client_address}]")

            t2 = threading.Thread(target=thread_process, args=(message, client_address), daemon=True)
            t2.start()

    except KeyboardInterrupt:
        print(f"키보트 입력에 의한 종료")
    except Exception as e:
        print(f"오류 발생. {e}")
    finally:
        sock.close()
        print("종료")
