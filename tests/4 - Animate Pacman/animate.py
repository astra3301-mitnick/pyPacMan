import os, sys, pygame

from Pacman import Pacman

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

# initialize movement variables
moveLeft = False
moveRight = False
moveDown = False
moveUp = False

# pixels per loop
MOVESPEED = 6

# create pacman and set coordinates to the center of the surface
pacman = Pacman(WINDOWWIDTH/2, WINDOWHEIGHT/2, MOVESPEED)
pacman_group = pygame.sprite.GroupSingle(pacman)

# blit pacman to the surface
pacman_group.draw(windowSurface)

# update the game
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_UP:
                moveLeft  = False
                moveRight = False
                moveDown  = False
                moveUp    = True
            if event.key == K_DOWN:
                moveLeft  = False
                moveRight = False
                moveDown  = True
                moveUp    = False
            if event.key == K_LEFT:
                moveLeft  = True
                moveRight = False
                moveDown  = False
                moveUp    = False
            if event.key == K_RIGHT:
                moveLeft  = False
                moveRight = True
                moveDown  = False
                moveUp    = False
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
                
    # move the sprite(pacman)
    pacman_group.update(moveUp, moveDown, moveLeft, moveRight)
    
    # redraw the background and sprite
    windowSurface.fill(BLACK)
    pacman_group.draw(windowSurface)
    
    # update the game
    pygame.display.update()
    mainClock.tick(16)