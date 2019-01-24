import pygame
import sys
import time
from pygame.locals import *

pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
color = (0, 0, 0)
colorper = (204,51,0)
colorother = (102,255,0)
color1 = (240,230,140)
color2 = (220,220,220)

N = height
M = width
H = 3

grid_map = [[[0 for i in range(M)] for i in range(N)] for i in range(H+1)]
block_list = []
bullet_list = []
del_list = []
total_bullet = 0
Dx = [0,1,0,-1]
Dy = [-1,0,1,0]
RobotSize = 20
BulletSize = 5     


clock = pygame.time.Clock()

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
    if lv > H :
        return
    for b in block_list:
        if(b.lv > lv):
            pygame.draw.rect(screen, color2, b.rect)
        elif b.lv == lv :
            pygame.draw.rect(screen, color1, b.rect)
            

class Robot(object):
    def __init__(self):
        self.x = 10
        self.y = 10
        self.z = 0
        self.is_fly = 0
        self.last_fly_time = 0
       
    def Move(self):
        global grid_map
        if(self.z > H):
            self.z -= 1
            pygame.draw.rect(screen,color1,Rect(self.x,self.y,20,20))
            return
            
        key_press = pygame.key.get_pressed()
        tx = self.x
        ty = self.y
        if(key_press[K_LEFT]):
            tx -= 1
        elif (key_press[K_RIGHT]):
            tx += 1
        elif (key_press[K_UP]):
            ty -= 1
        elif (key_press[K_DOWN]):
            ty += 1
        elif (key_press[K_z]):
            self.is_fly = 1
            nowtime = time.time()
            if(nowtime > self.last_fly_time + 1):
                self.last_fly_time = nowtime
                self.z += 1
                if(self.z > H):
                    self.z = H
        elif (key_press[K_x]):
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

            onhole = 1#是否走到塌陷区
            px = self.x
            py = self.y
            if(grid_map[h][py][px] or grid_map[h][py+19][px] 
            or grid_map[h][py][px+19] or grid_map[h][py+19][px+19]):
                onhole = 0
            
            if(onhole and 0 == self.is_fly):
                self.z -= 1    
            
##################################################
            
InitMap()
robot = Robot()

while True:
    global grid_map
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    robot.Move()
    z = robot.z
    y = robot.y
    x = robot.x

    if(0 == robot.z):
        screen.fill(color1)
    else:
        screen.fill(color)
        
    DrawMap(robot.z)
    pygame.draw.rect(screen,colorper,Rect(robot.x,robot.y,20,20))
    
    pygame.display.flip()
    

pygame.quit()
        
