import os, sys, pygame

from Pacman import Pacman
from Pellet import Pellet
from Magic_Pellet import Magic_Pellet
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

# create pellets
pellet_group = pygame.sprite.Group()
pellet_group.add(Pellet(50, 50), Pellet(100, 100))

# create magic pellets
m_pellet_group = pygame.sprite.Group()
m_pellet_group.add(Magic_Pellet(200, 200))

# blit pacman and pellets to the surface
pacman_group.draw(windowSurface)
pellet_group.draw(windowSurface)

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
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_UP:
                moveUp = False
                
    # move the sprite(pacman)
    pacman_group.update(moveLeft, moveRight, moveDown, moveUp)
    
    # check if Pacman collided with any Pellets in Pellet Group
    # true = Pellet will be destroyed when collided with
    pygame.sprite.spritecollide(pacman, pellet_group, True)
    
    # check if Pacman collided with any Magic Pellets
    # If so, then trigger the ghost's vulnerability
    collided_mps = pygame.sprite.spritecollide(pacman, m_pellet_group, True)
    if len(collided_mps) == 1:
        for ghost in ghost_group:
            ghost.triggerVulnerability()
    
    # check if Pacman collided with any Ghosts
    # If so, check if they are vulnerable
    # If true, destroy the sprite
    # If not, quit the game
    collided_ghosts = pygame.sprite.spritecollide(pacman, ghost_group, False)
    for ghost in collided_ghosts:
        if ghost.isVulnerable:
            ghost.kill()
        else:
            pygame.quit()
            sys.exit()
            
    # update ghost
    ghost_group.update()
    
    # redraw the background and sprite
    windowSurface.fill(BLACK)
    pacman_group.draw(windowSurface)
    ghost_group.draw(windowSurface)
    pellet_group.draw(windowSurface)
    m_pellet_group.draw(windowSurface)
    
    # update the game
    pygame.display.update()
    mainClock.tick(40)