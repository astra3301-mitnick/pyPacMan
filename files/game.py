import os, sys, pygame, constants, time

from pygame.locals import *

# from Start import Start
from Menus import Start, Retry
from Sprites import Tile, Ghost, Pacman, Pellet, Power_Pellet, Red, Teal, Orange, Pink

# Initialize Pygame
pygame.init()

# Initialize Clock
mainClock = pygame.time.Clock()

# Initialize the game's Start Menu
Start()

# Constants
LIVES = 3
POINTS = 0

# text
font_system = pygame.font.Font("../font/joystix.ttf", 14)
font_system_small = pygame.font.Font("../font/joystix.ttf", 7)
text = font_system.render("POINTS: {}".format(POINTS), True, constants.WHITE)
pygame.display.set_caption("Pac Man")
# Initialize window
window = pygame.display.set_mode((constants.WINDOWWIDTH, constants.WINDOWHEIGHT), 0, 32)

# Set background
background = pygame.image.load('../sprites/pacman-level.png')
window.blit(background, (0, 0))

# Pixels per loop
MOVESPEED = 4

# Create Tilees for collisions
walls = pygame.sprite.Group()

# Grid (for movement)
# Uses Tile objects
tile_system = pygame.sprite.Group()

# Pellets
# To create a Pellet object: Pellet(x, y)
pellets = pygame.sprite.Group()

# Magic Pellets
power_pellets = pygame.sprite.Group()

# Points
v_points = 200

# Keeps track of pacing Ghosts
p_list = []

# Teleporters
left_transporter = Tile(16 * 4, 16 * 15, 1, 16) # 16 * 0
left_exit = Tile(16 * 5, 16 * 15, 1, 16)
right_transporter = Tile(16 * 23, 16 * 15, 1, 16) # 16 * 27
right_exit = Tile(16 * 22, 16 * 15, 1, 16)
l_transporter = pygame.sprite.GroupSingle(left_transporter)
r_transporter = pygame.sprite.GroupSingle(right_transporter)

# Used for roaming
top_left_tile = Tile(16 * 1, 16 * 1, 16, 16)
top_right_tile = Tile(16 * 26, 16 * 1, 16, 16)
bottom_left_tile = Tile(0, 16 * 31, 16, 16)
bottom_right_tile = Tile(16 * 26, 16 * 31, 16, 16)
roam_tiles = pygame.sprite.Group(top_left_tile, top_right_tile, bottom_left_tile, bottom_right_tile)

# Respawner
respawner_tile = Tile(223, 192, 1, 16)
respawner = pygame.sprite.GroupSingle(respawner_tile)

# Create Grid System
x = 0
y = 16
while y < constants.WINDOWHEIGHT:
    while x < constants.WINDOWWIDTH:
        # 16x16 area used for cropping
        selected_area = pygame.Rect(x, y, 16, 16)
        
        # Creates a cropped image from the background
        cropped_image = background.subsurface(selected_area)
        
        # If the cropped image's color is BLACK
        if pygame.transform.average_color(cropped_image)[:3] == constants.BLACK:
            # Create grid for movement
            tile_system.add(Tile(x, y, 16, 16))
        else:
            walls.add(Tile(x, y, 16, 16))
        
        x += 16
    y += 16
    x = 0

# Connect Grid System
x = 0
y = 16
while y < constants.WINDOWHEIGHT:
    while x < constants.WINDOWWIDTH:
        # 16x16 area used for cropping
        selected_area = pygame.Rect(x, y, 16, 16)
        
        # Creates a cropped image from the background
        cropped_image = background.subsurface(selected_area)
        
        # If the cropped image's color is BLACK
        if pygame.transform.average_color(cropped_image)[:3] == constants.BLACK:
            for tile in tile_system:
                if tile.rect.x == x and tile.rect.y == y:
                    tile.check_possible_moves(x, y, tile_system.copy())
        
        x += 16
    y += 16
    x = 0
    
# Initialize Pacman
pacman = Pacman(224, 384, MOVESPEED) # 16 * 14, 16 * 24
pacman_group = pygame.sprite.GroupSingle(pacman)
    
# Initialize Ghosts
red = Red(208, 192, MOVESPEED, 'red')
teal = Teal(216, 240, MOVESPEED, 'teal')
orange = Orange(192, 240, MOVESPEED, 'orange')
pink = Pink(240, 240, MOVESPEED, 'pink')
ghost_group = pygame.sprite.Group(red, teal, orange, pink)
    
# Initialize movement variable
movement = 'R'
last_movement = 'R'

# Initialize timers
time_start = None
time_end = None
event_start = None
event_end = None
event_name = ''

# Loop
loop = 0

def create_pellets():
    """ Identifies where Pellets can and cannot go """
    # Goes through the entire map and outlines which 16x16 areas are black
    # This identifies where Pacman and Pellets can and cannot go
    list = [3, 4, 8, 9, 10, 17, 18, 19, 23, 24]
    columns = [i * constants.SPRITEWIDTH for i in list]
    x = 0
    y = 16
    while y < constants.WINDOWHEIGHT:
        while x < constants.WINDOWWIDTH:
            # 16x16 area used for cropping
            selected_area = pygame.Rect(x, y, 16, 16)
            
            # Creates a cropped image from the background
            cropped_image = background.subsurface(selected_area)
            
            # If the cropped image's color is BLACK
            if pygame.transform.average_color(cropped_image)[:3] == constants.BLACK:                
                # These if-statements are for specific cases
                if y == constants.SPRITEHEIGHT*4:
                    if not x in columns:
                        pellets.add(Pellet(selected_area.centerx, selected_area.centery))
                elif not (y >= constants.SPRITEHEIGHT*10 and y <= constants.SPRITEHEIGHT*20):
                    pellets.add(Pellet(selected_area.centerx, selected_area.centery))
                else:
                    if x == constants.SPRITEWIDTH*6 or x == constants.SPRITEWIDTH*21:
                        pellets.add(Pellet(selected_area.centerx, selected_area.centery))
            
            x += 16
        y += 16
        x = 0


def load_game():
    """Loads map and pellets"""    
    # Creates the map
    window.blit(background, (0, 0))
    
    # Sets Pacman to its default position
    pacman.reset_pos()
    for ghost in ghost_group:
        ghost.reset_pos()
        ghost.toggle_alive()

    teal.state = 'P'
    p_list.append(teal)
    orange.state = 'P'
    p_list.append(orange)
    pink.state = 'P'
    p_list.append(pink)
    
    # Create the pellets
    pellets.empty()
    create_pellets()
    
    # Create the magic pellets
    power_pellets.empty()
    coordinates = [(16*1, 16*4), (16*26, 16*4), (16*1, 16*24), (16*26, 16*24)]
    for (x, y) in coordinates:
        selected_area = pygame.Rect(x, y, 16, 16)
        power_pellets.add(Power_Pellet(selected_area.centerx, selected_area.centery))
    
    # Draw all sprites
    pellets.draw(window)
    power_pellets.draw(window)
    pacman_group.draw(window)
    ghost_group.draw(window)
    
    # "Ready" Message
    text = font_system.render("READY!", True, constants.YELLOW)
    window.blit(text, (192, 288))
    pygame.display.update()
    time.sleep(2.5)

    
def continue_game():
    """Loads sprites and leaves pellets the same"""
    # Creates the map
    window.blit(background, (0, 0))
    
    # Sets Pacman & Ghost to their default position
    pacman.reset_pos()
    for ghost in ghost_group:
        ghost.toggle_alive()
        ghost.reset_pos()

    teal.state = 'P'
    p_list.append(teal)
    orange.state = 'P'
    p_list.append(orange)
    pink.state = 'P'
    p_list.append(pink)
    
    # Updates Pacman's movement
    pacman_current_grid = pygame.sprite.spritecollide(pacman, tile_system, False)
    p_grid = pacman_current_grid.pop()
    
    # Updates Ghost's movement
    ghost_current_grid = pygame.sprite.spritecollide(ghost, tile_system, False)
    ghost_grid = ghost_current_grid.pop()
    ghost.create_path(p_grid, ghost_grid)
    
    # Draw all sprites
    pellets.draw(window)
    pacman_group.draw(window)
    ghost_group.draw(window)
    
    # "Ready" Message
    text = font_system.render("READY!", True, constants.YELLOW)
    window.blit(text, (192, 288))
    pygame.display.update()
    time.sleep(2.5)
    
    
def update_window():
    """Updates the window by redrawing the background and sprites"""

    # Redraw the background and sprites
    window.blit(background, (0, 0))
    pellets.draw(window)
    power_pellets.draw(window)
    pacman_group.draw(window)
    ghost_group.draw(window)
    
    # Redraw the text
    text = font_system.render("POINTS: {}".format(POINTS), True, constants.WHITE)
    window.blit(text, (1, 1))
    
    # Redraw the life system
    x = 16 * 20
    for _ in range(LIVES):
        sprite = pygame.image.load('../sprites/pacman-2.png')
        window.blit(sprite, (x, 0))
        x += 16
    
    # Update the display
    pygame.display.update()
    mainClock.tick(80)
    

def transport_right(sprite):
    """Transports sprite from the right side of the window to the left side"""
    
    while sprite.rect.left <= constants.WINDOWWIDTH:
        sprite.rect.right += 1
        update_window()
        
    sprite.rect.right = 0
    
    while sprite.rect.left <= 0:
        sprite.rect.right += 1
        update_window()
        
    sprite.rect = pygame.Rect(16 * 5, 16 * 15, 16, 16)
    
    
def transport_left(sprite):
    """Transports sprite from the left side of the window to the right side"""
    
    while sprite.rect.right >= 0:
        sprite.rect.left -= 1
        update_window()
        
    sprite.rect.left = constants.WINDOWWIDTH
    
    while sprite.rect.right >= constants.WINDOWWIDTH:
        sprite.rect.left -= 1
        update_window()
        
    sprite.rect = pygame.Rect(16 * 22, 16 * 15, 16, 16)
    
    
def test_movement(move, speed, pacman):
    """ Tests movement of player and will update Pacman if move is legal """
    test = Tile(pacman.rect.x, pacman.rect.y, 16, 16)
    global last_movement
    if move == 'U':
        test.rect.top -= speed
        if not pygame.sprite.spritecollide(test, walls, False):
            last_movement = 'U'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)
    elif move == 'D':
        test.rect.bottom += speed
        if not pygame.sprite.spritecollide(test, walls, False):
            last_movement = 'D'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)
    elif move == 'L':
        test.rect.left -= speed
        if not pygame.sprite.spritecollide(test, walls, False):
            last_movement = 'L'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)
    elif move == 'R':
        test.rect.right += speed
        if not pygame.sprite.spritecollide(test, walls, False):
            last_movement = 'R'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)

            
def test_last_movement(move, speed, pacman):
    """
        Tests last movement of player and will update Pacman if move is legal.
        
        Function used is test_movement() failed.
    """

    test = Tile(pacman.rect.x, pacman.rect.y, 16, 16)
    global last_movement
    if move == 'U':
        test.rect.top -= speed
        if not pygame.sprite.spritecollide(test, walls, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    elif move == 'D':
        test.rect.bottom += speed
        if not pygame.sprite.spritecollide(test, walls, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    elif move == 'L':
        test.rect.left -= speed
        if not pygame.sprite.spritecollide(test, walls, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    elif move == 'R':
        test.rect.right += speed
        if not pygame.sprite.spritecollide(test, walls, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    
load_game()
event_start = time.time()
###############################################################################
##########                     MAIN GAME LOOP                        ##########
###############################################################################
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_UP:
                movement = 'U'
            if event.key == K_DOWN:
                movement = 'D'
            if event.key == K_LEFT:
                movement = 'L'
            if event.key == K_RIGHT:
                movement = 'R'

    # Checks to see if a Power_Pellet had been eaten
    # Then if 5 seconds have passed, all Ghosts who are still 'V'ulnerable
    # will be switched back to 'A'live
    if time_start:
        time_end = time.time()
        if (time_end-time_start) >= 5.0:
            for ghost in ghost_group:
                if ghost.state == 'V':
                    ghost.toggle_alive()
            time_start = None

    # Toggles between events
    # Different events take place over 20 seconds
    # For 7 seconds, Ghosts are in 'A' state
    # For 13 seconds, Ghosts are in 'C' state
    event_end = time.time()
    if (event_end-event_start) >= 20.0:
        event_name = 'A'
        event_start = time.time()
    elif (event_end-event_start) >= 7.0:
        event_name = 'C'
        
    # Added new event trigger to keep track of current events
    # If Ghost comes out of spawn, it knows which state to be in
    if event_name == 'A':
        for ghost in ghost_group:
            if ghost.state == 'C':
                ghost.toggle_alive()
    elif event_name == 'C':
        for ghost in ghost_group:
            if ghost.state == 'A':
                ghost.toggle_chase()

    # Checks to see if any Ghosts are respawning
    # Then no other ghost is spawning, 'S'pawn the Ghost back into the game
    nom = None
    for ghost in p_list:
        if ghost.state == 'P' and nom == None:
            nom = ghost
        elif ghost.state == 'S':
            nom = None
            break
    
    if nom:
        nom.toggle_spawn()
        
                
    for ghost in ghost_group:
        if (ghost.pixel == 0 and loop % 3 == 0) or (ghost.state == 'D' and ghost.pixel == 0):
            # Find Pacman's and Respawner's current tile
            pacman_current_tile = pygame.sprite.spritecollide(pacman, tile_system, False)
            respawner_current_tile = pygame.sprite.spritecollide(respawner_tile, tile_system, False)
                
            # Find Ghost's current tiles
            red_current_tile = pygame.sprite.spritecollide(top_right_tile, walls, False)
            pink_current_tile = pygame.sprite.spritecollide(top_left_tile, walls, False)
            orange_current_tile = pygame.sprite.spritecollide(bottom_left_tile, walls, False)
            teal_current_tile = pygame.sprite.spritecollide(bottom_right_tile, walls, False)
                
            # Updates Ghost's movement
            ghost_current_tile = pygame.sprite.spritecollide(ghost, tile_system, False)
            try:
                ghost_tile = ghost_current_tile.pop()
            except IndexError:
                pass

            target = None

            if ghost.state == 'A':
                if ghost.name == 'red':
                    target = red_current_tile.pop()
                    red.create_path(target, ghost_tile)
                elif ghost.name == 'teal':
                    target = teal_current_tile.pop()
                    teal.create_path(target, ghost_tile)
                elif ghost.name == 'orange':
                    target = orange_current_tile.pop()
                    orange.create_path(target, ghost_tile)
                elif ghost.name == 'pink':
                    target = pink_current_tile.pop()
                    pink.create_path(target, ghost_tile)
            elif ghost.state == 'C':
                try:
                    target = pacman_current_tile.pop()
                    ghost.create_path(target, ghost_tile)
                except IndexError:
                    pass
            elif ghost.state == 'D':
                target = respawner_current_tile.pop()
                ghost.create_path(target, ghost_tile)
            elif ghost.state == 'V':
                ghost.random_direction(ghost_tile)
    
    # Transport Pacman if Pacman collides with either transporter
    if pygame.sprite.spritecollide(pacman, l_transporter, False):
        if pacman.state == 'N':
            pacman.toggle_TL()
    elif pygame.sprite.spritecollide(pacman, r_transporter, False):
        if pacman.state == 'N':
            pacman.toggle_TR()
    
    # Transport any Ghosts if Ghosts collide with either transporter
    for ghost in ghost_group:
        if pygame.sprite.spritecollide(ghost, l_transporter, False):
            if ghost.state == 'C' or ghost.state == 'V':
                ghost.toggle_TL()
        elif pygame.sprite.spritecollide(ghost, r_transporter, False):
            if ghost.state == 'C' or ghost.state == 'V':
                ghost.toggle_TR()
    
    # Move Pacman
    if loop % 3 == 0:
        if pacman.state == 'N':
            test_movement(movement, MOVESPEED, pacman)
        elif pacman.state == 'TL':
            pacman_group.update('L')
            if pacman.rect.right <= 0:
                pacman.rect.left = constants.WINDOWWIDTH
            elif pacman.rect.contains(right_exit.rect):
                pacman.toggle_N()
        elif pacman.state == 'TR':
            pacman_group.update('R')
            if pacman.rect.left >= constants.WINDOWWIDTH:
                pacman.rect.right = 0
            elif pacman.rect.contains(left_exit.rect):
                pacman.toggle_N()
        
    # Move Ghosts
    for ghost in ghost_group:
        if ghost.state == 'D' or loop % 3 == 0:
            # Updates Ghost's movement
            ghost_current_tile = pygame.sprite.spritecollide(ghost, tile_system, False)
            try:
                ghost_tile = ghost_current_tile.pop()
            except IndexError:
                pass
            if ghost.state != 'TL' and ghost.state != 'TR':                
                ghost.update(ghost_tile)
            else:
                if ghost.state == 'TL':
                    ghost.dir = 'L'
                    ghost.update(ghost_tile)
                    if ghost.rect.right <= 0:
                        ghost.rect.left = constants.WINDOWWIDTH
                    elif ghost.rect.contains(right_exit.rect):
                        ghost.toggle_back()
                elif ghost.state == 'TR':
                    ghost.dir = 'R'
                    ghost.update(ghost_tile)
                    if ghost.rect.left >= constants.WINDOWWIDTH:
                        ghost.rect.right = 0
                    elif ghost.rect.contains(left_exit.rect):
                        ghost.toggle_back()
    
    # Check if Pacman collided with any Pellets
    # True = Pellet will be destroyed when collided with
    eaten_pellets = pygame.sprite.spritecollide(pacman, pellets, True)
    for pellet in eaten_pellets:
        POINTS += 10
        
    # Check if Pacman collided with any Magic Pellets
    # True = Magic Pellet will be destroyed when collided with
    eaten_power_pellets = pygame.sprite.spritecollide(pacman, power_pellets, True)
    for power_pellet in eaten_power_pellets:
        time_start = time.time()
        v_points = 200
        for ghost in ghost_group:
            if ghost.state == 'A' or ghost.state == 'C':
                ghost.toggle_vulnerability()
        
    # Check if all Pellets are eaten
    if len(pellets) == 0:
        load_game()
        movement = 'R'
        last_movement = 'R'
    
    # check if Pacman collided with any Ghosts
    # If so, check if they are vulnerable
    # If true, destroy the sprite
    # If not, quit the game
    collided_ghosts = pygame.sprite.spritecollide(pacman, ghost_group, False)
    for ghost in collided_ghosts:
        if ghost.state == 'V':
            ghost.toggle_death()
            text = font_system_small.render(f"{v_points}", True, constants.WHITE)
            v_points += 200
            window.blit(text, (ghost.rect.x, ghost.rect.y))
            pygame.display.update()
            POINTS += v_points
            time.sleep(0.5)
        elif ghost.state == 'A' or ghost.state == 'C':
            pygame.mixer.Sound("../audio/death-quack.wav").play()
            window.fill(constants.BLACK)
            pygame.display.update()
            LIVES -= 1
            pacman.death()
            if LIVES == 0:
                Retry()
                load_game()
                POINTS = 0
                LIVES = 3            
            else:
                continue_game()
            
            movement = 'R'
            last_movement = 'R'
        
    # Move Ghost to Respawning Area if they collide with entrance and are dead
    for ghost in ghost_group:
        if ghost.state == 'D' and pygame.sprite.spritecollide(ghost, respawner, False):
            ghost.state = 'R'
            p_list.append(ghost)

    # Update game
    update_window()
    
    # Increment loop
    loop = loop + 1
