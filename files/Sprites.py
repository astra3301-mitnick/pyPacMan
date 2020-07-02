import pygame, time, math, random

from pygame.locals import *

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, x_size, y_size):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Create a x_size x y_size surface
        self.image = pygame.Surface([x_size, y_size])
        
        self.valid_moves = []
        
        # Set the rectangle's x and y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def check_possible_moves(self, x, y, tile_system):
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

    def __init__(self, x, y, speed, color):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()

        self.name = color
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load(f'../sprites/{color}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Defaults that can be referenced back to
        self.defaultimage = pygame.image.load(f'../sprites/{color}.png')
        self.defaultx = x
        self.defaulty = y
        
        # Speed of sprite
        self.speed = speed
        self.default_speed = speed
        
        # Used for path-finding
        self.dir = 'R'
        self.correct_pixel = True
        
        # Keeping track of which pixel Ghost is currently on
        self.pixel = 0
        
        # Seven states:
        #   - 'A'live               Roam
        #   - 'C'hase               Chase
        #   - 'V'ulnerable          Run Away
        #   - 'D'ead                Back to Spawner
        #   - 'R'espawning          Enter Spawner
        #   - 'P'urgatory           Pace in Spawner
        #   - 'S'pawning            Exit Spawner
        # Initial state is Alive
        self.state = 'A'
        self.saved_state = ''
        
        # Keeping track of pacing direction (within Respawning Zone)
        self.pace_dir = 'R'

        # Timer for respawning
        self.respawn_timer = None

        self.death_frames = {}
        self.gather_death_frames()

    def update(self, current_tile):
        if self.state == 'A':
            if self.correct_pixel:
                self.move()
            else:
                self.adjust(current_tile)

        elif self.state == 'C':
            if self.correct_pixel:
                self.move()
            else:
                self.adjust(current_tile)

        elif self.state == 'TL':
            self.move()

        elif self.state == 'TR':
            self.move()

        elif self.state == 'V':
            if self.correct_pixel:
                self.move()
            else:
                self.adjust(current_tile)

        elif self.state == 'D':
            if self.correct_pixel:
                self.move()
            else:
                self.adjust(current_tile)

        elif self.state == 'R':
            if self.rect.y < 240:       # Go into the spawn-zone
                self.rect.bottom += 4
                return
            self.state = 'P'

        elif self.state == 'P':
            self.pace()

        elif self.state == 'S':
            self.rect.x = 216
            if self.rect.y > 192:
                self.rect.top -= 4
                return
            self.rect.x = 208
            self.rect.y = 192
            self.toggle_alive()

    def gather_death_frames(self):
        spreadsheet = pygame.image.load('../sprites/ghosts.png')

        selected_area = pygame.Rect(16, 48, 16, 16)
        right_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(32, 48, 16, 16)
        up_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(48, 48, 16, 16)
        down_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(64, 48, 16, 16)
        left_image = spreadsheet.subsurface(selected_area)

        self.death_frames = {
            'U': up_image,
            'D': down_image,
            'L': left_image,
            'R': right_image,
        }

    def reset_pos(self):
        self.rect.x = self.defaultx
        self.rect.y = self.defaulty
        self.pixel = 0

    def create_path(self, target_tile, current_tile):
        """
            Parameters:
                - target_tile       : Target tile
                - current_tile      : Current tile
            
            Determines best direction using current_tile's position and current_tile's position.
        """
        best_distance = None
        new_distance = None
        all_possible_moves = {
            'U': None,
            'L': None,
            'D': None,
            'R': None,
        }
        for moves in current_tile.valid_moves:
            rect = self.rect.copy()
            if moves == 'U' and self.dir != 'D':
                rect.top -= self.speed
                new_distance = self.calculate_distance(rect, target_tile.rect)
                all_possible_moves['U'] = new_distance
            elif moves == 'D' and self.dir != 'U':
                rect.bottom += self.speed
                new_distance = self.calculate_distance(rect, target_tile.rect)
                all_possible_moves['D'] = new_distance
            elif moves == 'L' and self.dir != 'R':
                rect.left -= self.speed
                new_distance = self.calculate_distance(rect, target_tile.rect)
                all_possible_moves['L'] = new_distance
            elif moves == 'R' and self.dir != 'L':
                rect.right += self.speed
                new_distance = self.calculate_distance(rect, target_tile.rect)
                all_possible_moves['R'] = new_distance
            
            if best_distance == None:
                best_distance = new_distance
            elif new_distance < best_distance:
                best_distance = new_distance

        for key in all_possible_moves:
            if best_distance == all_possible_moves[key]:
                self.dir = key
                break

    def move(self):
        # Normal movement loop
        if self.dir == 'U':
            self.rect.top -= self.speed
            self.pixel += self.speed
        elif self.dir == 'D':
            self.rect.bottom += self.speed
            self.pixel += self.speed
        elif self.dir == 'L':
            self.rect.left -= self.speed
            self.pixel += self.speed
        elif self.dir == 'R':
            self.rect.right += self.speed
            self.pixel += self.speed
        
        # When Ghost reaches a grid, reset pixel count back to 0
        if self.pixel == 16:
            self.pixel = 0

    def random_direction(self, current_tile):
        tmp_list = current_tile.valid_moves.copy()
        
        if self.dir == 'U' and 'D' in tmp_list:
            tmp_list.remove('D')
        elif self.dir == 'D' and 'U' in tmp_list:
            tmp_list.remove('U')
        elif self.dir == 'L' and 'R' in tmp_list:
            tmp_list.remove('R')
        elif self.dir == 'R' and 'L' in tmp_list:
            tmp_list.remove('L')

        index = random.randint(0, len(tmp_list)-1)
        self.dir = tmp_list[index]

    def calculate_distance(self, point_1, point_2):
        return math.sqrt(math.pow(point_2.x - point_1.x, 2) + math.pow(point_2.y - point_1.y, 2))

    def adjust(self, current_tile):
        # if self.pixel % 4 != 0:
        #     if self.pixel < 8:
        #         if self.dir == 'U':
        #             self.rect.bottom += self.speed / 2
        #             self.pixel -= self.speed / 2
        #         elif self.dir == 'D':
        #             self.rect.top -= self.speed / 2
        #             self.pixel -= self.speed / 2
        #         elif self.dir == 'L':
        #             self.rect.right += self.speed / 2
        #             self.pixel -= self.speed / 2
        #         elif self.dir == 'R':
        #             self.rect.left -= self.speed / 2
        #             self.pixel -= self.speed / 2
        #     else:
        #         if self.dir == 'U':
        #             self.rect.top -= self.speed / 2
        #             self.pixel += self.speed / 2
        #         elif self.dir == 'D':
        #             self.rect.bottom += self.speed / 2                    
        #             self.pixel += self.speed / 2
        #         elif self.dir == 'L':
        #             self.rect.left -= self.speed / 2
        #             self.pixel += self.speed / 2
        #         elif self.dir == 'R':
        #             self.rect.right += self.speed / 2
        #             self.pixel += self.speed / 2
        # else:
        #     if self.pixel < 8:
        #         if self.dir == 'U':
        #             self.rect.bottom += self.speed
        #             self.pixel -= self.speed
        #         elif self.dir == 'D':
        #             self.rect.top -= self.speed
        #             self.pixel -= self.speed
        #         elif self.dir == 'L':
        #             self.rect.right += self.speed
        #             self.pixel -= self.speed
        #         elif self.dir == 'R':
        #             self.rect.left -= self.speed
        #             self.pixel -= self.speed
        #     else:
        #         if self.dir == 'U':
        #             self.rect.top -= self.speed
        #             self.pixel += self.speed
        #         elif self.dir == 'D':
        #             self.rect.bottom += self.speed                 
        #             self.pixel += self.speed
        #         elif self.dir == 'L':
        #             self.rect.left -= self.speed
        #             self.pixel += self.speed
        #         elif self.dir == 'R':
        #             self.rect.right += self.speed
        #             self.pixel += self.speed
        self.rect.x = current_tile.rect.x
        self.rect.y = current_tile.rect.y
        
        # if self.pixel % 16 == 0:
        self.pixel = 0
        self.correct_pixel = True

    def toggle_alive(self):
        self.state = 'A'
        self.image = self.defaultimage
        self.speed = self.default_speed
        if self.pixel != 0:
            self.correct_pixel = False
        else:
            self.correct_pixel = True

    def toggle_vulnerability(self):
        self.state = 'V'
        self.speed = self.speed / 2
        self.reverse()
        if self.pixel != 0:
            self.correct_pixel = False
        else:
            self.correct_pixel = True

    def toggle_death(self):
        self.state = 'D'
        self.image = self.death_frames[self.dir]
        if self.pixel != 0:
            self.correct_pixel = False
        else:
            self.correct_pixel = True

    def toggle_chase(self):
        self.state = 'C'
        self.image = self.defaultimage
        self.speed = self.default_speed
        if self.pixel != 0:
            self.correct_pixel = False
        else:
            self.correct_pixel = True

    def toggle_spawn(self):
        self.state = 'S'
        self.respawn_timer = None

    def toggle_TL(self):
        self.saved_state = self.state
        self.state = 'TL'

    def toggle_TR(self):
        self.saved_state = self.state
        self.state = 'TR'

    def toggle_back(self):
        self.state = self.saved_state

    def pace(self):
        self.image = self.directions[self.pace_dir]
        if self.pace_dir == 'R':
            if self.rect.x < 240:
                self.rect.right += 4
                return
            else:
                self.pace_dir = 'L'
        if self.pace_dir == 'L':
            if self.rect.x > 192:
                self.rect.left -= 4
                return
            else:
                self.pace_dir = 'R'

    def reverse(self):
        if self.dir == 'U':
            self.dir = 'D'
        elif self.dir == 'D':
            self.dir = 'U'
        elif self.dir == 'L':
            self.dir = 'R'
        elif self.dir == 'R':
            self.dir = 'L'


class Red(Ghost):

    def __init__(self, x, y, speed, color):
        super().__init__(x, y, speed, color)
        self.directions = {}
        self.gather_frames()
        self.image = self.directions['R']

    def gather_frames(self):
        spreadsheet = pygame.image.load('../sprites/ghosts.png')

        selected_area = pygame.Rect(0, 0, 16, 16)
        right_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(16, 0, 16, 16)
        up_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(32, 0, 16, 16)
        down_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(48, 0, 16, 16)
        left_image = spreadsheet.subsurface(selected_area)

        self.directions = {
            'U': up_image,
            'D': down_image,
            'L': left_image,
            'R': right_image,
        }

    def update(self, current_tile):
        if self.state == 'D':
            self.image = self.death_frames[self.dir]
        elif self.state == 'V' or self.saved_state == 'V':
            self.image = pygame.image.load('../sprites/v-ghost.png')
        else:
            self.image = self.directions[self.dir]
        self.image = pygame.transform.scale(self.image, (20, 20))
        super().update(current_tile)
        

class Teal(Ghost):

    def __init__(self, x, y, speed, color):
        super().__init__(x, y, speed, color)
        self.directions = {}
        self.gather_frames()
        self.image = self.directions['R']

    def gather_frames(self):
        spreadsheet = pygame.image.load('../sprites/ghosts.png')

        selected_area = pygame.Rect(64, 0, 16, 16)
        right_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(0, 16, 16, 16)
        up_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(16, 16, 16, 16)
        down_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(32, 16, 16, 16)
        left_image = spreadsheet.subsurface(selected_area)

        self.directions = {
            'U': up_image,
            'D': down_image,
            'L': left_image,
            'R': right_image,
        }

    def update(self, current_tile):
        if self.state == 'D':
            self.image = self.death_frames[self.dir]
        elif self.state == 'V' or self.saved_state == 'V':
            self.image = pygame.image.load('../sprites/v-ghost.png')
        else:
            self.image = self.directions[self.dir]
        self.image = pygame.transform.scale(self.image, (20, 20))
        super().update(current_tile)


class Orange(Ghost):
    def __init__(self, x, y, speed, color):
        super().__init__(x, y, speed, color)
        self.directions = {}
        self.gather_frames()
        self.image = self.directions['R']

    def gather_frames(self):
        spreadsheet = pygame.image.load('../sprites/ghosts.png')

        selected_area = pygame.Rect(48, 16, 16, 16)
        right_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(64, 16, 16, 16)
        up_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(0, 32, 16, 16)
        down_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(16, 32, 16, 16)
        left_image = spreadsheet.subsurface(selected_area)

        self.directions = {
            'U': up_image,
            'D': down_image,
            'L': left_image,
            'R': right_image,
        }

    def update(self, current_tile):
        if self.state == 'D':
            self.image = self.death_frames[self.dir]
        elif self.state == 'V' or self.saved_state == 'V':
            self.image = pygame.image.load('../sprites/v-ghost.png')
        else:
            self.image = self.directions[self.dir]
        self.image = pygame.transform.scale(self.image, (20, 20))
        super().update(current_tile)


class Pink(Ghost):
    def __init__(self, x, y, speed, color):
        super().__init__(x, y, speed, color)
        self.directions = {}
        self.gather_frames()
        self.image = self.directions['R']

    def gather_frames(self):
        spreadsheet = pygame.image.load('../sprites/ghosts.png')

        selected_area = pygame.Rect(32, 32, 16, 16)
        right_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(48, 32, 16, 16)
        up_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(64, 32, 16, 16)
        down_image = spreadsheet.subsurface(selected_area)

        selected_area = pygame.Rect(0, 48, 16, 16)
        left_image = spreadsheet.subsurface(selected_area)

        self.directions = {
            'U': up_image,
            'D': down_image,
            'L': left_image,
            'R': right_image,
        }

    def update(self, current_tile):
        if self.state == 'D':
            self.image = self.death_frames[self.dir]
        elif self.state == 'V' or self.saved_state == 'V':
            self.image = pygame.image.load('../sprites/v-ghost.png')
        else:
            self.image = self.directions[self.dir]
        self.image = pygame.transform.scale(self.image, (20, 20))
        super().update(current_tile)


class Pacman(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Set animation frames
        self.frames = [ '../sprites/pacman-1.png',
                        '../sprites/pacman-2.png',
                        '../sprites/pacman-3.png',
                        '../sprites/pacman-2.png',
        ]
        
        # Set frames for death animation
        self.death_frames = [   '../sprites/pacman-death-1.png',
                                '../sprites/pacman-death-2.png',
                                '../sprites/pacman-death-3.png',
                                '../sprites/pacman-death-4.png',
                                '../sprites/pacman-death-5.png',
                                '../sprites/pacman-death-6.png',
                                '../sprites/pacman-death-7.png',
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

        # Get the sound effects
        self.beep = pygame.mixer.Sound("../audio/beep.wav")
        
        # Default coordinates when the game restarts
        self.defaultx = x
        self.defaulty = y
        
        # Setting the pixels per loop of the sprite
        self.speed = speed

        # Three states:
        # 'N'one
        # 'TR'
        # 'TL'
        self.state = 'N'
        
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
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.beep.play()
            
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

    def toggle_TR(self):
        self.state = 'TR'
    
    def toggle_TL(self):
        self.state = 'TL'

    def toggle_N(self):
        self.state = 'N'


class Pellet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../sprites/pellet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class Power_Pellet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../sprites/magic_pellet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
