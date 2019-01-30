import socket

HOST = "127.0.0.1"
PORT = 11000
BUFSIZE = 1024
ADDR = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)

while True:
    data = input(">>>")
    if not data:
        break
    
    s.send(bytes(data,'utf-8'))
    data = s.recv(BUFSIZE)
    if not data:
        break
    print(data.decode('utf-8'))
s.close()
