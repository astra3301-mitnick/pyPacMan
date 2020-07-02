import os, sys, pygame

from Pacman import Pacman
from Ghost import Ghost

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

# create ghosts
ghost_group = pygame.sprite.Group()
ghost_group.add(Ghost(300, 300))

# blit pacman and pellets to the surface
pacman_group.draw(windowSurface)

# update the game
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
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
            if event.key == K_DOWN:
                moveLeft  = False
                moveRight = False
                moveDown  = True
                moveUp    = False
            if event.key == K_UP:
                moveLeft  = False
                moveRight = False
                moveDown  = False
                moveUp    = True
                
    # move the sprite(pacman)
    pacman_group.update(moveLeft, moveRight, moveDown, moveUp)
    
    # check if Pacman collided with any Ghosts
    # If so, check if they are vulnerable
    # If true, destroy the sprite
    # If not, quit the game
    collided_ghosts = pygame.sprite.spritecollide(pacman, ghost_group, False)
    for ghost in collided_ghosts:
        if ghost.isVulnerable:
            ghost.kill()
        else:
            windowSurface.fill(BLACK)
            pygame.display.update()
            pacman.death()
            pygame.quit()
            sys.exit()
            
    # update ghost
    ghost_group.update()
    
    # redraw the background and sprite
    windowSurface.fill(BLACK)
    pacman_group.draw(windowSurface)
    ghost_group.draw(windowSurface)
    
    # update the game
    pygame.display.update()
    mainClock.tick(40)