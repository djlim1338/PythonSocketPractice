#
# struct_test.py
# djlim
#

import struct

BUFF_SIZE = 512
RRQ_OPCODE = 0x0001  # RRQ(read)
RRQ_MODE = 'netascii'  # netascii(=text)
TFTP_MESSAGE_SPACE = 0x00  # 구분 공백


def join(self, *arrs):
    res = []

    try:
        for arr in arrs:
            if not isinstance(arr, list):
                arr = [arr]
            res += arr
    except Exception as err:
        print("join", err)
    return res

def make_rrq_message(in_file_name):
    pack_str = f"!h{len(in_file_name)}sb{len(RRQ_MODE)}sb"

    opcode_byte = struct.pack('!h', RRQ_OPCODE)
    file_name_byte = struct.pack(f'!{len(in_file_name)}s', in_file_name.encode())
    mode_byte = struct.pack(f'!{len(RRQ_MODE)}s', RRQ_MODE.encode())
    space_byte = struct.pack('!b', TFTP_MESSAGE_SPACE)

    print(pack_str)
    print(opcode_byte, file_name_byte, mode_byte, space_byte)
    print(opcode_byte + file_name_byte + space_byte + mode_byte + space_byte)

    obj1 = struct.pack(pack_str, RRQ_OPCODE, in_file_name.encode(), TFTP_MESSAGE_SPACE, RRQ_MODE.encode(), TFTP_MESSAGE_SPACE)
    obj2 = bytearray(obj1)
    print(obj1)
    print(obj2)
    print(type(obj1))
    print(type(obj2))


print(f"!h => {struct.pack('!h', 0x0001)}")
print(f"h => {struct.pack('h', 0x0001)}")

print(f"!b => {struct.pack('!b', 0x00)}")
print(f"b => {struct.pack('b', 0x00)}")

print(f"5s => {struct.pack('5s', 'ABCDE'.encode())}")
print(f"!5s => {struct.pack('!5s', 'ABCDE'.encode())}")

print(f"5p => {struct.pack('5p', 'ABCDE'.encode())}")
print(f"!5p => {struct.pack('!5p', 'ABCDE'.encode())}")


print(bytearray(join((0, 0x01, 0, 0))))

in_file_name = "textText.txt"
make_rrq_message(in_file_name)


