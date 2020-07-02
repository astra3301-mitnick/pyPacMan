import os, sys, pygame

from pygame.locals import *

# initialize pygame
pygame.init()
mainClock = pygame.time.Clock()

# constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
windowSurface.fill(BLACK)

# create square
square = pygame.draw.rect(windowSurface, WHITE, pygame.Rect(0, 0, 32, 32))

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



    