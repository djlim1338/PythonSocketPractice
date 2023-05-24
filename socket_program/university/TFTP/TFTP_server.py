"""

TFTP_server.py
djlim

"""

from TFTP_lib import *
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 생성
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ''
port = 50069 #69  #50069
BACKLOG = 5

address = (host, port)
sock.bind(address)


def thread_process(in_message, in_client_address):
    print(f"start thread")
    serve_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serve_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serve_sock.settimeout(SOCKET_TIME_OUT)  # 타임아웃 설정
    #serve_sock.bind(("", 0))

    rq_split_list = rq_check(in_message)
    send_msg = ""
    print(rq_split_list)
    #block_number = 0
    if rq_split_list['opcode'] == MESSAGE_OP_CODE['RRQ']:  # rrq 수신한 경우
        print("send RRQ")
        #send_msg = make_error_message(0x00, "not implemented yet (RRQ)")
        if not os.path.isfile(TFTP_ROOT_DIR + rq_split_list['filename'].decode()):  # 파일이 없는 경우
            send_msg = make_error_message(0x01, ERROR_CODE[0x01])  # 0x01: "File not found."
            serve_sock.sendto(send_msg, in_client_address)
        else:
            try:
                rrq_server(serve_sock, in_client_address, rq_split_list['filename'].decode())
            except Exception as e:
                print(f"server ERROR! {e}")
    elif rq_split_list['opcode'] == MESSAGE_OP_CODE['WRQ']:  # WRQ 수신한 경우
        print("send WRQ")
        try:
            wrq_server(serve_sock, in_client_address, rq_split_list['filename'].decode())
        except Exception as e:
            print(f"server ERROR! {e}")
        #send_msg = make_error_message(0x00, "not implemented yet (WRQ)")
    else:
        send_msg = make_error_message(0x05, ERROR_CODE[0x05])  # 0x05: "Unknown transfer ID."
        serve_sock.sendto(send_msg, in_client_address)

    serve_sock.close()


if __name__ == "__main__":
    if not os.path.isdir(TFTP_ROOT_DIR):
        os.mkdir(TFTP_ROOT_DIR)
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
