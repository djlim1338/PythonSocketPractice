#!/usr/bin/python3

import socket

host = ''
port = 11125
buff_size = 128
backlog = 5

conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
conn_sock.bind(server_address)
conn_sock.listen(backlog)

while True:
    print("waiting for requests...")
    data_sock, address = conn_sock.accept()

    file_name = data_sock.recv(buff_size)

    fd = open(file_name.decode(), 'r')
    for line in fd:
        data_sock.sendall(line.encode())

    fd.close()
    data_sock.close()
