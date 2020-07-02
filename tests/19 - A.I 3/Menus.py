import pygame, sys, constants

from pygame.locals import *

class Start(object):
	
    def __init__(self):

        # Initialize window
        window = pygame.display.set_mode((constants.WINDOWWIDTH, constants.WINDOWHEIGHT), 0, 32)
        window.fill(constants.BLACK)
        
        # Initialize font
        font = pygame.font.Font("../../font/joystix.ttf", 36)

        # Create Title
        pacman_title = pygame.image.load("../../sprites/pyman_title.png")
        pacman_title_rect = pacman_title.get_rect()
        pacman_title_rect.centerx = constants.WINDOWWIDTH/2
        pacman_title_rect.centery = 128

        # Create Start Button
        start = pygame.Surface((192, 48))
        start_rect = start.get_rect()
        start_rect.centerx = constants.WINDOWWIDTH/2
        start_rect.centery = 320

        # Create Exit Button
        quit = pygame.Surface((96, 48))
        quit_rect = quit.get_rect()
        quit_rect.centerx = constants.WINDOWWIDTH/2
        quit_rect.centery = 408
        
        # Create Start Text
        start_text = font.render("START", True, constants.GREEN)
        start_text_rect = start_text.get_rect()
        start_text_rect.centerx = start_rect.centerx
        start_text_rect.centery = start_rect.centery
        
        # Create Quit Text
        quit_text = font.render("QUIT", True, constants.RED)
        quit_text_rect = quit_text.get_rect()
        quit_text_rect.centerx = quit_rect.centerx
        quit_text_rect.centery = quit_rect.centery
        
        window.blit(pacman_title, pacman_title_rect)
        window.blit(start_text, start_text_rect)
        window.blit(quit_text, quit_text_rect)

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
                        return
                        
                        

class Retry(object):
	
    def __init__(self):        

        # Initialize window
        window = pygame.display.set_mode((constants.WINDOWWIDTH, constants.WINDOWHEIGHT), 0, 32)
        window.fill(constants.BLACK)
        
        # Initialize font
        font = pygame.font.Font("../../font/minecraft.ttf", 36)

        # Create Retry Button
        retry = pygame.Surface((192, 48))
        retry_rect = retry.get_rect()
        retry_rect.centerx = 112
        retry_rect.centery = 352

        # Create Quit Button
        quit = pygame.Surface((192, 48))
        quit_rect = quit.get_rect()
        quit_rect.centerx = 336
        quit_rect.centery = 352
        
        # Create Retry Text
        retry_text = font.render("RETRY", True, constants.GREEN)
        retry_text_rect = retry_text.get_rect()
        retry_text_rect.centerx = retry_rect.centerx
        retry_text_rect.centery = retry_rect.centery
        
        # Create Quit Text
        quit_text = font.render("QUIT", True, constants.RED)
        quit_text_rect = quit_text.get_rect()
        quit_text_rect.centerx = quit_rect.centerx
        quit_text_rect.centery = quit_rect.centery

        window.blit(retry_text, retry_text_rect)
        window.blit(quit_text, quit_text_rect)

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
                        return