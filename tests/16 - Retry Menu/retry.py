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

# Create Retry Button
retry = pygame.Surface((192, 48))
retry.fill(GREEN)
retry_rect = retry.get_rect()
retry_rect.centerx = 112
retry_rect.centery = 352

# Create Quit Button
quit = pygame.Surface((192, 48))
quit.fill(RED)
quit_rect = quit.get_rect()
quit_rect.centerx = 336
quit_rect.centery = 352

window.blit(retry, retry_rect)
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
            elif retry_rect.collidepoint(x, y):
                pass # Start the game