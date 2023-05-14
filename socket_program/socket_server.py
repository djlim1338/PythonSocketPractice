# socket_server.py
# djlim
# 2023/03/09 ~
# socket test code

import socket
import threading
from SocketServer import SocketServer as sock

if __name__ == "__main__":
    try:
        sob = sock('', 50905, 'UDP')  # 노브툭을 서버로 할 때
        sob.socket_bind()

        while True:
            print(f"수신 대기중...")
            message, client_address = sob.socket_recvfrom()
            print(f"client:[{message.encoding()}] / msg:[{client_address}]")
            sob.socket_sendto(message, client_address)
    except KeyboardInterrupt:
        print(f"키보트 입력에 의한 종료")
    except Exception as e:
        print(f"오류 발생. {e}")
    finally:
        sob.socket_close()
        print("종료")
