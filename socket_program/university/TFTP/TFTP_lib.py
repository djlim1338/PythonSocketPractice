"""

 TFTP_lib.py
 djlim

"""

import struct
import socket
import os
import sys
import time
import validators


BUFF_SIZE = 2048
DATA_MAX_SIZE = 512
MODE = 'netascii'  # netascii(=text)
TFTP_MESSAGE_SPACE = 0x00  # 구분 공백
SOCKET_TIME_OUT = 5
SOCKET_TIME_OUT_MAX = 3
TFTP_ROOT_DIR = './TFTP_ROOT/'  # server TFTP data root dir
TFTP_CLIENT_ROOT_DIR = './TFTP_CLIENT_ROOT/'  # client TFTP data root dir
WS = "-----------------------------------------------------------------------------------------------------------------------------"  # print출력시 벽

COMMAND_ACTION_LIST = ['GET', 'PUT']  # 명령어 리스트
COMMAND_EXIT_LIST = ['EXIT', 'QUIT']  # 종료 명령어
COMMAND_RESET_LIST = ['RESET']  # 리셋 명령어

STATE_CODE = {  # 무한 반복 상태 코드
    'INPUT_SKIP': 0,
    'INPUT_HOST': 1,
    'INPUT_PORT': 2,
    'PRINT_ADDRESS': 3,
    'INPUT_COMMAND': 4,
    'PROCESSING_COMMAND': 5
}

COMMAND_OPCODE = {  # 각 명령어에 해당하는 동작
    'GET': 'RRQ',
    'PUT': 'WRQ'
}

MESSAGE_OP_CODE = {  # op code
    'RRQ': 0x0001,
    'WRQ': 0x0002,
    'DATA': 0x0003,
    'ACK': 0x0004,
    'ERROR': 0x0005
}

ERROR_CODE = {  # error code
    0x00: "Not defined, see error message (if any).",
    0x01: "File not found.",
    0x02: "Access violation.",
    0x03: "Disk full or allocation exceeded.",
    0x04: "Illegal TFTP operation.",
    0x05: "Unknown transfer ID.",
    0x06: "File already exists",
    0x07: "No such user."
}


def input_y_n(print_str):  # 터미널에서 YES/NO(Y/N) 받고 T/F 출력.
    try:
        positive_answer_list = ['Y', 'YES']
        negative_answer_list = ['N', 'NO']
        while True:
            _key_input = input(print_str).upper()
            if _key_input in positive_answer_list: return True
            elif _key_input in negative_answer_list: return False
            elif _key_input in COMMAND_EXIT_LIST: sys.exit(0) # 종료 코드시 코드 종료
            else:
                print(f"Words you can enter: {positive_answer_list}, {negative_answer_list}")
                continue
    except Exception as _e:
        print(f"ERROR!! {_e}")


def data_check(in_byte_data):  # Data packet check
    opcode = int.from_bytes(in_byte_data[:2], 'big')
    block_number = int.from_bytes(in_byte_data[2:4], 'big')
    last_block = False

    if opcode == MESSAGE_OP_CODE['ERROR']:
        data_bytes = in_byte_data[4:-1]
    else:
        data_bytes = in_byte_data[4:]

    data_str = data_bytes.decode()
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


def rq_check(in_byte_data):  # server RRQ/QRQ check
    opcode = int.from_bytes(in_byte_data[:2], 'big')

    space_index = []
    for counter in range(len(in_byte_data)):
        one_byte = int.from_bytes(in_byte_data[counter:counter + 1], 'big')
        if one_byte == TFTP_MESSAGE_SPACE:
            space_index.append(counter)

    file_name = in_byte_data[2:space_index[1]]
    mode = in_byte_data[space_index[1]+1:space_index[2]]

    return_dgram_dic = {
        'opcode': opcode,
        'filename': file_name,
        'mode': mode
    }

    return return_dgram_dic


def make_rq_message(opcode, file_name, mode):  # make WRQ/QQR message
    pack_str = f"!H{len(file_name)}sB{len(mode)}sB"
    return struct.pack(pack_str, MESSAGE_OP_CODE[opcode], file_name.encode(), TFTP_MESSAGE_SPACE, mode.encode(), TFTP_MESSAGE_SPACE)


def make_data_message(opcode, block_number, data):  # make data message
    pack_str = f"!HH{len(data)}s"
    return struct.pack(pack_str, MESSAGE_OP_CODE[opcode], block_number, data.encode())


def make_ack_message(data_block_number):  # make ACK message
    pack_str = f"!2H"
    return struct.pack(pack_str, MESSAGE_OP_CODE['ACK'], data_block_number)


def make_error_message(error_number, error_message):  # make ERROR message
    pack_str = f"!2H{len(error_message)}sB"
    return struct.pack(pack_str, MESSAGE_OP_CODE['ERROR'], error_number, error_message.encode(), TFTP_MESSAGE_SPACE)


def send_rq(socket_obj, address, opcode, file_name):  # RRQ/WRQ send
    send_msg = make_rq_message(opcode, file_name, MODE)  # RQ 바이트열 생성
    socket_obj.sendto(send_msg, address)  # RQ 송신
    timeout_counter = 0
    while True:
        try:
            data, recv_address = socket_obj.recvfrom(BUFF_SIZE)
        except TimeoutError:
            socket_obj.sendto(send_msg, address)  # RQ 송신
            timeout_counter += 1
            if timeout_counter > SOCKET_TIME_OUT_MAX:
                raise
            continue
        return data, recv_address


def pop_data_split(put_data):  # 보낼 데이서 512바이트씩 분리하여 리스트에 저장
    data_piece = put_data[:DATA_MAX_SIZE]
    if put_data:
        put_data = put_data[DATA_MAX_SIZE:]
    else:
        put_data = ""
    return data_piece, put_data


def rrq_server(socket_obj, address, file_name):  # server RRQ(GET)=
    read_file_pointer = open(TFTP_ROOT_DIR + file_name, 'r', encoding='utf-8')
    last_block_number = 1  # 블럭 번호 저장
    data_one_block = ""  # 한 블럭 데이터 저장
    timeout_counter = 0
    print(WS)
    while True:
        if data_one_block == "":
            data_one_block = read_file_pointer.read(DATA_MAX_SIZE)
        send_dgram_msg = make_data_message('DATA', last_block_number, data_one_block)  # 데이터
        socket_obj.sendto(send_dgram_msg, address)
        try:
            recv_data, address = socket_obj.recvfrom(BUFF_SIZE)  # 수신 (대기)
        except TimeoutError:
            timeout_counter += 1
            if timeout_counter >= SOCKET_TIME_OUT_MAX:
                raise
            print("timeout DATA resend")
            continue
        data_split_list = data_check(recv_data)
        if len(data_one_block) < DATA_MAX_SIZE:  # 마지막으로 수신한 데이터의 길이<512 = 마지막 데이터
            break

        # 블럭번호 & opcode 확인
        if (data_split_list['opcode'] == MESSAGE_OP_CODE['ACK']) and (data_split_list['number'] == last_block_number):
            last_block_number += 1
            if last_block_number > 65535:
                last_block_number = 0
            data_one_block = ""
    read_file_pointer.close()
    print(f"RRQ file done.")
    print(WS)


def get_file(socket_obj, address, opcode, file_name):  # client
    send_msg = make_rq_message(opcode, file_name, MODE)  # RRQ 바이트열 생성
    socket_obj.sendto(send_msg, address)  # RRQ 송신
    #print(send_msg)
    write_file = open(TFTP_CLIENT_ROOT_DIR + file_name, 'w', encoding='utf-8')  # 파일 쓰기로 open
    last_block_number = 1  # 블럭 번호 저장
    timeout_counter = 0
    print(WS)
    while True:
        try:
            data, recv_address = socket_obj.recvfrom(BUFF_SIZE)  # 수신 (대기)
        except TimeoutError:
            socket_obj.sendto(send_msg, address)  # RRQ 송신
            timeout_counter += 1
            if timeout_counter >= SOCKET_TIME_OUT_MAX:
                write_file.close()
                raise
            continue
        data_split_list = data_check(data)  # 데이터 분류

        if (data_split_list['opcode'] == MESSAGE_OP_CODE['DATA']) and (
                data_split_list['number'] == last_block_number):  # 데이터 수신시 번호를 보고 잘 왔으면 저장
            # ACK 송신
            ack_msg = make_ack_message(data_split_list['number'])
            socket_obj.sendto(ack_msg, recv_address)

            last_block_number += 1  # 블럭 번호 계수기
            if last_block_number > 65535:
                last_block_number = 0  # 다음으로 와야할 블럭 번호. 65536 -> 0 (2byte 0~65535)
            # 데이터가 있으면 파일에 작성. 데이터가 없는 경우는 데이터가 512byte의 배수라는 의미로 마지막임을 알리기 위한 공백일 수 있음
            if data_split_list['data']:
                write_file.write(data_split_list['data'])
            if data_split_list['last']:  # 마지막 블럭인 경우 루프 중단
                break
        elif data_split_list['opcode'] == MESSAGE_OP_CODE['ERROR']:  # 에러코드 발생시 알린 후 종료
            error_str = f"ERROR!! code({data_split_list['opcode']})  {data_split_list['data']}"
            print(error_str)
            write_file.write('\n\n' + error_str)
            print(WS)
            break
    write_file.close()
    print(f"get file done.")
    print(WS)


def wrq_server(socket_obj, address, file_name):  # server WRQ(PUT)
    write_file = open(TFTP_ROOT_DIR + file_name, 'w', encoding='utf-8')  # 파일 쓰기로 open
    last_block_number = 0  # 블럭 번호 저장
    next_block_number = last_block_number + 1
    timeout_counter = 0
    print(WS)
    while True:
        send_ack_msg = make_ack_message(last_block_number)  # ACK 바이트열 생성
        socket_obj.sendto(send_ack_msg, address)  # ACK 송신
        try:
            data, recv_address = socket_obj.recvfrom(BUFF_SIZE)  # 수신 (대기)
        except TimeoutError:
            timeout_counter += 1
            if timeout_counter >= SOCKET_TIME_OUT_MAX:
                write_file.close()
                raise
            print("timeout ACK resend")
            continue

        data_split_list = data_check(data)  # 데이터 분류
        #print(f"WRQ from client[{address}] : no.{data_split_list['number']}")

        if (data_split_list['opcode'] == MESSAGE_OP_CODE['DATA']) and (
                data_split_list['number'] == (next_block_number)):  # 데이터 수신시 번호를 보고 잘 왔으면 저장
            last_block_number += 1  # 블럭 번호 계수기
            if last_block_number > 65535:
                last_block_number = 0  # 다음으로 와야할 블럭 번호. 65536 -> 0 (2byte 0~65535)
            next_block_number = last_block_number + 1
            if next_block_number > 65535:
                next_block_number = 0  # 다음으로 와야할 블럭 번호. 65536 -> 0 (2byte 0~65535)
            # 데이터가 있으면 파일에 작성. 데이터가 없는 경우는 데이터가 512byte의 배수라는 의미로 마지막임을 알리기 위한 공백일 수 있음
            if data_split_list['data']:
                write_file.write(data_split_list['data'])

        if data_split_list['last']:  # 마지막 블럭인 경우 마지막 ACK 송신 후 루프 중단
            send_ack_msg = make_ack_message(last_block_number)  # ACK 바이트열 생성
            socket_obj.sendto(send_ack_msg, address)  # ACK 송신
            break
    write_file.close()
    print(f"server WRQ done.")
    print(WS)


def put_file(socket_obj, address, opcode, file_name):  # client
    send_msg = make_rq_message(opcode, file_name, MODE)  # WRQ 바이트열 생성
    socket_obj.sendto(send_msg, address)  # WRQ 송신
    #print(send_msg)
    read_file_pointer = open(TFTP_CLIENT_ROOT_DIR + file_name, 'r', encoding='utf-8')
    last_block_number = 0  # 블럭 번호 저장
    data_one_block = ""
    last_ack_state = False
    timeout_counter = 0
    print(WS)
    while True:
        try:
            data, recv_address = socket_obj.recvfrom(BUFF_SIZE)  # 수신 (대기)
        except TimeoutError:
            socket_obj.sendto(send_msg, address)  # WRQ 송신
            timeout_counter += 1
            if timeout_counter > SOCKET_TIME_OUT_MAX:
                raise
            print("timeout resend")
            continue
        data_split_list = data_check(data)  # 데이터 분류
        if last_ack_state:
            break

        if data_split_list['opcode'] == MESSAGE_OP_CODE['ERROR']:  # 에러코드 발생시 알린 후 종료
            error_str = f"ERROR!! code({data_split_list['opcode']})  {data_split_list['data']}"
            print(error_str)
            print(WS)
            return
        elif (data_split_list['opcode'] == MESSAGE_OP_CODE['ACK']) and (
                data_split_list['number'] == last_block_number):  # 블럭번호 확인 후 데이터 송신
            last_block_number += 1
            if last_block_number > 65535:
                last_block_number = 0
            data_one_block = read_file_pointer.read(DATA_MAX_SIZE)
            send_dgram_msg = make_data_message('DATA', last_block_number, data_one_block)  # 데이터
            socket_obj.sendto(send_dgram_msg, recv_address)

            if len(data_one_block) < 512:
                last_ack_state = True

    read_file_pointer.close()
    print(f"put file done.")
    print(WS)
