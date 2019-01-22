import pygame
import sys
from pygame.locals import *

pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
color = (0, 0, 0)
color1 = (127,1,7)
color2 = (0,255,127)
color3 = (0,0,255)

speed = [1, 1]

clock = pygame.time.Clock()
#0空闲,1左键按下,2右键按下
mouse_state = 0
mouse_begin = [0,0]
mouse_end = [0,0]
move_tar = [0,0]
move_click = False
check_select = False

            
class Robot(object):
    def __init__(self,clo,ms):
        self.dir = [0,0]
        self.x = 120
        self.y = 350
        self.isselect = False
        self.color = clo
        self.move_speed = ms
        self.tar =[0,0]
    
    def Move(self):
        if check_select:
            minx = min(mouse_begin[0],mouse_end[0])
            maxx = max(mouse_begin[0],mouse_end[0])
            miny = min(mouse_begin[1],mouse_end[1])
            maxy = max(mouse_begin[1],mouse_end[1])
            if(self.x >=minx and self.x <= maxx and self.y >= miny and self.y <= maxy):
                self.isselect = True
            else:
                self.isselect = False

        if move_click:
            if self.isselect :
                self.tar = move_tar
                dx = self.tar[0]-self.x
                dy = self.tar[1]-self.y
                len=(dx*dx+dy*dy)**0.5
                if(len > 0):
                    dx /= len
                    dy /= len
                dx *= self.move_speed
                dy *= self.move_speed
                self.dir = [dx,dy]
        
        if( self.dir[0] != 0 or self.dir[1] != 0):
            dx = self.tar[0]-self.x
            dy = self.tar[1]-self.y
            len=(dx*dx+dy*dy)**0.5
            if(len < 10):
                self.x=self.tar[0]
                self.y=self.tar[1]
                self.dir = [0,0]
            self.x += self.dir[0]
            self.y += self.dir[1]
        
        if True == self.isselect :
            pygame.draw.rect(screen,color1,Rect(self.x,self.y,20,20))
        else:
            pygame.draw.rect(screen,self.color,Rect(self.x,self.y,20,20))
            

if __name__ == '__main__':
    robot = Robot(color2,1)
    
    other = Robot(color3,5)
      
    while True:
        clock.tick(60)
        move_click = False
        check_select = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            mouse_state = 1
                            check_select = True
                        elif index == 2:
                            mouse_state = 2
                if mouse_state > 0 :
                    mouse_begin = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP:
                if(mouse_state == 1):
                    check_select = True
                if(mouse_state == 2):
                    move_click = True
                    move_tar = pygame.mouse.get_pos()
                mouse_state = 0
                mouse_end = pygame.mouse.get_pos()
            elif event.type == MOUSEMOTION and mouse_state > 0:
                if(mouse_state == 1):
                    check_select = True
                mouse_end = pygame.mouse.get_pos()

        screen.fill(color)
        robot.Move()
        other.Move()
        pygame.display.flip()

    pygame.quit()
