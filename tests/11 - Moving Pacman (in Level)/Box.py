import pygame

from pygame.locals import *

class Box(pygame.sprite.Sprite):

    def __init__(self, x, y, color):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Create a 16x16 surface and fill it with the color RED
        self.image = pygame.Surface([16, 16])
        self.image.fill(color)
        
        # Set the rectangle's x and y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y