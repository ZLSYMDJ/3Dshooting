import os
import socket
import time
import threading
from threading import Thread
import pygame
import sys
from pygame.locals import *
 
g_socket_server = None
 
g_conn_pool = []

size = width, height = 600, 500
color = (0, 0, 0)
color1 = (127,1,7)
color2 = (220,220,220)

N = height
M = width
H = 3
RobotSize = 20
BulletSize = 5
Dx = [0,1,0,-1]
Dy = [-1,0,1,0]  

grid_map = [[[0 for i in range(M)] for i in range(N)] for i in range(H+1)]
block_list = []
robot_list = []
total_robot_num = 0
bullet_list = []
total_bullet = 0
del_list = []
lock = threading.Lock()#线程锁
g_need_syna = 0

class Block(object):
    def __init__(self,x,y,w,h,lv):
        self.rect = Rect(x,y,w,h)
        self.lv = lv
        for k in range(lv):
            for i in range(y,y+h):
                for j in range(x,x+w):
                    grid_map[k][i][j]=2#h层的阻挡
                    
        for i in range(y,y+h):
            for j in range(x,x+w):
                if(0 == grid_map[lv][i][j]):#注意不能把已有的阻挡重算为平地
                    grid_map[lv][i][j]=1#lv层的阻挡 
                

def InitMap():
    for k in range(H):
        for i in range(N):
            for j in range(M):
                grid_map[k][i][j]=0
                
    for i in range(N):
        for j in range(M):
            grid_map[0][i][j]=1#第0层初始都是地面
            
    b1 = Block(100,100,300,200,1)
    b2 = Block(200,200,400,200,1)
    b3 = Block(100,300,300,200,2)
    block_list.append(b1)
    block_list.append(b2)
    block_list.append(b3)
        
def OnBlock(x,y,z,w,h):
    if z > H:
        return 1
    if(x<0 or x+20>=M or y<0 or y+20>=N):
        return 1
    onblock = 0
    for i in range(x,x+w):
        if(grid_map[z][y][i]>1 or grid_map[z][y+h][i]>1):
            onblock = 1
            break
    for i in range(y,y+h):
        if(grid_map[z][i][x]>1 or grid_map[z][i][x+w]>1):
            onblock = 1
            break
            
    return onblock
    
def JudgeHit(fa,x,y,z):
    global robot_list
    for rbt in robot_list:
        if fa == rbt.id:
            continue
        if(z == rbt.z and x>=rbt.x and x<rbt.x+20 and y>=rbt.y and y<rbt.y+20):
            robot_list.remove(rbt)
            return True
            
class Robot(object):
    def __init__(self,id):
        self.id=id
        self.x = 10
        self.y = 10
        self.z = 0
        self.dir = 0
        self.is_fly = 0
        self.last_fly_time = 0
       
    def Move(self, move_dir):
        tx = self.x
        ty = self.y
        if(move_dir < 4):
            self.dir = move_dir
        if(move_dir == 3):
            tx -= 1
        elif (move_dir == 1):
            tx += 1
        elif (move_dir == 0):
            ty -= 1
        elif (move_dir == 2):
            ty += 1
        elif (move_dir == 4):#飞行
            self.is_fly = 1
            nowtime = time.time()
            if(nowtime > self.last_fly_time + 1):
                self.last_fly_time = nowtime
                self.z += 1
                if(self.z > H):
                    self.z = H
        elif (move_dir == 5):#下落
            self.is_fly = 0
            
        if(tx>=0 and tx+20<M and ty>=0 and ty+20<N):
            onblock = 0#是否碰到阻挡
            h = self.z
            for i in range(tx,tx+20):
                if(grid_map[h][ty][i] > 1 or grid_map[h][ty+19][i] > 1):
                    onblock = 1
                    break
            for i in range(ty,ty+20):
                if(grid_map[h][i][tx] > 1 or grid_map[h][i][tx+19] > 1):
                    onblock = 1
                    break
                    
            if(onblock == 0):
                self.x=tx
                self.y=ty

            onhole = 1#是否在空洞中
            px = self.x
            py = self.y
            if(grid_map[h][py][px] or grid_map[h][py+19][px] 
            or grid_map[h][py][px+19] or grid_map[h][py+19][px+19]):
                onhole = 0
            
            if(onhole and 0 == self.is_fly):
                self.z -= 1
 
class Bullet(object):
    def __init__(self,id,fa,x,y,z,dir,ms):
        #print("id=",id)
        self.id = id
        self.fa = fa
        self.x = x
        self.y = y
        self.z = z
        self.dir = dir
        self.ms = ms
        
    def Move(self):
        global total_bullet,del_list,BulletSize,g_need_syna
        tx = self.x + Dx[self.dir]
        ty = self.y + Dy[self.dir]
        tz = self.z
        if(JudgeHit(self.fa,tx,ty,tz)):
            del_list.append(self.id)
            g_need_syna = True           
        elif(OnBlock(tx,ty,tz,BulletSize,BulletSize)):
            del_list.append(self.id)
            g_need_syna = True               
        else:
            self.x = tx
            self.y = ty
            #pygame.draw.rect(screen,color1,Rect(self.x,self.y,BulletSize,BulletSize))

def accept_client():
    global total_robot_num,lock,g_need_syna
    while True:
        client, _ = g_socket_server.accept()# 阻塞，等待客户端连接
        g_conn_pool.append(client)
        thread = Thread(target=message_handle, args=(client,))
        thread.setDaemon(True)
        thread.start()
        lock.acquire()
        total_robot_num += 1
        robot = Robot(total_robot_num)
        robot_list.append(robot)
        g_need_syna = 1
        res_msg = "accept "+str(total_robot_num)
        client.send(bytes(res_msg,'utf-8'))
        #print(res_msg)
        lock.release()
 
 
def message_handle(client):
    global lock,g_need_syna,total_bullet,RobotSize,BulletSize
    while True:
        data = client.recv(8192)
        data = data.decode('utf-8')
        if len(data) == 0:
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
        else:
            #print(data)
            str_list = data.split(' ')
            if(len(str_list)>=2):
                robot_id = int(str_list[0])
                move_dir = int(str_list[1])
                lock.acquire()
                if(7 == move_dir):
                    relife = True
                    for rbt in robot_list:
                        if rbt.id == robot_id:
                            relife = False
                    if(relife):
                        robot = Robot(robot_id)
                        robot_list.append(robot)
                        g_need_syna = 1
                elif(move_dir <= 6):#0123方向，45飞行，6射击,7复活
                    for rbt in robot_list:
                        if rbt.id == robot_id:
                            if(move_dir < 6):
                                rbt.Move(move_dir)
                            else:
                                px = rbt.x + RobotSize//2 - BulletSize//2
                                py = rbt.y + RobotSize//2 - BulletSize//2
                                bul = Bullet(total_bullet,rbt.id,px,py,rbt.z,rbt.dir,RobotSize)
                                print("bullet ",bul.fa,bul.x,bul.y,bul.z,bul.dir)
                                bullet_list.append(bul)
                                total_bullet += 1
                            
                g_need_syna = 1
                lock.release()
            #client.send(bytes(res,'utf-8'))

def GetIP():
    f = open("cfg.txt",encoding='utf-8')
    while(True):
        lines = f.readline()
        line_info = lines.split(':')
        if(len(line_info)==2):
            if(line_info[0]=="svrlisten"):
                return line_info[1]
                       
g_socket_server
g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
ipstr = GetIP()
print("ip=",ipstr)
g_socket_server.bind((ipstr, 11000) )
g_socket_server.listen(5)

thread = Thread(target=accept_client)
thread.setDaemon(True)
thread.start()
# 主线程逻辑
while True:
    InitMap()
      
    while True:
        lock.acquire()#同步机器人位置
        for bul in bullet_list:#更新子弹
            bul.Move()
            #print("bullet ",bul.fa,bul.x,bul.y,bul.dir)
        for id in del_list:
            for bul in bullet_list:
                if bul.id == id :
                    bullet_list.remove(bul)
                    break
        if(g_need_syna or len(bullet_list)):
            syna_msg = []
            syna_msg.append("robots\n")
            for rbt in robot_list:
                syna_msg.append(str(rbt.id)+" ")
                syna_msg.append(str(rbt.x)+" ")
                syna_msg.append(str(rbt.y)+" ")
                syna_msg.append(str(rbt.z)+" ")
                syna_msg.append(str(rbt.dir)+"\n")
                
            syna_msg.append("bullets\n")
            for bul in bullet_list:
                syna_msg.append(str(bul.id)+" ")
                syna_msg.append(str(bul.fa)+" ")
                syna_msg.append(str(bul.x)+" ")
                syna_msg.append(str(bul.y)+" ")
                syna_msg.append(str(bul.z)+"\n")
            syna_str = ''.join(syna_msg)
            
            del_con_list = []
            for clt in g_conn_pool:
                try:
                    clt.sendall(bytes(syna_str,'utf-8'))
                except Exception as err:
                    print(err)
                    del_con_list.append(clt)
                    
            for clt in del_con_list:
                g_conn_pool.remove(clt)
            g_need_syna = 0
            #print("Syna! ",syna_str)

        lock.release()
        time.sleep(0.005)

