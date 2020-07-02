import os, sys, pygame

from pygame.locals import *

# Initialize pygame
pygame.init()

# Initialize clock
mainClock = pygame.time.Clock()

# Constants
WINDOWWIDTH = 448 #(16 * 28) (row numbers range from 0 - 27)
WINDOWHEIGHT = 512 #(16 * 32) (column numbers range from 0 - 31)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize window
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
window.fill(BLACK)

# Create Title
pacman_title = pygame.Surface((384, 192))
pacman_title.fill(WHITE)
pacman_title_rect = pacman_title.get_rect()
pacman_title_rect.centerx = WINDOWWIDTH/2
pacman_title_rect.centery = 128

# Create Start Button
start = pygame.Surface((192, 48))
start.fill(GREEN)
start_rect = start.get_rect()
start_rect.centerx = WINDOWWIDTH/2
start_rect.centery = 320

# Create Exit Button
quit = pygame.Surface((96, 48))
quit.fill(RED)
quit_rect = quit.get_rect()
quit_rect.centerx = WINDOWWIDTH/2
quit_rect.centery = 408

window.blit(pacman_title, pacman_title_rect)
window.blit(start, start_rect)
window.blit(quit, quit_rect)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if quit_rect.collidepoint(x, y):
                pygame.quit()
                sys.exit()
            elif start_rect.collidepoint(x, y):
                pass # Start the game