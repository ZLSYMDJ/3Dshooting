import socket
from time import ctime

HOST = "127.0.0.1"
PORT = 11000
BUFSIZE = 1024
ADDR = (HOST, PORT)

serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()
    
    while True:
        print("wait client msg")
        data = clientsocket.recv(BUFSIZE)
        if not data:
            break
        data = data.decode('utf-8')
        print(data)
        res = "recv %s" % data
        clientsocket.send(bytes(res,'utf-8'))
    clientsocket.close()
serversocket.close()
