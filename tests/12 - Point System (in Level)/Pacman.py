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
        
        # Keep history of the last movement made
        # lastMove can be 'U' | 'D' | 'L' | 'R'
        # Pacman starts looking right, so "R" is the initial value
        self.lastMove = 'R'
        
        # Will become true if one of the movement variables are true
        self.isMoving = False
        
        # Get the sprite and set the x+y coordinates
        self.image = self.directions[self.lastMove]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Setting the pixels per loop of the sprite
        self.speed = speed
        
        # Set the collisions for Pacman
        self.collisions = collisions
        
    def update(self, moveUp, moveDown, moveLeft, moveRight):

        list_of_movement = [moveLeft, moveRight, moveDown, moveUp]
        
        if list_of_movement.count(True) > 0:
            self.isMoving = True
        else:
            self.isMoving = False
        
        # if Pacman is moving, continue looping through the animation frames
        if self.isMoving:
            self.index += 1
            if self.index is len(self.frames):
                self.index = 0
        else:
            self.index = 0
        
        if moveUp:
            self.rect.top -= self.speed
            if not pygame.sprite.spritecollide(self, self.collisions, False):
                self.lastMove = 'U'
            else:
                self.rect.top += self.speed
                self.index = 0
            
        if moveDown:
            self.rect.bottom += self.speed
            if not pygame.sprite.spritecollide(self, self.collisions, False):
                self.lastMove = 'D'
            else:
                self.rect.bottom -= self.speed
                self.index = 0
    
        if moveLeft:
            self.rect.left -= self.speed
            if not pygame.sprite.spritecollide(self, self.collisions, False):
                self.lastMove = 'L'
            else:
                self.rect.left += self.speed
                self.index = 0
            
        if moveRight:
            self.rect.right += self.speed
            if not pygame.sprite.spritecollide(self, self.collisions, False):
                self.lastMove = 'R'
            else:
                self.rect.right -= self.speed
                self.index = 0
                
        # Directions is called again to update the image based on index
        self.directions = { 'U': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 90),
                            'D': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 270),
                            'L': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 180),
                            'R': pygame.transform.rotate(pygame.image.load(self.frames[self.index]), 0),
        }
            
        # Update image
        self.image = self.directions[self.lastMove]
        