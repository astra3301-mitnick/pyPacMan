import pygame

from pygame.locals import *

class Pacman(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../../sprites/pacman.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Setting the pixels per loop of the sprite
        self.speed = speed
        
    def update(self, moveLeft, moveRight, moveDown, moveUp):
        if moveLeft and self.rect.left > 0:
            # set image to be the original sprite rotated 180 degrees counter-clockwise
            self.image = pygame.transform.rotate(pygame.image.load('../../sprites/pacman.png'), 180)
            self.rect.left -= self.speed
            
        if moveRight and self.rect.right < self.surface.get_width():
            # set image to be the original sprite
            self.image = pygame.image.load('../../sprites/pacman.png')
            self.rect.right += self.speed
            
        if moveDown and self.rect.bottom < self.surface.get_height():
            # set image to be the original sprite rotated 270 degrees counter-clockwise
            self.image = pygame.transform.rotate(pygame.image.load('../../sprites/pacman.png'), 270)
            self.rect.bottom += self.speed
            
        if moveUp and self.rect.top > 0:
            # set image to be the original sprite rotated 90 degrees counter-clockwise
            self.image = pygame.transform.rotate(pygame.image.load('../../sprites/pacman.png'), 90)
            self.rect.top -= self.speed