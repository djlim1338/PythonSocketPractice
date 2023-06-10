"""

TFTP_client_for_submission.py
djlim

"""

from TFTP_lib import *
import argparse

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 생성
sock.settimeout(SOCKET_TIME_OUT)  # 타임아웃 설정

if __name__ == "__main__":
    server_port = 69  # 50069

    parser = argparse.ArgumentParser(description='TFTP client program')
    parser.add_argument(dest="host", help="Server IP address", type=str)
    parser.add_argument(dest="action", help="get or put a file", type=str)
    parser.add_argument(dest="filename", help="name of file to transfer", type=str)
    parser.add_argument("-p", "--port", dest="port", action="store", type=int)
    args = parser.parse_args()

    """
    교수님쪽에 설치되지 않은 모듈. 빼야함
    if validators.domain(args.host):
        server_ip = socket.gethostbyname(args.host)
    elif validators.ip_address.ipv4(args.host):
        server_ip = args.host
    else:
        print("Invalid host address")
        exit(0)
    """

    if not(args.port is None):
        server_port = args.port
    server_host = args.host
    input_command = args.action.upper()
    input_file_name = args.filename

    if not os.path.isdir(TFTP_CLIENT_ROOT_DIR):
        os.mkdir(TFTP_CLIENT_ROOT_DIR)
    input_address = (server_host, server_port)

    keyboard_input_state = STATE_CODE['INPUT_SKIP']

    input_address = (server_host, server_port)

    start_time = time.time()
    try:
        if input_command == 'GET':
            print(f"{input_command} file :{input_file_name} start...")
            get_file(sock, input_address, COMMAND_OPCODE[input_command], input_file_name)
        elif input_command == 'PUT':
            if not os.path.isfile(TFTP_CLIENT_ROOT_DIR + input_file_name):
                print(f"[{input_file_name}] That file doesn't exist.")
                exit(0)
            print(f"{input_command} file :{input_file_name} start...")
            put_file(sock, input_address, COMMAND_OPCODE[input_command], input_file_name)
        else:
            print(f"unknown command! [{input_command}]")
            exit(0)
        end_time = time.time() - start_time
        print(f"time = {end_time:.3f}")
        print("")
    except Exception as e:
        print(f"ERROR! {e}")
    finally:
        exit(0)
