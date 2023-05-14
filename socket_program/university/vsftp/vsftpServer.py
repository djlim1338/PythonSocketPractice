#
# vsftpServer.py
# djlim
#
import errno
import socket
import os
import signal

host = ''
port = 50905
BUFF_SIZE = 1024
BACK_LOG = 5


def collect_zombie(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except:
            break


signal.signal(signal.SIGCHLD, collect_zombie)


conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 즉시 사용
server_address = (host, port)
conn_sock.bind(server_address)
conn_sock.listen(BACK_LOG)

exit_state = False

try:
    while True:
        try:
            print("연결 대기중...")
            data_sock, address = conn_sock.accept()
            print(f"연결된 포트: {port}")
        except IOError as e:
            code, msg = e.args
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0:
            conn_sock.close()
            file_name = data_sock.recv(BUFF_SIZE).decode()
            send_data_size = 0
            if os.path.isfile(file_name):
                with open(file_name, 'r', encoding='utf-8') as open_file:
                    for line in open_file:
                        data_sock.sendall(line.encode('utf-8'))
                    print(f"보낸 파일명: {file_name}")
            else:
                error_str = f"해당 파일이 존재하지 않습니다. {file_name}"
                print(error_str)
                #data_sock.sendall(error_str.encode())

            os._exit(0)

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
