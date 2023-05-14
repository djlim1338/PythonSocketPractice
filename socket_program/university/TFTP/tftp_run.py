"""

 TFTP_client.py
 djlim

 validators
 https://validators.readthedocs.io/en/latest/
 pip install validators
 import validators

"""

#from TFTP_client import *
import struct
import socket
import os
import sys
import time
import validators

BUFF_SIZE = 2048
DATA_MAX_SIZE = 512
RRQ_OPCODE = 0x0001  # RRQ(read)
WRQ_OPCODE = 0x0002  # WRQ(write)
ACK_OPCODE = 0x0004  # ACK
MODE = 'netascii'  # netascii(=text)
TFTP_MESSAGE_SPACE = 0x00  # 구분 공백
TIME_OUT = 5
WS = "-----------------------------------------------------------------------------------------------------------------------------"  # print출력시 벽

COMMAND_LIST = ['GET', 'PUT']  # 명령어 리스트
COMMAND_EXIT_LIST = ['EXIT', 'QUIT']  # 종료 명령어

STATE_CODE = {
    'INPUT_SKIP': 0,
    'INPUT_HOST': 1,
    'INPUT_PORT': 2,
    'PRINT_ADDRESS': 3,
    'INPUT_COMMAND': 4,
    'PROCESSING_COMMAND': 5
}

COMMAND_OPCODE = {
    'GET': 'RRQ',
    'PUT': 'WRQ'
}

MESSAGE_OP_CODE = {  # op code
    'RRQ': '0001',
    'WRQ': '0002',
    'DATA': '0003',
    'ACK': '0004',
    'ERROR': '0005',
    '0001': 'RRQ',
    '0002': 'WRQ',
    '0003': 'DATA',
    '0004': 'ACK',
    '0005': 'ERROR',
}


def input_y_n(print_str):  # 터미널에서 YES/NO(Y/N) 받고 T/F 출력.
    try:
        positive_answer_list = ['y', 'Y', 'yes', 'YES']
        negative_answer_list = ['n', 'N', 'no', 'NO']
        while True:
            _key_input = input(print_str).upper()
            if _key_input in positive_answer_list: return True
            elif _key_input in negative_answer_list: return False
            elif _key_input.upper() in COMMAND_EXIT_LIST: sys.exit(0) # 종료 코드시 코드 종료
            else:
                print(f"Words you can enter: {positive_answer_list}, {negative_answer_list}")
                continue
    except Exception as _e:
        print(f"ERROR!! {_e}")


def data_check(in_byte_data):
    byte_data_split_list = in_byte_data.hex('-').split('-')  # 헥사로 표현하여 1비트씩 끊어서 리스트에 저장. 자료형은 str

    opcode = ''.join(byte_data_split_list[0:2])  # opcode 추출
    block_number = int(''.join(byte_data_split_list[2:4]), 16)  # 블럭 번호 추출. hex문자열 => 자료형 int 로
    last_block = False

    if opcode == MESSAGE_OP_CODE['ERROR']:
        data_hex = ''.join(byte_data_split_list[4:-1])
    else:
        data_hex = ''.join(byte_data_split_list[4:])

    data_str = bytes.fromhex(data_hex).decode()
    data_length = len(data_str)  # 데이터 길이

    if data_length < DATA_MAX_SIZE:
        last_block = True

    return_dgram_dic = {
        'opcode': opcode,
        'number': block_number,
        'data': data_str,
        'last': last_block
    }

    return return_dgram_dic


def make_message(opcode, file_name, mode):
    pack_str = f"!H{len(file_name)}sB{len(mode)}sB"
    return struct.pack(pack_str, int(MESSAGE_OP_CODE[opcode]), file_name.encode(), TFTP_MESSAGE_SPACE, mode.encode(), TFTP_MESSAGE_SPACE)


def make_data_message(opcode, block_number, data):
    pack_str = f"!HH{len(data)}s"
    return struct.pack(pack_str, int(MESSAGE_OP_CODE[opcode]), block_number, data.encode())


def make_ack_message(data_block_number):
    pack_str = f"!2H"
    return struct.pack(pack_str, ACK_OPCODE, data_block_number)


def get_file(tftp_obj, address, opcode, file_name):
    send_msg = make_message(opcode, file_name, MODE)  # RRQ 바이트열 생성
    #print(f"{address} => {send_msg}")
    tftp_obj.sendto(send_msg, address)  # RRQ 송신
    file = open(file_name, 'w', encoding='utf-8')  # 파일 쓰기로 open
    last_block_number = 0  # 블럭 번호 저장
    print(WS)
    while True:
        data, recv_address = tftp_obj.recvfrom(BUFF_SIZE)  # 수신 (대기)
        data_split_list = data_check(data)  # 데이터 분류
        print(f"get from server[{address}] : no.{data_split_list['number']}")

        if data_split_list['opcode'] == MESSAGE_OP_CODE['ERROR']:  # 에러코드 발생시 알린 후 종료
            error_str = f"ERROR!! code({data_split_list['opcode']})  {data_split_list['data']}"
            print(error_str)
            file.write('\n\n' + error_str)
            print(WS)
            return
        elif (data_split_list['opcode'] == MESSAGE_OP_CODE['DATA']) and (
                data_split_list['number'] == last_block_number + 1):  # 데이터 수신시 번호를 보고 잘 왔으면 저장
            last_block_number = data_split_list['number']  # 블럭 번호 계수기
            if last_block_number >= 65535: last_block_number = 0  # 다음으로 와야할 블럭 번호. 65535 -> 1 (2byte 0~65535)
            # 데이터가 있으면 파일에 작성. 데이터가 없는 경우는 데이터가 512byte의 배수라는 의미로 마지막임을 알리기 위한 공백일 수 있음
            if data_split_list['data']:
                file.write(data_split_list['data'])
            # ACK 송신
            ack_msg = make_ack_message(data_split_list['number'])
            tftp_obj.sendto(ack_msg, recv_address)
            if data_split_list['last']:  # 마지막 블럭인 경우 루프 중단
                break
    print(f"get file done.")
    print(WS)
    file.close()


def put_file(tftp_obj, address, opcode, file_name):
    send_msg = make_message(opcode, file_name, MODE)  # WRQ 바이트열 생성
    tftp_obj.sendto(send_msg, address)  # WRQ 송신
    file = open(file_name, 'r', encoding='utf-8') # 파일 읽기로 open
    file_data_list = file.read()
    last_block_number = 0  # 블럭 번호 저장
    last_block_max_state = False
    print(WS)
    while True:
        data, recv_address = tftp_obj.recvfrom(BUFF_SIZE)
        data_split_list = data_check(data)  # 데이터 분류
        print(f"from server[{address}] : no.{data_split_list['number']}  type {MESSAGE_OP_CODE[data_split_list['opcode']]}  data {data_split_list['data']}")

        if data_split_list['opcode'] == MESSAGE_OP_CODE['ERROR']:  # 에러코드 발생시 알린 후 종료
            error_str = f"ERROR!! code({data_split_list['opcode']})  {data_split_list['data']}"
            print(error_str)
            file.write('\n\n' + error_str)
            print(WS)
            return
        elif (data_split_list['opcode'] == MESSAGE_OP_CODE['ACK']) and (
                data_split_list['number'] == last_block_number):  # 블럭번호 확인 후 데이터 송신
            if (len(file_data_list) <= 0) and (not last_block_max_state):
                break
            last_block_number += 1
            data_piece = file_data_list[:512]
            file_data_list = file_data_list[512:]
            if not last_block_max_state:
                send_dgram_msg = make_data_message('DATA', last_block_number, data_piece)  # 데이터
            else:
                send_dgram_msg = make_data_message('DATA', last_block_number, "")  # 데이터
                last_block_max_state = False
            #print(f"send put data = {send_dgram_msg}")
            tftp_obj.sendto(send_dgram_msg, recv_address)
            if (not last_block_max_state) and (len(data_piece) == 512) and (len(file_data_list) == 0):  # 데이터 크기가 512 배수인 경우
                #print(f"데이터의 크기가 512배수입니다.")
                last_block_max_state = True

    print(f"put file done.")
    print(WS)
    file.close()


if __name__ == "__main__":
    server_domain = "localhost"
    server_host = '127.0.0.1'
    server_port = 69
    input_address = (server_host, server_port)
    sock = ""
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
                if command_split[0] in COMMAND_LIST:
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
                    if os.path.isfile('./'+input_file_name):
                        over_write_answer = input_y_n(f"해당 파일({input_file_name})이 이미 존재합니다. 덮어 씌우시겠습니까? (y/n): ")
                        if not over_write_answer: # n선택시 명령어 입력으로
                            keyboard_input_state = STATE_CODE['INPUT_COMMAND']
                            continue
                    print(f"{command} file :{input_file_name} start...")
                    get_file(sock, input_address, COMMAND_OPCODE[command], input_file_name)
                elif command == 'PUT':
                    if not os.path.isfile('./'+input_file_name):
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
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 생성
            sock.settimeout(TIME_OUT)
            input_address = (server_host, server_port)
            keyboard_input_state = STATE_CODE['INPUT_COMMAND']
