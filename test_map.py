import pygame
import sys
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
            
class Robot(object):
    def __init__(self):
        self.x = N//2
        self.y = M//2
       
    def Move(self):
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
        if(tx>=0 and tx+20<M and ty>=0 and ty+20<N):
            onblock = 0
            for i in range(tx,tx+20):
                if(grid_map[ty][i] or grid_map[ty+19][i]):
                    onblock = 1
                    break
            for i in range(ty,ty+20):
                if(grid_map[i][tx] or grid_map[i][tx+19]):
                    onblock = 1
                    break
            if(onblock == 0):
                self.x=tx
                self.y=ty

        pygame.draw.rect(screen,color1,Rect(self.x,self.y,20,20))

if __name__ == '__main__':
    InitMap()
    robot = Robot()
      
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(color)
        robot.Move()
        DrawMap()
        pygame.display.flip()

    pygame.quit()
