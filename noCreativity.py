'''
Todo:
Enemy tanks. Drop bombs on them. Tanks can shoot back.
Have plane shoot missiles
'''

import pygame

#RNG
#import random

from pygame.locals import (
RLEACCEL,
K_UP,
K_DOWN,
K_LEFT,
K_RIGHT,
K_ESCAPE,
K_z,
K_x,
KEYDOWN,
QUIT,
)

import my_sprites

#Screen Resolution
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Battle Surface dimensions
BATTLE_WIDTH = 1000
BATTLE_HEIGHT = SCREEN_HEIGHT

BATTLE_X = SCREEN_WIDTH - BATTLE_WIDTH

HARD_SPEED_MAX = 50
HARD_SPEED_MIN = 10

SKY_COLOR = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

missile_maxspeed = 20
player_speed = 7
cloud_speed = 2
tank_speed = 1

#initialize score
score = 0

pygame.mixer.init()
pygame.init()

#Create screen object

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

#create battle Surface
battle_surf = pygame.Surface( (BATTLE_WIDTH, BATTLE_HEIGHT) )
battle_surf.fill( SKY_COLOR )

#create info Surface
info_surface = pygame.Surface( (BATTLE_X, SCREEN_HEIGHT) )
info_surface.fill( WHITE )

#create font for info area
font_size = 28
info_font = pygame.font.Font(None, font_size)

import my_events

#Create a custom event for adding a new Enemy
#ADDMISSILE = pygame.USEREVENT + 1
pygame.time.set_timer(my_events.ADDMISSILE, 500)

#Custom event and timer for clouds
#ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(my_events.ADDCLOUD, 1000)

#Custom event for Tanks Laser
#ADDTANK = pygame.USEREVENT + 3
#ADDLASER = pygame.USEREVENT + 4
#MAKESOUND = pygame.USEREVENT + 5

#instantiate Player
player = my_sprites.Player(BATTLE_X, SCREEN_WIDTH, 0, BATTLE_HEIGHT, player_speed, SKY_COLOR)

#create a group of enemies
enemies = pygame.sprite.Group()
pygame.time.set_timer(my_events.ADDTANK, 250, True)

#create a group of clouds
clouds = pygame.sprite.Group()
#create a group of all game pieces (enemies + player)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup clock to change framerate
clock = pygame.time.Clock()

pygame.mixer.music.load("media/01_go_without_seeing_back_.ogg")
pygame.mixer.music.play(loops=-1)
volume = pygame.mixer.music.get_volume() * 0.4
pygame.mixer.music.set_volume(volume)

laser_sound = pygame.mixer.Sound("media/explosion.ogg")

#define functions
def handle_events(events):
    global missile_maxspeed
    global score
    running = True
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_x:
                missile_maxspeed += 10
                missile_maxspeed = min(missile_maxspeed, HARD_SPEED_MAX)
            elif event.key == K_z:
                missile_maxspeed -= 10
                missile_maxspeed = max(missile_maxspeed, HARD_SPEED_MIN)
                score = score // 2
        elif event.type == QUIT:
            running = False
        elif event.type == my_events.ADDMISSILE:
            #create a new enemy and add it to sprite groups
            new_missile = my_sprites.Missile(BATTLE_X, SCREEN_WIDTH, 0, BATTLE_HEIGHT, missile_maxspeed, SKY_COLOR)
            enemies.add(new_missile)
            all_sprites.add(new_missile)
        elif event.type == my_events.ADDCLOUD:
            #create new cloud
            new_cloud = my_sprites.Cloud(BATTLE_X, SCREEN_WIDTH, 0, BATTLE_HEIGHT, cloud_speed, SKY_COLOR)
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        elif event.type == my_events.ADDTANK:
            new_tank = my_sprites.LaserTank(BATTLE_X, SCREEN_WIDTH, BATTLE_HEIGHT, tank_speed, SKY_COLOR, player)
            enemies.add(new_tank)
            all_sprites.add(new_tank)
        elif event.type == my_events.ADDLASER:
            new_laser = my_sprites.Laser(event.centerx, event.bottom, SKY_COLOR)
            enemies.add(new_laser)
            all_sprites.add(new_laser)
        elif event.type == my_events.MAKESOUND:
            pygame.mixer.Sound(event.filename).play()
    return running

def write_info():
    screen.blit(info_surface, (0, 0) )
    #display score
    score_text = info_font.render("Score: %010d" % score, True, BLACK )
    screen.blit(score_text, (5, 5))
    #displayspeed
    speed_text = info_font.render("Speed: %03d" % missile_maxspeed, True, BLACK )
    screen.blit(speed_text, (5, font_size * 2))

    #Display instructions

    lower_speed_text = info_font.render("Slow down w/Z (1/2 Score)", True, BLACK )
    screen.blit(lower_speed_text, (5, font_size * 4))

    raise_speed_text = info_font.render("Speed up w/X", True, BLACK )
    screen.blit(raise_speed_text, (5, font_size * 6))

    #Display FPS
    fps_text = info_font.render("FPS: %.2f" % clock.get_fps(), True, BLACK )
    screen.blit(fps_text, (5, font_size * 8))

running = True
while running:
    #Go through event collection
    running = handle_events(pygame.event.get())

    #Get the key press list and update the player's position
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #update enemy position
    enemies.update()
    clouds.update()

    #fill screen with white
    screen.fill( WHITE )

    #draw battle portion of screen
    screen.blit(battle_surf, (BATTLE_X, 0) )

    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #draw info Surface
    write_info()

    #Check if any enemies have collided with the Player

    if pygame.sprite.spritecollideany(player, enemies):
        #if a collision occured, remove the player and stop the loop
        player.kill()
        running = False

    score += missile_maxspeed
    pygame.display.flip()

    #Force fps
    clock.tick(60)
print("Final score: %010d" % score)
pygame.mixer.music.stop()
pygame.mixer.quit()
