import pygame, math

from pygame.locals import *

class Ghost(pygame.sprite.Sprite):

    def __init__(self, x, y, speed):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../../sprites/red.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Set Vulnerable state to False
        self.isVulnerable = False
        
        self.speed = speed
        
    def update(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        
        distance = math.sqrt(math.pow(x - self.rect.x, 2) + math.pow(y - self.rect.y, 2))
        
        list_of_new_distances = {}
        
        # test up
        self.rect.top -= self.speed
        list_of_new_distances['U'] = math.sqrt(math.pow(x - self.rect.x, 2) + math.pow(y - self.rect.y, 2))
        self.rect.top += self.speed
            
        # test down
        self.rect.bottom += self.speed
        list_of_new_distances['D'] = math.sqrt(math.pow(x - self.rect.x, 2) + math.pow(y - self.rect.y, 2))
        self.rect.bottom -= self.speed
            
        # test left
        self.rect.left -= self.speed
        list_of_new_distances['L'] = math.sqrt(math.pow(x - self.rect.x, 2) + math.pow(y - self.rect.y, 2))
        self.rect.left += self.speed
            
        # test right
        self.rect.right += self.speed
        list_of_new_distances['R'] = math.sqrt(math.pow(x - self.rect.x, 2) + math.pow(y - self.rect.y, 2))
        self.rect.right -= self.speed
        
        closest_distance = None
        for key in list_of_new_distances:
            dir = key
            val = list_of_new_distances[key]
            if closest_distance == None:
                closest_distance = [dir, val - distance]
            else:
                if (val - distance) < closest_distance[1]:
                    closest_distance = [dir, val - distance]
                    
        if closest_distance[0] == 'U':
            self.rect.top -= self.speed
        elif closest_distance[0] == 'D':
            self.rect.bottom += self.speed
        elif closest_distance[0] == 'L':
            self.rect.left -= self.speed
        elif closest_distance[0] == 'R':
            self.rect.right += self.speed
        
    