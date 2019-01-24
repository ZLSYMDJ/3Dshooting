import pygame
import sys
from pygame.locals import *
import socket
from threading import Thread
import time
import threading

pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)

color = (0, 0, 0)
colorper = (204,51,0)
colorother = (102,255,0)
colorlow = (143,188,143)
color1 = (240,230,140)
color2 = (220,220,220)
colorfont=(0,255,255)

N = height
M = width
H = 3
RobotSize = 20
BulletSize = 5  

grid_map = [[[0 for i in range(M)] for i in range(N)] for i in range(H+1)]
block_list = []
robot_list = []
bullet_list = []

last_move_time = 0
last_shoot_time = 0
last_tick_time = 0
self_robot_id = 0
clock = pygame.time.Clock()
lock = threading.Lock()#线程锁

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

        
def DrawMap(lv):
    global screen,color2
    if lv > H :
        return
    for b in block_list:
        if(b.lv > lv):
            pygame.draw.rect(screen, color2, b.rect)
        elif b.lv == lv :
            pygame.draw.rect(screen, color1, b.rect)
        
def DrawRobot(cl,x,y,dir):
    global screen,RobotSize
    if(dir == 0):
        pygame.draw.rect(screen,cl,Rect(x+RobotSize//2-3,y,6,RobotSize))
        pygame.draw.rect(screen,cl,Rect(x,y+RobotSize//2,RobotSize,RobotSize//2))
    elif(dir == 1):
        pygame.draw.rect(screen,cl,Rect(x,y+RobotSize//2-3,RobotSize,6))
        pygame.draw.rect(screen,cl,Rect(x,y,RobotSize//2,RobotSize))
    elif(dir == 2):
        pygame.draw.rect(screen,cl,Rect(x+RobotSize//2-3,y,6,RobotSize))
        pygame.draw.rect(screen,cl,Rect(x,y,RobotSize,RobotSize//2))
    elif(dir == 3):
        pygame.draw.rect(screen,cl,Rect(x,y+RobotSize//2-3,RobotSize,6))
        pygame.draw.rect(screen,cl,Rect(x+RobotSize//2,y,RobotSize//2,RobotSize))
            
class Robot(object):
    global screen,color1
    def __init__(self,id,x,y,z,dir):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.dir = dir
        self.is_fly = 0
        self.last_fly_time = 0
       
    def Move(self):
        print(time.time(),self.x,self.y)
        pygame.draw.rect(screen,color1,Rect(self.x,self.y,20,20))
        
class Bullet(object):
    def __init__(self,id,fa,x,y,z):
        self.id = id
        self.fa = fa
        self.x = x
        self.y = y
        self.z = z
        
def RecvMsg(client):
    global lock,robot_list,bullet_list,self_robot_id
    while True:
        data = client.recv(8192)
        data = data.decode()
        #print("-------------------------------",len(data))
        str_list = data.split('\n')
        if(len(str_list)):
            first_line = str_list[0]
            fl = first_line.split(' ')
            if(len(fl)):
                if(fl[0]=="accept"):#连接成功
                    self_robot_id = int(fl[1])
                    #print("Robot ",self_robot_id)
                elif(fl[0]=="robots"):#同步位置
                    #print(data)
                    lock.acquire()  
                    robot_list.clear()
                    bullet_list.clear()
                    cnt=0
                    start_idx = 0
                    for sl in str_list:
                        info_list = sl.split(' ')
                        if(info_list[0] == "robots"):
                            start_idx = cnt                        
                        cnt += 1
                    cnt = start_idx+1
                    for i in range(cnt,len(str_list)):
                        info_list = str_list[i].split(' ')
                        if(info_list[0] == "bullets"):
                            break
                        if(len(info_list) == 5):
                            id = int(info_list[0])
                            x = int(info_list[1])
                            y = int(info_list[2])
                            z = int(info_list[3])
                            dir = int(info_list[4])
                            
                            robot = Robot(id,x,y,z,dir)
                            robot_list.append(robot)
                            
                        cnt +=1
                        
                    #子弹
                    cnt += 1
                    for i in range(cnt,len(str_list)):
                        info_list = str_list[i].split(' ')
                        if(len(info_list) == 5):
                            id = int(info_list[0])
                            fa = int(info_list[1])
                            x = int(info_list[2])
                            y = int(info_list[3])
                            z = int(info_list[4])
                            
                            bul = Bullet(id,fa,x,y,z)
                            bullet_list.append(bul)
                            
                    #print("Bullet cnt:",len(bullet_list))
                    lock.release()
        
    client.close()
    
def GetIP():
    f = open("cfg.txt",encoding='utf-8')
    while(True):
        lines = f.readline()
        line_info = lines.split(':')
        if(len(line_info)==2):
            if(line_info[0]=="cltconnect"):
                return line_info[1]

if __name__ == '__main__':
    InitMap()
    
    client = socket.socket()
    ipstr = GetIP()
    client.connect((ipstr,11000))

    thread = Thread(target=RecvMsg, args=(client,))
    thread.setDaemon(True)
    thread.start()
    
    robot_list.clear()
    bullet_list.clear()
    cnt=0  
    while True:
        cnt +=1
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        nowtime = time.time()
        if(self_robot_id and nowtime > last_move_time + 0.01):
            last_move_time = nowtime
            key_press = pygame.key.get_pressed()
            if(key_press[K_LEFT]):
                msg = str(self_robot_id) + " 3"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_RIGHT]):
                msg = str(self_robot_id) + " 1"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_UP]):
                msg = str(self_robot_id) + " 0"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_DOWN]):
                msg = str(self_robot_id) + " 2"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_z]):
                last_shoot_time = nowtime
                msg = str(self_robot_id) + " 4"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_x]):
                last_shoot_time = nowtime
                msg = str(self_robot_id) + " 5"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_SPACE] and nowtime > last_shoot_time + 1):
                last_shoot_time = nowtime
                msg = str(self_robot_id) + " 6"
                client.send(msg.encode("utf-8"))
            elif (key_press[K_r]):
                last_shoot_time = nowtime
                msg = str(self_robot_id) + " 7"
                client.send(msg.encode("utf-8"))
            elif nowtime > last_tick_time + 0.01 :
                last_tick_time = nowtime
                msg = str(self_robot_id) + " 99"
                client.sendall(msg.encode("utf-8"))
        
        lock.acquire()
        self_level = 0
        is_over = True        
        for rbt in robot_list:
            if(self_robot_id == rbt.id):
                self_level = rbt.z
                is_over = False
                break
      
        if(self_level == 0):               
            screen.fill(color1)
        else:
            screen.fill(color)

        DrawMap(self_level)    
        for rbt in robot_list:
            if(rbt.z == self_level):
                if(self_robot_id == rbt.id):
                    DrawRobot(colorper,rbt.x,rbt.y,rbt.dir)
                else:
                    DrawRobot(colorother,rbt.x,rbt.y,rbt.dir)
            elif(rbt.z < self_level):
                DrawRobot(colorlow,rbt.x,rbt.y,rbt.dir)
        
        for bul in bullet_list:
            if(bul.z == self_level):
                if(self_robot_id == bul.fa):
                    pygame.draw.rect(screen,colorper,Rect(bul.x,bul.y,5,5))
                else:
                    pygame.draw.rect(screen,colorother,Rect(bul.x,bul.y,5,5))

        if is_over:
            fontObj=pygame.font.Font('freesansbold.ttf',32)
            txtObj=fontObj.render("Game Over,Prees R To Relife", True, colorfont)
            rectObj=txtObj.get_rect()
            rectObj.center=(300,150)
            screen.blit(txtObj,rectObj)
        else:
            if(len(robot_list) == 1):
                fontObj=pygame.font.Font('freesansbold.ttf',32)
                txtObj=fontObj.render("You Win", True, colorfont)
                rectObj=txtObj.get_rect()
                rectObj.center=(300,150)
                screen.blit(txtObj,rectObj)
                
        lock.release()
        
        pygame.display.update()
        pygame.display.flip()
        #print("Fresh")

    pygame.quit()
