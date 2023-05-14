#
# tftp_get_client.py
# djlim
# D:\NAS\universityData\pythonProject\socket_program\university\TFTP
#

import struct
import socket
import os
import sys

BUFF_SIZE = 1024
DATA_MAX_SIZE = 512
RRQ_OPCODE = 0x0001  # RRQ(read)
ACK_OPCODE = 0x0004  # ACK
RRQ_MODE = 'netascii'  # netascii(=text)
TFTP_MESSAGE_SPACE = 0x00  # 구분 공백
WS = "-----------------------------------------------------------------------------------------------------------------------------"  # print출력시 벽

DATA_INDEX_OPCODE = 0
DATA_INDEX_BLOCK_NUMBER = 1
DATA_INDEX_DATA = 2
DATA_INDEX_LAST_STATE = 3

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

"""
강의자료랑 실제 오류 코드가 다른데..?
MESSAGE_ERROR_CODE = {  # error code
    '0000': 'Not defined, see error message (if any).',
    '0001': 'File not found.',
    '0002': 'Access violation.',
    '0003': 'Disk full or allocation exceeded.',
    '0004': 'Illegal TFTP operation.',
    '0005': 'Unknown transfer ID.',
    '0006': 'File already exists',
    '0007': 'No such user.',
}
"""

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def make_rrq_message(in_file_name):
    pack_str = f"!H{len(in_file_name)}sb{len(RRQ_MODE)}sb"
    return struct.pack(pack_str, RRQ_OPCODE, in_file_name.encode(), TFTP_MESSAGE_SPACE, RRQ_MODE.encode(), TFTP_MESSAGE_SPACE)


def send_message(_opcode, _file_name, _mode):
    pack_str = f"!H{len(_file_name)}sb{len(RRQ_MODE)}sb"
    return struct.pack(pack_str, _opcode, _file_name.encode(), TFTP_MESSAGE_SPACE, RRQ_MODE.encode(), TFTP_MESSAGE_SPACE)


def make_ack_message(in_data_block_number):
    pack_str = f"!2H"
    return struct.pack(pack_str, ACK_OPCODE, in_data_block_number)


def send_ack_message(_socket, _address, _data_block_number):
    _pack_str = f"!2H"
    _bytes_sent = _socket.sendto(struct.pack(_pack_str, ACK_OPCODE, _data_block_number), _address)
    print(f"ACK data len : {_bytes_sent}  address : {address}")
    return True


def data_check(in_byte_data):
    byte_data_split_list = in_byte_data.hex('-').split('-')  # 헥사로 표현하여 1비트씩 끊어서 리스트에 저장. 자료형은 str

    opcode = ''.join(byte_data_split_list[0:2])  # opcode 추출
    #print(byte_data_split_list[2:4])
    block_number = int(''.join(byte_data_split_list[2:4]), 16)  # 블럭 번호 추출. hex문자열 => 자료형 int 로
    last_block = False

    if opcode == MESSAGE_OP_CODE['ERROR']:
        data_hex = ''.join(byte_data_split_list[4:-1])
        print(byte_data_split_list[4:-1])
        print(data_hex)
    else:
        data_hex = ''.join(byte_data_split_list[4:])

    data_str = bytes.fromhex(data_hex).decode()
    data_length = len(data_str)  # 데이터 길이

    if data_length < DATA_MAX_SIZE:
        last_block = True

    """
    print(WS)
    print(f"opcode = {opcode}:{MESSAGE_OP_CODE[opcode]}")
    #print(f"data byte = {in_byte_data}")
    #print(f"data list = {byte_data_split_list}")
    #print(f"data string = {data_str}")
    print(f"data block number = {block_number}")
    print(f"data len = {data_length}")
    print(f"last block state = {last_block}")
    print(WS)
    """

    return opcode, block_number, data_str, last_block


def input_y_n(_print_str):  # 터미널에서 YES/NO(Y/N) 받고 T/F 출력.
    try:
        positive_answer_list = ['y', 'Y', 'yes', 'YES']
        negative_answer_list = ['n', 'N', 'no', 'NO']
        while True:
            _key_input = input(_print_str).upper()
            if _key_input in positive_answer_list: return True
            elif _key_input in negative_answer_list: return False
            else:
                print(f"Words you can enter: {positive_answer_list}, {negative_answer_list}")
                continue
    except Exception as _e:
        print(f"ERROR!! {_e}")


if __name__ == "__main__":

    #server_host = '203.250.133.86'  # 랩실 내 라즈베리파이
    #server_host = '203.250.133.88'  # 주기호 교수님
    server_host = '127.0.0.1'
    server_port = 69
    file_name = "tmpData_1024BYTE.txt"

    keyboard_input_state = -1
    while True:
        if keyboard_input_state == -1:  # 기본값 여부
            skip_answer = input_y_n("[skip] setting value default (y/n): ")
            if skip_answer: keyboard_input_state = 3
            else: keyboard_input_state += 1
        elif keyboard_input_state == 0:  # server IP address 입력
            server_host = input("server ip: ")
            keyboard_input_state += 1
        elif keyboard_input_state == 1:  # server port 입력
            server_port = int(input("server port: "))
            keyboard_input_state += 1
        elif keyboard_input_state == 2:
            file_name = input("file name: ")
            keyboard_input_state += 1
        elif keyboard_input_state == 3:
            if os.path.isfile("./"+file_name):
                over_write_answer = input_y_n(f"해당 파일({file_name})이 이미 존재합니다. 덮어 씌우시겠습니까? (y/n): ")
                if not over_write_answer:
                    keyboard_input_state = 2
                    continue
            keyboard_input_state += 1
        else:
            break

    server_address = (server_host, server_port)
    print(f"server: {server_host}:{server_port}  /  file name: {file_name}")

    rrq_message_buffer = make_rrq_message(file_name)
    print(f"send msg = {rrq_message_buffer}")
    try:
        bytes_sent = sock.sendto(rrq_message_buffer, server_address)
        f = open(file_name, 'w', encoding='utf-8')  # 저장할 파일 열기
        last_block_number = 0  # 블럭 번호 저장
        while True:
            data, address = sock.recvfrom(BUFF_SIZE)
            data_split_list = data_check(data)  # 데이터 분류
            print(f"server[{address}] : {data_split_list[DATA_INDEX_BLOCK_NUMBER]}")

            if data_split_list[DATA_INDEX_OPCODE] == MESSAGE_OP_CODE['ERROR']:  # 에러코드 발생시 알린 후 종료
                error_str = f"ERROR!! code({data_split_list[DATA_INDEX_OPCODE]})  {data_split_list[DATA_INDEX_DATA]}"
                print(error_str)
                f.write('\n\n' + error_str)
                break

            if (data_split_list[DATA_INDEX_OPCODE] == MESSAGE_OP_CODE['DATA']) and (data_split_list[DATA_INDEX_BLOCK_NUMBER] == last_block_number + 1):  # 데이터 수신시 번호를 보고 잘 왔으면 저장
                last_block_number = data_split_list[DATA_INDEX_BLOCK_NUMBER]  # 블럭 번호 계수기
                if last_block_number >= 65535: last_block_number = 0 # 다음으로 와야할 블럭 번호. 65535 -> 1 (2byte 0~65535)
                # 데이터가 있으면 파일에 작성. 데이터가 없는 경우는 데이터가 512byte의 배수라는 의미로 마지막임을 알리기 위한 공백일 수 있음
                if data_split_list[DATA_INDEX_DATA]:
                    f.write(data_split_list[DATA_INDEX_DATA])
                # ACK 송신
                send_ack_message(sock, address, data_split_list[DATA_INDEX_BLOCK_NUMBER])
                if data_split_list[DATA_INDEX_LAST_STATE]:  # 마지막 블럭인 경우 루프 중단
                    break
        f.close()
        print(WS)
        print(WS)
        print(f"FILE NAME = {file_name}")
        print(WS)
        print(WS)

    except KeyboardInterrupt:
        print(f"키보트 입력에 의한 종료")
    except Exception as e:
        print(f"오류 발생. {e}")
    finally:
        sock.close()
        print("종료")
