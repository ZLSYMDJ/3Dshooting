import pygame
import sys
from pygame.locals import *

pygame.init()
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
color = (0, 0, 0)
color1 = (127,1,7)

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(color)
    pygame.draw.rect(screen,color1,Rect(300,250,20,20))
    pygame.display.flip()

pygame.quit()
