import os
import socket
import time
from threading import Thread

ADDRESS = ('127.0.0.1', 11000)#ip地址和端口
 
g_socket_server = None#负责监听的socket
 
g_conn_pool = []#连接池

#接收客户端连接
def acc_clt():
    while True:
        clt, addr = g_socket_server.accept()
        print("one client connect!")
        g_conn_pool.append(clt)
        thread = Thread(target=deal_msg,args=(clt,))#创建一个新的线程，用来处理刚连进来的这个客户端的消息
        thread.setDaemon(True)#设置为守护线程
        thread.start()
        
#处理客户端的消息
def deal_msg(client):
    while True:
        data = client.recv(1024)
        data = data.decode('utf-8')
        if len(data) == 0:
            client.close()
            g_conn_pool.remove(client)
            print("remove one client!")
        else:
            print(data)
            res = "recv %s" % data
            client.send(bytes(res,'utf-8'))#給客户端回包
            
g_socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
g_socket_server.bind(ADDRESS)
g_socket_server.listen(5)#绑定端口并开始监听

thread = Thread(target=acc_clt)#等待连接的线程
thread.setDaemon(True)
thread.start()

print("main loop begin!")
while True:
    #主线程逻辑
    #do something
    #print("main thread running!")
    time.sleep(0.1)
