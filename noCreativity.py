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
K_SPACE
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

SCORE_FRAME_DURATION = 60

SKY_COLOR = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

missile_maxspeed = 20
player_speed = 7
cloud_speed = 2
tank_speed = 1
bomb_drop_speed = 10

#initialize score
score = 0

#initialize bomb status
can_bomb = True

pygame.mixer.init()
pygame.init()
#Set title
pygame.display.set_caption("My CO Hates Me and Sent Me on a Suicide Mission")

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
player = my_sprites.Player(BATTLE_X, SCREEN_WIDTH, 0, BATTLE_HEIGHT, player_speed)

#create a group of enemies
enemies = pygame.sprite.Group()
pygame.time.set_timer(my_events.ADDTANK, 250, True)

#create a group of clouds
clouds = pygame.sprite.Group()

#create group of player projectiles
player_projectiles = pygame.sprite.Group()

#create a group of miscellaneous sprites
misc_sprites = pygame.sprite.Group()

#create a group of temp text sprites. These should be drawn last for max visibility
temp_text_sprites = pygame.sprite.Group()

#create a group of all game pieces (enemies + player + clouds)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup clock to change framerate
clock = pygame.time.Clock()

#load and set volume of main BGM
pygame.mixer.music.load("media/01_go_without_seeing_back_.ogg")
pygame.mixer.music.play(loops=-1)
volume = pygame.mixer.music.get_volume() * 0.4
pygame.mixer.music.set_volume(volume)

#dictionary to hold sound objects
sound_dict = {
"explosion": pygame.mixer.Sound("media/explosion.ogg"),
"laser": pygame.mixer.Sound("media/Laser.ogg"),
"reloaded": pygame.mixer.Sound("media/reloaded.ogg")
}

#define functions
def handle_events(events):
    global missile_maxspeed
    global score
    global can_bomb
    running = True
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_x:
                missile_maxspeed += 10
                missile_maxspeed = min(missile_maxspeed, HARD_SPEED_MAX)
            elif event.key == K_z:
                if missile_maxspeed > HARD_SPEED_MIN:
                    missile_maxspeed -= 10
                    missile_maxspeed = max(missile_maxspeed, HARD_SPEED_MIN)
                    score //= 2
            elif event.key == K_SPACE:
                if can_bomb & player.alive():
                    new_bomb = my_sprites.PlayerBomb(player.rect.centerx, player.rect.bottom, BATTLE_HEIGHT, bomb_drop_speed)
                    all_sprites.add(new_bomb)
                    player_projectiles.add(new_bomb)
                    can_bomb = False
                    pygame.time.set_timer(my_events.RELOADBOMB, 4000, True)
        elif event.type == QUIT:
            running = False
        elif event.type == my_events.ADDMISSILE:
            #create a new enemy and add it to sprite groups
            new_missile = my_sprites.Missile(BATTLE_X, SCREEN_WIDTH, 0, BATTLE_HEIGHT, missile_maxspeed)
            enemies.add(new_missile)
            all_sprites.add(new_missile)
        elif event.type == my_events.ADDCLOUD:
            #create new cloud
            new_cloud = my_sprites.Cloud(BATTLE_X, SCREEN_WIDTH, 0, BATTLE_HEIGHT, cloud_speed)
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        elif event.type == my_events.ADDTANK:
            new_tank = my_sprites.LaserTank(BATTLE_X, SCREEN_WIDTH, BATTLE_HEIGHT, tank_speed,  player)
            enemies.add(new_tank)
            all_sprites.add(new_tank)
        elif event.type == my_events.ADDLASER:
            new_laser = my_sprites.Laser(event.centerx, event.bottom)
            enemies.add(new_laser)
            all_sprites.add(new_laser)
        elif event.type == my_events.MAKESOUND:
            sound_dict[event.sound_index].play()
        elif event.type == my_events.ADDEXPLOSION:
            new_explosion = my_sprites.Explosion(event.rect)
            all_sprites.add(new_explosion)
            misc_sprites.add(new_explosion)
            sound_dict["explosion"].play()
        elif event.type == my_events.RELOADBOMB:
            if player.alive():
                can_bomb = True
                sound_dict["reloaded"].play()
        elif event.type == my_events.SCOREBONUS:
            score += event.score
            text_sprite = my_sprites.TempText("+ %d" % event.score, info_font, (0, 100, 0), event.rect.center, SCORE_FRAME_DURATION
            )
            temp_text_sprites.add(text_sprite)

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
    player.update(pressed_keys, can_bomb)

    #update enemy, cloud, and misc sprite positions
    enemies.update()
    clouds.update()
    misc_sprites.update()
    player_projectiles.update()
    temp_text_sprites.update()

    #fill screen with white
    screen.fill( WHITE )

    #draw battle portion of screen
    screen.blit(battle_surf, (BATTLE_X, 0) )

    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Temporary text is drawn separately and later to ensure z-order
    for entity in temp_text_sprites:
        screen.blit(entity.surf, entity.rect)

    #draw info Surface
    write_info()

    #Handle collision between player projectiles and enemies
    pygame.sprite.groupcollide(player_projectiles, enemies, True, True)


    if player.alive():
        #If a collision occured, enemy_collider will be non-None, an actual enemy
        enemy_collider = pygame.sprite.spritecollideany(player, enemies)
        #if a collision occured, remove the player and stop the loop in a few seconds
        if enemy_collider:
            #draw explosion
            player.kill()
            #The enemy dies depending on its kill_on_contact instance var
            if enemy_collider.kill_on_contact:
                enemy_collider.kill()
            #Prepare to quit
            pygame.time.set_timer(QUIT, 3000, True)

        score += missile_maxspeed
    pygame.display.flip()

    #Force fps
    clock.tick(60)
print("Final score: %010d" % score)
pygame.mixer.music.stop()
pygame.mixer.quit()
