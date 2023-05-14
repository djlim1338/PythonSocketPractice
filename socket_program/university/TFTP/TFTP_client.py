#
# TFTP_client.py
# djlim
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


class TFTPClient:
    _file_name = ""
    # _dgram_dic = {}

    def __init__(self, server_host, server_port):
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = (server_host, server_port)

    def get_address(self):
        return self._address

    def send_message(self, opcode, file_name, mode=RRQ_MODE):
        self._file_name = file_name
        pack_str = f"!H{len(file_name)}sb{len(mode)}sb"
        send_byte_data = struct.pack(pack_str, opcode, file_name.encode(), TFTP_MESSAGE_SPACE, mode.encode(),
                                     TFTP_MESSAGE_SPACE)
        self._udp_socket.sendto(send_byte_data, self._address)

    def recv_message(self):
        while True:
            data, address = self._udp_socket.recvfrom(BUFF_SIZE)
            byte_data_split_list = data.hex('-').split('-')  # 헥사로 표현하여 1비트씩 끊어서 리스트에 저장. 자료형은 str

            opcode = ''.join(byte_data_split_list[0:2])  # opcode 추출
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

            return_dic = {
                "opcode": opcode,
                "number": block_number,
                "data": data_str,
                "last": last_block,
                "address": address
            }
            return return_dic

    def send_ack(self, number, address):
        pack_str = f"!2H"
        send_byte_data = struct.pack(pack_str, ACK_OPCODE, number)
        self._udp_socket.sendto(send_byte_data, address)
