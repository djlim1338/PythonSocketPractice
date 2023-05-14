

TFTP_MODES = {
    'unknown': 0,
    'netascii': 1,
    'octet': 2,
    'mail': 3}

TFTP_OPCODES = {
    'unknown': 0,
    'read': 1,  # RRQ
    'write': 2,  # WRQ
    'data': 3,  # DATA
    'ack': 4,  # ACKNOWLEDGMENT
    'error': 5}  # ERROR


class TFTPPackets(object):

    def __init__(self):
        self.opcodes = TFTP_OPCODES
        self.modes = TFTP_MODES
        self.to_int = lambda args: [ord(a) for a in args]
        self.to_bytes = bytearray  # lazy-invoking of bytearray ctor

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

    def request_packet(self, filename, mode, opcode):  # RRQ and WRQ packets (opcode 1 and 2)
        try:
            return self.to_bytes(self.join(0, opcode, self.to_int(filename), 0, self.to_int(mode),
                                           0))  # 2 bytes for opcode string as filename(as sequence of bytes terminated by zero-byte mode (netascii, octet) and terminated by a zero byte
        except Exception as err:
            print("request_packet", err)
            self.log("request_packet", params=(filename, mode, opcode), msg="Err: %s" % err)


tlqkf = TFTPPackets()
print(tlqkf.request_packet('test.text', 'netascii', 1))
