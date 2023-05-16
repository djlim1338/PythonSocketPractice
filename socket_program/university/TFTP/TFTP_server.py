"""

TFTP_server.py
djlim

"""

from TFTP_lib import *
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 생성
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ''
port = 69
BACKLOG = 5

TFTP_ROOT_DIR = './TFTP_ROOT'

address = (host, port)
sock.bind(address)


def thread_process(in_message, in_client_address):
    print(f"start thread")
    serve_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serve_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    rq_split_list = rq_check(in_message)
    send_msg = ""
    print(rq_split_list)
    file_path = TFTP_ROOT_DIR + rq_split_list['filename']
    block_number = 0
    if rq_split_list['opcode'] == MESSAGE_OP_CODE['RRQ']:  # rrq 수신한 경우
        #send_msg = make_error_message(0x00, "not implemented yet (RRQ)")
        if not os.path.isfile(file_path):  # 파일이 없는 경우
            send_msg = make_data_message(0x01, ERROR_CODE[0x01])  # 0x01: "File not found."
        else:
            open_file = open(file_path, 'r', encoding="utf-8")
            put_file(serve_sock, in_client_address, "RRQ", input_file_name)
    elif rq_split_list['opcode'] == MESSAGE_OP_CODE['WRQ']:  # WRQ 수신한 경우
        #while True:
        send_msg = make_error_message(0x00, "not implemented yet (WRQ)")
    else:
        send_msg = make_error_message(0x05, ERROR_CODE[0x05])  # 0x05: "Unknown transfer ID."

    serve_sock.sendto(send_msg, in_client_address)
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
