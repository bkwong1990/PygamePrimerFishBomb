#Change list
#12/23/2019: Initial checkin

import pygame
import my_events

from pygame.locals import (
RLEACCEL,
K_UP,
K_DOWN,
K_LEFT,
K_RIGHT
)
#RNG needed for enemies and clouds
import random

#A class representing the player character
class Player(pygame.sprite.Sprite):
    '''
    Creates a new player
    Parameters:
        self: the object being created
        left_bound, right_bound, top_bound, bottom_bound (int): the numbers indicating the boundaries of the space the player is in
        player_speed (int): The amount of pixels the player can move per frame. Diagonal movement is faster
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
    '''
    def __init__(self, left_bound, right_bound, top_bound, bottom_bound, player_speed, colorkey):
        super(Player, self).__init__()
        #Set image
        self.surf = pygame.image.load("img/jet6.png").convert_alpha()
        #self.surf.set_colorkey( colorkey, RLEACCEL )
        self.rect = self.surf.get_rect()
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.top_bound = top_bound
        self.bottom_bound = bottom_bound
        self.player_speed = player_speed

    '''
    Updates the player's position based on the pressed keys. The player cannot pass the boundaries of the containing area.
    Parameters:
        self: The calling object
        pressed_keys: a collection that shows which keys were pressed for the current frame
    '''
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.player_speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.player_speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.player_speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.player_speed, 0)

        #Check if in bounds
        self.rect.left = self.left_bound if (self.rect.left < self.left_bound) else self.rect.left
        self.rect.right = self.right_bound if (self.rect.right > self.right_bound) else self.rect.right
        self.rect.top = self.top_bound if (self.rect.top < self.top_bound) else self.rect.top
        self.rect.bottom = self.bottom_bound if (self.rect.bottom > self.bottom_bound) else self.rect.bottom
    def kill(self):
        explosion_event = pygame.event.Event(my_events.ADDEXPLOSION, center = self.rect.center)
        pygame.event.post(explosion_event)
        pygame.sprite.Sprite.kill(self)

#A missile to shoot down the player
class Missile(pygame.sprite.Sprite):
    '''
    Creates a new missile
    Parameters:
        self: the object being created
        left_bound, right_bound, top_bound, bottom_bound (int): the numbers indicating the boundaries of the space the missile is in
        missile_maxspeed (int): The maximum speed the missile can get from the RNG
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
    '''
    def __init__(self, left_bound, right_bound, top_bound, bottom_bound, missile_maxspeed, colorkey):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("img/missile6.png").convert_alpha()
        #self.surf.set_colorkey( colorkey, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                #Missile can generate out of view on right side of screen
                random.randint(right_bound + 20, right_bound + 100),
                random.randint(0, bottom_bound)
            )
        )
        self.left_bound = left_bound
        self.speed = random.randint(5, missile_maxspeed)
    '''
    Updates the missile's position. The missile will be killed upon going through the left side of the containing space.
    Parameters:
        self: The calling object
    '''
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < self.left_bound:
            self.kill()
#A cloud that does nothing
class Cloud(pygame.sprite.Sprite):
    '''
    Creates a new cloud
    Parameters:
        self: the object being created
        left_bound, right_bound, top_bound, bottom_bound (int): the numbers indicating the boundaries of the space the cloud is in
        cloud_speed (int): The cloud's speed
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
    '''
    def __init__(self, left_bound, right_bound, top_bound, bottom_bound, cloud_speed, colorkey):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("img/cloud4.png").convert_alpha()
        #self.surf.set_colorkey( colorkey, RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(right_bound + 20, right_bound + 100),
                random.randint(top_bound, bottom_bound)
            )
        )
        self.left_bound = left_bound
        self.speed = cloud_speed

    '''
    Updates the cloud's position. The cloud will be killed upon going through the left side of the containing space.
    Parameters:
        self: The calling object
    '''
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < self.left_bound:
            self.kill()

#A tank enemy that follows the player's position and shoots lasers
class LaserTank(pygame.sprite.Sprite):
    LASER_COOLDOWN = 300
    SPAWN_TIME = 10000
    '''
    Creates a new tank
    Parameters:
        self: the object being created
        left_bound, right_bound, bottom_bound (int): the numbers indicating the boundaries of the space the tank is in
        tank_speed (int): The number of pixels the tank can move per frame
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
        target (anything with a Rect instance variable): The object being tracked by the tank
        laser_event_type (event type): The event type to be used to create a laser
        respawn_event_type (event type): The event type to be used to force another tank to spawn
    '''
    def __init__(self, left_bound, right_bound, bottom_bound, tank_speed, colorkey, target):
        super(LaserTank, self).__init__()
        self.surf = pygame.image.load("img/tank3.png").convert_alpha()
        #self.surf.set_colorkey(colorkey, RLEACCEL)

        width = self.surf.get_rect().width
        height = self.surf.get_rect().height
        self.rect = self.surf.get_rect()

        self.rect.centerx = random.randint(left_bound + width // 2, right_bound - width // 2)
        self.rect.bottom = bottom_bound

        self.left_bound = left_bound
        self.right_bound = right_bound
        self.bottom_bound = bottom_bound

        self.target = target
        self.speed = tank_speed
        self.frames_until_laser = LaserTank.LASER_COOLDOWN
        #self.laser_event_type = my_events.ADDLASER
        self.frames_until_movement = 0;

    '''
    Updates the tank's position. The tank will track the player, but cannot pass the boundaries of the screen.
    Parameters:
        self: The calling object
    '''
    def update(self):
        if self.frames_until_movement <= 0 & self.target.alive():
            if self.target.rect.centerx < self.rect.centerx:
                self.rect.move_ip(-self.speed, 0)
            elif self.target.rect.centerx > self.rect.centerx:
                self.rect.move_ip(self.speed, 0)

            self.rect.left = self.left_bound if (self.rect.left < self.left_bound) else self.rect.left
            self.rect.right = self.right_bound if (self.rect.right > self.right_bound) else self.rect.right
        else:
            #The tank can't move until it's done firing the laser.
            self.frames_until_movement = self.frames_until_movement - 1

        #The tank has a cooldown time for the laser
        if self.frames_until_laser <= 0:
            self.frames_until_laser = LaserTank.LASER_COOLDOWN
            self.frames_until_movement = Laser.LASER_DURATION
            self.rect.bottom = self.bottom_bound
            #creates a laser event object that also contains the coordinates to start the laser at
            laser_event = pygame.event.Event(my_events.ADDLASER, centerx = self.rect.centerx, bottom = self.rect.top)
            pygame.event.post(laser_event)
        else:
            if self.frames_until_laser == 60:
                sfx_event = pygame.event.Event(my_events.MAKESOUND, sound_index="laser")
                pygame.event.post(sfx_event)
            if self.frames_until_laser <= 60:
                #Suspend movement for one second before the laser fires.
                self.frames_until_movement = Laser.LASER_DURATION
            self.frames_until_laser -= 1
    '''
    Kills the tank, but not before setting a one-time timer to force another tank to spawn
    '''
    def kill(self):
        pygame.time.set_timer(my_events.ADDTANK, LaserTank.SPAWN_TIME, True)
        pygame.sprite.Sprite.kill(self)

#A laser that pierces the heavens
class Laser(pygame.sprite.Sprite):
    LASER_DURATION = 10
    '''
    Creates a new laser
    Parameters:
        self: The object being created
        centerx: The horizontal coordinate of the laser's center
        bottom: The vertical coordinate of the laser's bottom
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
    '''
    def __init__(self, centerx, bottom, colorkey):
        super(Laser, self).__init__()
        self.surf = pygame.image.load("img/laser.png").convert_alpha()
        #self.surf.set_colorkey(colorkey, RLEACCEL)

        self.rect = self.surf.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom

        self.frame_duration = Laser.LASER_DURATION

    '''
    Updates the laser's position and counts down the frames until the laser expires
    Parameters:
        self: The calling object
    '''
    def update(self):
        if self.frame_duration == 0:
            self.kill()
        self.frame_duration -= 1

class Explosion(pygame.sprite.Sprite):

    COLUMNS = 8
    ROWS = 4

    def __init__(self, center, colorkey):
        super(Explosion, self).__init__()
        self.animation_surf = pygame.image.load("img/explosion.png").convert_alpha()
        #self.animation_surf.set_colorkey(colorkey, RLEACCEL)


        animation_rect = self.animation_surf.get_rect()
        self.surf_width = animation_rect.width // Explosion.COLUMNS
        self.surf_height = animation_rect.height // Explosion.ROWS

        self.rect = pygame.Rect( (0,0), (self.surf_width, self.surf_height) )
        self.rect.center = center

        self.current_frame = 0
        self.surf = self.get_surf()

    def update(self):
        if(self.current_frame >= 32):
            self.kill()
        else:
            self.surf = self.get_surf()
            self.current_frame += 1

    def get_surf(self):
        current_column = min(self.current_frame % Explosion.COLUMNS, Explosion.COLUMNS - 1)
        current_row = min(self.current_frame // Explosion.COLUMNS, Explosion.ROWS - 1)

        current_x = current_column * self.surf_width
        current_y = current_row * self.surf_width

        return self.animation_surf.subsurface((current_x, current_y, self.surf_width, self.surf_height))
