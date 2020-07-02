import pygame

from pygame.locals import *

class Pacman(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed, collisions):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Set animation frames
        self.frames = [ '../../sprites/pacman.png',
                        '../../sprites/pacman-2.png',
                        '../../sprites/pacman-3.png',
                        '../../sprites/pacman-2.png',
        ]
        
        # Used to determine which frame the animation is in
        # Therefore, the index can go as far as 3 before resetting back to zero
        # if the movement were continuous
        self.index = 0
        
        # This dictionary contains the possible direction keywords
        # Each keyword points to the correct orientation of the image
        self.directions = { 'U': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 90),
                            'D': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 270),
                            'L': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 180),
                            'R': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 0),
        }
        
        # Will become true if one of the movement variables are true
        self.isMoving = False
        
        # Get the sprite and set the x+y coordinates
        self.image = self.directions['R']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Setting the pixels per loop of the sprite
        self.speed = speed
        
    def update(self, movement):
        
        if movement == 'U':
            self.rect.top -= self.speed
            self.index += 1
        elif movement == 'D':
            self.rect.bottom += self.speed
            self.index += 1
        elif movement == 'L':
            self.rect.left -= self.speed
            self.index += 1
        elif movement == 'R':
            self.rect.right += self.speed
            self.index += 1
        else:
            self.index = 0
        
        # Specfic Case
        if self.index == 4:
            self.index = 0
                
        # Called again to update the image based on index
        self.directions = { 'U': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 90),
                            'D': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 270),
                            'L': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 180),
                            'R': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 0),
        }
            
        # Update image
        if movement:
            self.image = self.directions[movement]
        