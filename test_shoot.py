import pygame
import sys
import time
from pygame.locals import *

pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
color = (0, 0, 0)
color1 = (127,1,7)
color2 = (220,220,220)

N = height
M = width

grid_map = [[0 for i in range(M)] for i in range(N)]
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
    def __init__(self,x,y,w,h):
        self.rect = Rect(x,y,w,h)
        for i in range(y,y+h):
            for j in range(x,x+w):
                grid_map[i][j]=1
                

def InitMap():
    for i in range(N):
        for j in range(M):
            grid_map[i][j]=0
            
    for i in range(0,M,50):
        b1 = Block(i,0,10,100)
        b2 = Block(i,200,10,100)
        b3 = Block(i,400,10,100)
        block_list.append(b1)
        block_list.append(b2)
        block_list.append(b3)

def DrawMap():
    for b in block_list:
        pygame.draw.rect(screen, color2, b.rect)
        
def OnBlock(x,y,w,h):
    if(x<0 or x+w>=M or y<0 or y+w>=N):
        return 1
    onblock = 0
    for i in range(x,x+w):
        if(grid_map[y][i] or grid_map[y+h][i]):
            onblock = 1
            break
    for i in range(y,y+h):
        if(grid_map[i][x] or grid_map[i][x+w]):
            onblock = 1
            break
            
    return onblock
 
class Robot(object):
    def __init__(self):
        self.x = N//2 + 10
        self.y = M//2 + 10
        self.dir = 0
        self.shoot_time = 0
       
    def Update(self):
        global total_bullet
        key_press = pygame.key.get_pressed()
        tx = self.x
        ty = self.y
        if(key_press[K_LEFT]):
            tx -= 1
            self.dir = 3
        elif (key_press[K_RIGHT]):
            tx += 1
            self.dir = 1
        elif (key_press[K_UP]):
            ty -= 1
            self.dir = 0
        elif (key_press[K_DOWN]):
            ty += 1
            self.dir = 2
        elif (key_press[K_SPACE]):
            nowtime = time.time()
            if(nowtime > self.shoot_time + 1):
                self.shoot_time = nowtime
                px = self.x + RobotSize//2 - BulletSize//2
                py = self.y + RobotSize//2 - BulletSize//2
                bul = Bullet(total_bullet,px,py,self.dir,RobotSize)
                bullet_list.append(bul)
                total_bullet += 1

        if(OnBlock(tx,ty,RobotSize,RobotSize) == 0):
            self.x=tx
            self.y=ty
        if(self.dir == 0):
            pygame.draw.rect(screen,color1,Rect(self.x+RobotSize//2-3,self.y,6,RobotSize))
            pygame.draw.rect(screen,color1,Rect(self.x,self.y+RobotSize//2,RobotSize,RobotSize//2))
        elif(self.dir == 1):
            pygame.draw.rect(screen,color1,Rect(self.x,self.y+RobotSize//2-3,RobotSize,6))
            pygame.draw.rect(screen,color1,Rect(self.x,self.y,RobotSize//2,RobotSize))
        elif(self.dir == 2):
            pygame.draw.rect(screen,color1,Rect(self.x+RobotSize//2-3,self.y,6,RobotSize))
            pygame.draw.rect(screen,color1,Rect(self.x,self.y,RobotSize,RobotSize//2))
        elif(self.dir == 3):
            pygame.draw.rect(screen,color1,Rect(self.x,self.y+RobotSize//2-3,RobotSize,6))
            pygame.draw.rect(screen,color1,Rect(self.x+RobotSize//2,self.y,RobotSize//2,RobotSize))
            
class Bullet(object):
    def __init__(self,id,x,y,dir,ms):
        self.id = id
        self.x = x
        self.y = y
        self.dir = dir
        self.ms = ms
        
    def Move(self):
        tx = self.x + Dx[self.dir]
        ty = self.y + Dy[self.dir]
        if(OnBlock(tx,ty,BulletSize,BulletSize)):
            del_list.append(self.id)
        else:
            self.x = tx
            self.y = ty
            pygame.draw.rect(screen,color1,Rect(self.x,self.y,BulletSize,BulletSize))
        

if __name__ == '__main__':
    InitMap()
    robot = Robot()
      
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(color)
        robot.Update()
        for bul in bullet_list:
            bul.Move()
        for id in del_list:
            for bul in bullet_list:
                if bul.id == id :
                    bullet_list.remove(bul)
                    break
        del_list.clear()
        DrawMap()
        pygame.display.flip()

    pygame.quit()
