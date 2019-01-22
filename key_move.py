import pygame
import sys
from pygame.locals import *

pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
color = (0, 0, 0)
color1 = (127,1,7)

speed = [1, 1]

clock = pygame.time.Clock()

            
class Robot(object):
    def __init__(self):
        self.speed = speed
        self.x = 120
        self.y = 350
    
    def Update(self):
        if(self.x < 0 or self.x > width):
            self.speed[0] = -self.speed[0]
        if(self.y < 0 or self.y > height):
            self.speed[1] = -self.speed[1]
        self.x += self.speed[0]
        self.y += self.speed[1]
        pygame.draw.rect(screen,color1,Rect(self.x,self.y,20,20))
       
    def Move(self):
        key_press = pygame.key.get_pressed()
        if(key_press[K_LEFT]):
            self.x -= 1
        elif (key_press[K_RIGHT]):
            self.x += 1
        elif (key_press[K_UP]):
            self.y -= 1
        elif (key_press[K_DOWN]):
            self.y += 1
        pygame.draw.rect(screen,color1,Rect(self.x,self.y,20,20))

if __name__ == '__main__':
    robot = Robot()
    
    other = Robot()
      
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(color)
        robot.Move()
        other.Update()
        pygame.display.flip()

    pygame.quit()
