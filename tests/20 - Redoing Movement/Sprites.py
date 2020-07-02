import pygame, time, math, random

from pygame.locals import *

class Box(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Create a 16x16 surface and fill it with the color RED
        self.image = pygame.Surface([16, 16])
        
        self.valid_moves = []
        
        # Set the rectangle's x and y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Used for path-finding
        self.path = ''
        
    def check_possible_moves(self, x, y):
        BLACK = (0, 0, 0)
        
        # Check if the space above this area is also black
        x_up = x
        y_up = y - 16
        area_up = pygame.Rect(x_up, y_up, 16, 16)
        cropped_image = self.surface.subsurface(area_up)
        if pygame.transform.average_color(cropped_image)[:3] == BLACK:
            self.valid_moves.append('U')
        
        # Check if the space below this area is also black
        x_down = x
        y_down = y + 16
        area_down = pygame.Rect(x_down, y_down, 16, 16)
        try:
            cropped_image = self.surface.subsurface(area_down)
            if pygame.transform.average_color(cropped_image)[:3] == BLACK:
                self.valid_moves.append('D')
        except ValueError:
            pass
        
        
        # Check if the space to the left of this area is also black
        x_left = x - 16
        y_left = y
        area_left = pygame.Rect(x_left, y_left, 16, 16)
        try:
            cropped_image = self.surface.subsurface(area_left)
            if pygame.transform.average_color(cropped_image)[:3] == BLACK:
                self.valid_moves.append('L')
        except ValueError:
            pass
        
        # Check if the space to the right of this area is also black
        x_right = x + 16
        y_right = y
        area_right = pygame.Rect(x_right, y_right, 16, 16)
        try:
            cropped_image = self.surface.subsurface(area_right)
            if pygame.transform.average_color(cropped_image)[:3] == BLACK:
                self.valid_moves.append('R')
        except ValueError:
            pass


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
        
        self.defaultx = x
        self.defaulty = y
        self.default_speed = speed
        
        # Speed of sprite
        self.speed = speed
        
        # Used to determine whether Pacman can eat Ghost
        self.isVulnerable = False
        
        # Used for path-finding
        self.path = None
        self.path_move = None
        self.correct_path = True
        
        # Keeping track of which pixel Ghost is currently on
        self.pixel = 0

    def toggleVulnerability(self):
        if self.isVulnerable:
            self.isVulnerable = False
            self.image = pygame.image.load('../../sprites/red.png')
            self.speed = self.default_speed
        else:
            self.isVulnerable = True
            self.image = pygame.image.load('../../sprites/v-ghost.png')
            self.speed = self.speed / 2
            if self.pixel != 0:
                self.correct_path = False
            else:
                self.correct_path = True

    def update(self, current_grid, pacman):
        if self.isVulnerable:
            if self.pixel == 0 and self.correct_path:
                self.choose_direction(current_grid, pacman)
                
            if not self.correct_path:
                self.reverse()
            else:
                self.run_away()
        else:
            self.chase_pacman()

    def reset_pos(self):
        self.rect.x = self.defaultx
        self.rect.y = self.defaulty

    def create_path(self, pacman, untraversed, grid_system):
        """
            Parameters:
                - pacman       : Pacman's current Box()
                - untraversed  : list of untraversed Box()
                - grid_system  : list of all Box() in the game
        """
        for box in untraversed:
            if box == pacman: # check if box being checked is where pacman is
                self.path = box.path
                box.path = ''
                return
                
            for move in box.valid_moves:
                if move == 'U':
                    for grid in grid_system:
                        if grid.rect.x == box.rect.x and grid.rect.y == box.rect.y - 16:
                            grid.path = box.path + 'U' # keeps track of where it came from
                            grid.remove(grid_system) # remove from grid_system
                            untraversed.append(grid) # appends to end of untraversed list
                            break
                if move == 'D':
                    for grid in grid_system:
                        if grid.rect.x == box.rect.x and grid.rect.y == box.rect.y + 16:
                            grid.path = box.path + 'D' # keeps track of where it came from
                            grid.remove(grid_system) # remove from grid_system
                            untraversed.append(grid) # appends to end of untraversed list
                            break
                if move == 'L':
                    for grid in grid_system:
                        if grid.rect.x == box.rect.x - 16 and grid.rect.y == box.rect.y:
                            grid.path = box.path + 'L' # keeps track of where it came from
                            grid.remove(grid_system) # remove from grid_system
                            untraversed.append(grid) # appends to end of untraversed list
                            break
                if move == 'R':
                    for grid in grid_system:
                        if grid.rect.x == box.rect.x + 16 and grid.rect.y == box.rect.y:
                            grid.path = box.path + 'R' # keeps track of where it came from
                            grid.remove(grid_system) # remove from grid_system
                            untraversed.append(grid) # appends to end of untraversed list
                            break
            
            box.path = ''

    def chase_pacman(self):
        # Normal movement loop
        if self.path[0] == 'U':
            self.rect.top -= self.speed
            self.pixel += self.speed
            self.path_move = 'U'
        elif self.path[0] == 'D':
            self.rect.bottom += self.speed
            self.pixel += self.speed
            self.path_move = 'D'
        elif self.path[0] == 'L':
            self.rect.left -= self.speed
            self.pixel += self.speed
            self.path_move = 'L'
        elif self.path[0] == 'R':
            self.rect.right += self.speed
            self.pixel += self.speed
            self.path_move = 'R'
        
        # When Ghost reaches a grid, reset pixel count back to 0
        if self.pixel == 16:
            self.pixel = 0

    def run_away(self):
        # Normal movement loop
        if self.path_move == 'U':
            self.rect.top -= self.speed
            self.pixel += self.speed
        elif self.path_move == 'D':
            self.rect.bottom += self.speed
            self.pixel += self.speed
        elif self.path_move == 'L':
            self.rect.left -= self.speed
            self.pixel += self.speed
        elif self.path_move == 'R':
            self.rect.right += self.speed
            self.pixel += self.speed
        
        # When Ghost reaches a grid, reset pixel count back to 0
        if self.pixel == 16:
            self.pixel = 0
            self.path_move = None

    def reverse(self):
        # Normal movement loop
        if self.path_move == 'U':
            self.rect.bottom += self.speed
            self.pixel -= self.speed
        elif self.path_move == 'D':
            self.rect.top -= self.speed
            self.pixel -= self.speed
        elif self.path_move == 'L':
            self.rect.right += self.speed
            self.pixel -= self.speed
        elif self.path_move == 'R':
            self.rect.left -= self.speed
            self.pixel -= self.speed
        
        # When Ghost reaches a grid, reset pixel count back to 0
        if self.pixel == 0:
            self.correct_path = True
            self.path_move = None

    def choose_direction(self, current_grid, pacman):
        valid_moves = current_grid.valid_moves
        distance = self.calculate_distance(current_grid.rect, pacman.rect)
        for moves in valid_moves:
            rect = self.rect.copy()
            if moves == 'U':
                rect.top -= self.speed
                new_distance = self.calculate_distance(rect, pacman.rect)
                if new_distance > distance:
                    self.path_move = 'U'
                    break
            elif moves == 'D':
                rect.bottom += self.speed
                new_distance = self.calculate_distance(rect, pacman.rect)
                if new_distance > distance:
                    self.path_move = 'D'
                    break
            elif moves == 'L':
                rect.left -= self.speed
                new_distance = self.calculate_distance(rect, pacman.rect)
                if new_distance > distance:
                    self.path_move = 'L'
                    break
            elif moves == 'R':
                rect.right += self.speed
                new_distance = self.calculate_distance(rect, pacman.rect)
                if new_distance > distance:
                    self.path_move = 'R'
                    break
        if self.path_move == None:
            index = random.randint(0, len(valid_moves)-1)
            self.path_move = valid_moves[index]

    def calculate_distance(self, point_1, point_2):
        return math.sqrt(math.pow(point_2.x - point_1.x, 2) + math.pow(point_2.y - point_1.y, 2))


class Pacman(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Set animation frames
        self.frames = [ '../../sprites/pacman-1.png',
                        '../../sprites/pacman-2.png',
                        '../../sprites/pacman-3.png',
                        '../../sprites/pacman-2.png',
        ]
        
        # Set frames for death animation
        self.death_frames = [   '../../sprites/pacman-death-1.png',
                                '../../sprites/pacman-death-2.png',
                                '../../sprites/pacman-death-3.png',
                                '../../sprites/pacman-death-4.png',
                                '../../sprites/pacman-death-5.png',
                                '../../sprites/pacman-death-6.png',
                                '../../sprites/pacman-death-7.png',
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
        
        # Get the sprite and set the x+y coordinates
        self.image = self.directions['R']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Default coordinates when the game restarts
        self.defaultx = x
        self.defaulty = y
        
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
            
    def death(self):
        time.sleep(1)
        for image in self.death_frames:
            self.image = pygame.image.load(image)
            self.surface.blit(self.image, self.rect)
            pygame.display.update()
            time.sleep(0.1)
        
        time.sleep(1)
        
    def reset_pos(self):
        self.image = self.directions['R']
        self.rect.x = self.defaultx
        self.rect.y = self.defaulty


class Pellet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../../sprites/pellet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class Magic_Pellet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../../sprites/magic_pellet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
