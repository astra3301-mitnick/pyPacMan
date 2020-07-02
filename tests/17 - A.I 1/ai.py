import os, sys, pygame

from pygame.locals import *
from Pacman import Pacman
from Ghost import Ghost

# Initialize Pygame
pygame.init()

# Initialize Clock
mainClock = pygame.time.Clock()

# Constants
WINDOWWIDTH = 448 #(16 * 28) (row numbers range from 0 - 27)
WINDOWHEIGHT = 512 #(16 * 32) (column numbers range from 0 - 31)

# Initialize colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize window
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
window.fill(BLACK)

# Pixels per loop
MOVESPEED = 16
    
# Initialize Pacman
pacman = Pacman(224, 384, MOVESPEED) # 16 * 14, 16 * 24
pacman_group = pygame.sprite.GroupSingle(pacman)

# Initialize Ghost
ghost = Ghost(224, 256, MOVESPEED)
ghost_group = pygame.sprite.GroupSingle(ghost)

# Initialize movement variable
movement = 'R'

# Draw Pacman onto the window
pacman_group.draw(window)

# Update display
pygame.display.update()

def update_window():
    """Updates the window by redrawing the background and sprites"""

    # Redraw the background and sprites
    window.fill(BLACK)
    pacman_group.draw(window)
    ghost_group.draw(window)
    
    # Update the display
    pygame.display.update()
    mainClock.tick(10)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_UP:
                movement = 'U'
            if event.key == K_DOWN:
                movement = 'D'
            if event.key == K_LEFT:
                movement = 'L'
            if event.key == K_RIGHT:
                movement = 'R'
                
    pacman_group.update(movement)
    ghost_group.update((pacman.rect.x, pacman.rect.y))
    
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
    
    # Update game
    update_window()