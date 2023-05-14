import socket

server = 'www.pcu.ac.kr'
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server, port))
request = "GET / HTTP/1.1\r\nHost: "+server+"\r\n\r\n"
sock.send(request.encode())
response = sock.recv(4096)
print(response)
