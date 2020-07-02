import pygame

from pygame.locals import *

class Magic_Pellet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../../sprites/magic_pellet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y