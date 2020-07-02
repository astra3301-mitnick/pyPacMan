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

# create pacman and set coordinates to the center of the surface
pacman = pygame.image.load('../../sprites/pacman.png')
pacman_rect = pacman.get_rect()
pacman_rect.centerx = WINDOWWIDTH/2
pacman_rect.centery = WINDOWHEIGHT/2

# blit pacman to the surface
windowSurface.blit(pacman, pacman_rect)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 