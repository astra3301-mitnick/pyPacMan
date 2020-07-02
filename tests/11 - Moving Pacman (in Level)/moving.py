import os, sys, pygame

from pygame.locals import *

from Pellet import Pellet
from Pacman import Pacman
from Box import Box

# initialize pygame
pygame.init()
mainClock = pygame.time.Clock()

# constants
WINDOWWIDTH = 448 #(16 * 28) (row numbers range from 0 - 27)
WINDOWHEIGHT = 512 #(16 * 32) (column numbers range from 0 - 31)
SPRITEWIDTH = 16
SPRITEHEIGHT = 16

# initialize window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

# initialize colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# set background
background = pygame.image.load('../../sprites/pacman-level.png')
windowSurface.blit(background, (0, 0))

# pixels per loop
MOVESPEED = 16

# Create Boxes for collisions
box_group = pygame.sprite.Group()

# Pellets
pellet_group = pygame.sprite.Group()

# Teleporters
teleporter_left = pygame.sprite.GroupSingle(Box(0, 16 * 15, BLUE))
teleporter_right = pygame.sprite.GroupSingle(Box(16 * 27, 16 * 15, BLUE))

# goes through the entire map and outlines which 16x16 areas are black
# and which ones are not
# this identifies where Pacman and Pellets can and cannot spawn
list = [3, 4, 8, 9, 10, 17, 18, 19, 23, 24]
columns = [i * SPRITEWIDTH for i in list]
x = 0
y = 16
while y < WINDOWHEIGHT:
    while x < WINDOWWIDTH:
        selected_area = pygame.Rect(x, y, 16, 16)
        cropped_image = background.subsurface(selected_area)
        if pygame.transform.average_color(cropped_image)[:3] == BLACK:
            if y == SPRITEHEIGHT*4:
                if not x in columns:
                    pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
            elif not (y >= SPRITEHEIGHT*10 and y <= SPRITEHEIGHT*20):
                pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
            else:
                if x == SPRITEWIDTH*6 or x == SPRITEWIDTH*21:
                    pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
        else:
            box_group.add(Box(x, y, RED))
           
        x += 16
    y += 16
    x = 0
    
# create pacman and set coordinates to the center of the surface
pacman = Pacman(224, 384, MOVESPEED, box_group) # 16 * 14, 16 * 24
pacman_group = pygame.sprite.GroupSingle(pacman)

# Initialize movement variable
movement = 'R'
last_movement = 'R'

# draw pellets
pellet_group.draw(windowSurface)
pacman_group.draw(windowSurface)

# update display
pygame.display.update()

def update_surface():
    # redraw the background and sprite
    windowSurface.blit(background, (0, 0))
    box_group.draw(windowSurface)
    pellet_group.draw(windowSurface)
    pacman_group.draw(windowSurface)
    
    # update the game
    pygame.display.update()
    mainClock.tick(10)

def transport_right(sprite):
    while sprite.rect.left <= WINDOWWIDTH:
        sprite.rect.right += 2
        update_surface()
        
    sprite.rect.right = 0
    
    while sprite.rect.left <= 0:
        sprite.rect.right += 2
        update_surface()
        
    sprite.rect = pygame.Rect(16 * 1, 16 * 15, 16, 16)
    
def transport_left(sprite):
    while sprite.rect.right >= 0:
        sprite.rect.left -= 2
        update_surface()
        
    sprite.rect.left = WINDOWWIDTH
    
    while sprite.rect.right >= WINDOWWIDTH:
        sprite.rect.left -= 2
        update_surface()
        
    sprite.rect = pygame.Rect(16 * 26, 16 * 15, 16, 16)
    
def test_movement(move, speed, pacman):
    test = Box(pacman.rect.x, pacman.rect.y, RED)
    global last_movement
    if move == 'U':
        test.rect.top -= speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            last_movement = 'U'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)
    elif move == 'D':
        test.rect.bottom += speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            last_movement = 'D'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)
    elif move == 'L':
        test.rect.left -= speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            last_movement = 'L'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)
    elif move == 'R':
        test.rect.right += speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            last_movement = 'R'
            pacman_group.update(move)
        else:
            test_last_movement(last_movement, speed, pacman)

def test_last_movement(move, speed, pacman):
    test = Box(pacman.rect.x, pacman.rect.y, RED)
    global last_movement
    if move == 'U':
        test.rect.top -= speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    elif move == 'D':
        test.rect.bottom += speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    elif move == 'L':
        test.rect.left -= speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
    elif move == 'R':
        test.rect.right += speed
        if not pygame.sprite.spritecollide(test, box_group, False):
            pacman_group.update(move)
        else:
            pacman_group.update('')
        
        
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
                
    # move the sprite(pacman)
    test_movement(movement, MOVESPEED, pacman)
    
    # check if Pacman collided with any Pellets in Pellet Group
    # true = Pellet will be destroyed when collided with
    pygame.sprite.spritecollide(pacman, pellet_group, True)
    
    if pygame.sprite.spritecollide(pacman, teleporter_left, False):
        transport_left(pacman)
        
    if pygame.sprite.spritecollide(pacman, teleporter_right, False):
        transport_right(pacman)
    
    update_surface()