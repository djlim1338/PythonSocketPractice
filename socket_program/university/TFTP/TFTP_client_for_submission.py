"""

TFTP_client_for_submission.py
djlim

"""

from TFTP_lib import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 생성
sock.settimeout(SOCKET_TIME_OUT)  # 타임아웃 설정

if __name__ == "__main__":
    if not os.path.isdir(TFTP_CLIENT_ROOT_DIR):
        os.mkdir(TFTP_CLIENT_ROOT_DIR)
    server_domain = "localhost"
    server_host = '127.0.0.1'
    server_port = 69  # 50069
    input_address = (server_host, server_port)
    input_command = ""
    input_file_name = ""

    keyboard_input_state = STATE_CODE['INPUT_SKIP']
    while True:
        if keyboard_input_state == STATE_CODE['INPUT_COMMAND']:  # 명령어 입력
            try:
                input_command = input(f"commend : ")
                if input_command.upper() in COMMAND_EXIT_LIST: sys.exit(0)  # 종료 코드시 코드 종료
                command_split = input_command.split()
                command_split[0] = command_split[0].upper()
                if command_split[0] in COMMAND_ACTION_LIST:
                    command = command_split[0]
                    input_file_name = command_split[1]
                    keyboard_input_state = STATE_CODE['PROCESSING_COMMAND']
                else:
                    print(f"Unknown command! {command_split[0]}")
            except Exception as e:
                keyboard_input_state = STATE_CODE['INPUT_COMMAND']
                print(f"Please enter the correct command")

        elif keyboard_input_state == STATE_CODE['PROCESSING_COMMAND']:  # 명령어 처리
            start_time = time.time()
            try:
                if command == 'GET':
                    if os.path.isfile(TFTP_CLIENT_ROOT_DIR+input_file_name):
                        over_write_answer = input_y_n(f"해당 파일({input_file_name})이 이미 존재합니다. 덮어 씌우시겠습니까? (y/n): ")
                        if not over_write_answer: # n선택시 명령어 입력으로
                            keyboard_input_state = STATE_CODE['INPUT_COMMAND']
                            continue
                    print(f"{command} file :{input_file_name} start...")
                    get_file(sock, input_address, COMMAND_OPCODE[command], input_file_name)
                elif command == 'PUT':
                    if not os.path.isfile(TFTP_CLIENT_ROOT_DIR+input_file_name):
                        print(f"해당 파일({input_file_name})이 존재하지 않습니다.")
                        keyboard_input_state = STATE_CODE['INPUT_COMMAND']  # 명령어 입력으로
                        continue
                    print(f"{command} file :{input_file_name} start...")
                    put_file(sock, input_address, COMMAND_OPCODE[command], input_file_name)
                end_time = time.time() - start_time
                print(f"time = {end_time:.3f}")
                print("")
            except Exception as e:
                print(f"ERROR! {e}")
            finally:
                keyboard_input_state = STATE_CODE['INPUT_COMMAND']

        elif keyboard_input_state == STATE_CODE['INPUT_SKIP']:  # 기본값 여부
            skip_answer = input_y_n("[skip] setting value default (y/n): ")
            if skip_answer: keyboard_input_state = STATE_CODE['PRINT_ADDRESS']
            else: keyboard_input_state = STATE_CODE['INPUT_HOST']

        elif keyboard_input_state == STATE_CODE['INPUT_HOST']:  # server IP address 입력
            server_host = input("server ip: ")
            if server_host.upper() in COMMAND_EXIT_LIST: sys.exit(0) # 종료 코드시 코드 종료
            if validators.domain(server_host):  # 입력한 값이 도메인
                server_domain = server_host
                server_host = socket.gethostbyname(server_domain)
            elif validators.ip_address.ipv4(server_host) or validators.ip_address.ipv6(server_host):  # 입력한 값이 주소
                print("Scanning domain...")
                try:
                    server_domain = socket.gethostbyaddr(server_host)
                except Exception as e:
                    server_domain = "unknown_domain"
                finally:
                    print(f"doamin:{server_domain}")
            keyboard_input_state = STATE_CODE['INPUT_PORT']

        elif keyboard_input_state == STATE_CODE['INPUT_PORT']:  # server port 입력
            server_port = input("server port: ")
            try:
                server_port = int(server_port)  # 입력값 정수도 변환 시도
                keyboard_input_state = STATE_CODE['PRINT_ADDRESS']
            except Exception as e:
                if server_port.upper() in COMMAND_EXIT_LIST: sys.exit(0)  # 종료 코드시 코드 종료
                print("Please enter an integer")  # 실패시 안내문장 출력

        elif keyboard_input_state == STATE_CODE['PRINT_ADDRESS']:  # server address 출력
            print(f"server address is [{server_domain}]{server_host}:{server_port}")
            input_address = (server_host, server_port)
            keyboard_input_state = STATE_CODE['INPUT_COMMAND']
