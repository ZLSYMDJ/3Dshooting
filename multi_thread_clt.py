import socket
from threading import Thread

def RecvMsg(client):
    while True:
        data = client.recv(1024)
        print("recv:>",data.decode())
        
    client.close()


client = socket.socket()
client.connect(("127.0.0.1",11000))

thread = Thread(target=RecvMsg, args=(client,))
thread.setDaemon(True)
thread.start()

while True:
    msg = input(">>>").strip()
    if len(msg) ==0:continue
    client.send(msg.encode("utf-8"))
