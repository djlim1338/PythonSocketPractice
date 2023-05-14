#
# vsftpClient.py
# djlim
#
import os
import socket
import sys
import time

host = '203.250.133.88'
#host = '203.250.133.86'
port = 50905
#port = 8080
BUFF_SIZE = 1024
BACK_LOG = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (host, port)
print(f"연결할 서버 {server_address}")
sock.connect(server_address)

try:
    message = input("Enter file name>")
    try:
        start_time = time.time()  # 다운로드 소요시간 측정
        data_size = 0
        data = bytes(message, encoding='utf-8')
        sock.sendall(data)
        data_counter = 0
        with open(message, 'w', encoding='utf-8') as open_file:
            while True:
                line = sock.recv(BUFF_SIZE)
                if line:
                    open_file.write(line.decode('utf-8'))
                    data_counter += 1
                    data_size += len(line)
                else:
                    break
        end_time = time.time() - start_time
        if data_counter != 0:
            print(f"file transfer completed. 소요된 시간:{end_time:.5f} / 받은 데이터:{data_size}byte")
        else:
            os.remove(message)
            print(f"받은 데이터가 없어서 생성된 파일을 제거했습니다.[{message}]")
    except Exception as e:
        print(f"오류 발생 {e}")
        sys.exit(0)
    sock.close()

except KeyboardInterrupt:
    print(f"키보트 입력에 의한 종료")
except Exception as e:
    print(f"오류 발생. {e}")
finally:
    try:
        sock.close()
    except Exception as e:
        print("data_sock 만들어지기 전 종료.")
