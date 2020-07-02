import os, sys, pygame

from Pellet import Pellet
from Magic_Pellet import Magic_Pellet

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

# initialize the pellets
pellet_group = pygame.sprite.Group()
for x in range(0, WINDOWWIDTH, 25):
    pellet_group.add(Pellet(x, x))

# initialize the magic pellets
for x in range(0, WINDOWWIDTH, 50):
    pellet_group.add(Magic_Pellet(50, x))

# create pacman and set coordinates to the center of the surface
pacman = pygame.image.load('../../sprites/pacman.png')
pacman_rect = pacman.get_rect()
pacman_rect.centerx = WINDOWWIDTH/2
pacman_rect.centery = WINDOWHEIGHT/2

# blit pacman to the surface
windowSurface.blit(pacman, pacman_rect)
pellet_group.draw(windowSurface)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 