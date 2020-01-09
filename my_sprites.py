#Change list
#12/23/2019: Initial checkin

import pygame

import math

from pygame.locals import (
RLEACCEL,
K_UP,
K_DOWN,
K_LEFT,
K_RIGHT
)
#RNG needed for enemies and clouds
import random
#Using from import because I don't need every event.
from my_events import (
ADDTANK,
ADDLASER,
MAKESOUND,
TANKDEATH,
post_explosion,
post_score_bonus
)

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
    def __init__(self, left_bound, right_bound, top_bound, bottom_bound, player_speed):
        super(Player, self).__init__()

        # https://thenounproject.com/term/fighter-jet/59845/

        self.image = pygame.image.load("img/jet.png").convert_alpha()

        self.rect = self.image.get_rect( centery = (bottom_bound - top_bound) // 2)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.top_bound = top_bound
        self.bottom_bound = bottom_bound
        self.player_speed = player_speed

    '''
    Updates the player's position based on the pressed keys. The player cannot pass the boundaries of the containing area.
    Also updates the player's sprite depending on whether or not the bomb is ready
    Parameters:
        self: The calling object
        pressed_keys: a collection that shows which keys were pressed for the current frame
        can_bomb: a boolean indicating if the player's bomb is ready and loaded
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
    '''
    Posts explosion event and removes this sprite from all sprite groups it belongs to
    Parameters:
        self: the calling object
    '''
    def kill(self):
        post_explosion(self.rect)
        pygame.sprite.Sprite.kill(self)
#A superclass for all enemy sprites with shared behavior
class Enemy(pygame.sprite.Sprite):
    '''
    Creates a new enemy with default values for its instance vars
    Parameters:
        self: the object being created
    '''
    def __init__(self):
        super(Enemy, self).__init__()
        self.kill_on_contact = True
        self.enemy_name = ""
        self.rect = None
        self.explode_on_death = True
    '''
    Posts a score event and an explosion event.
    Removes enemy sprite from all sprite groups
    If this behavior is unneeded, use pygame.sprite.Sprite.kill(self)
    Parameters:
        self: the calling object
    '''
    def kill(self):
        #Post score bonus event
        if self.enemy_name != "":
            post_score_bonus(self.enemy_name, self.rect.center)
        #If the enemy is supposed to explode on death, post an explosion event
        if self.explode_on_death:
            post_explosion(self.rect)
        pygame.sprite.Sprite.kill(self)

#A missile to shoot down the player
class Missile(Enemy):
    '''
    Creates a new missile
    Parameters:
        self: the object being created
        left_bound, right_bound, top_bound, bottom_bound (int): the numbers indicating the boundaries of the space the missile is in
        missile_maxspeed (int): The maximum speed the missile can get from the RNG
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
    '''
    def __init__(self, left_bound, right_bound, top_bound, bottom_bound, missile_maxspeed):
        super(Missile, self).__init__()
        # https://premiumbpthemes.com/explore/missile-transparent-background.html
        self.image = pygame.image.load("img/missile.png").convert_alpha()

        self.rect = self.image.get_rect(
            center=(
                #Missile can generate out of view on right side of screen
                random.randint(right_bound + 20, right_bound + 100),
                random.randint(0, bottom_bound)
            )
        )
        self.left_bound = left_bound
        self.speed = random.randint(5, missile_maxspeed)
        self.enemy_name = "missile"
    '''
    Updates the missile's position. The missile will be killed upon going through the left side of the containing space.
    Parameters:
        self: The calling object
    '''
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < self.left_bound:
            #Use default sprite kill to prevent needless explosion & score increase
            pygame.sprite.Sprite.kill(self)

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
    def __init__(self, left_bound, right_bound, top_bound, bottom_bound, cloud_speed):
        super(Cloud, self).__init__()
        # https://www.cleanpng.com/png-cloud-computing-dust-676210/preview.html
        self.image = pygame.image.load("img/cloud.png").convert_alpha()

        self.rect = self.image.get_rect(
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
class LaserTank(Enemy):
    LASER_COOLDOWN = 300
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
    def __init__(self, left_bound, right_bound, bottom_bound, tank_speed, target):
        super(LaserTank, self).__init__()
        # https://huntpng.com/keyword/tank-sprite-png
        self.image = pygame.image.load("img/tank.png").convert_alpha()

        width = self.image.get_rect().width
        height = self.image.get_rect().height
        self.rect = self.image.get_rect()

        self.rect.centerx = random.randint(left_bound + width // 2, right_bound - width // 2)
        self.rect.bottom = bottom_bound

        self.left_bound = left_bound
        self.right_bound = right_bound
        self.bottom_bound = bottom_bound

        self.target = target
        self.speed = tank_speed
        self.frames_until_laser = LaserTank.LASER_COOLDOWN

        self.frames_until_movement = 0;

        self.enemy_name = "tank"

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
            laser_event = pygame.event.Event(ADDLASER, centerx = self.rect.centerx, bottom = self.rect.top)
            pygame.event.post(laser_event)
        else:
            if self.frames_until_laser == 60:
                sfx_event = pygame.event.Event(MAKESOUND, sound_index="laser")
                pygame.event.post(sfx_event)
            if self.frames_until_laser <= 60:
                #Suspend movement for one second before the laser fires.
                self.frames_until_movement = Laser.LASER_DURATION
            self.frames_until_laser -= 1
    '''
    Set a one-time timer to force another tank to spawn and removes the tank from
    all sprite groups it belongs to
    Parameters:
        self: The calling object
    '''
    def kill(self):
        pygame.event.post( pygame.event.Event(TANKDEATH) )
        Enemy.kill(self)

#A laser that pierces the heavens
class Laser(Enemy):
    LASER_DURATION = 10
    '''
    Creates a new laser
    Parameters:
        self: The object being created
        centerx: The horizontal coordinate of the laser's center
        bottom: The vertical coordinate of the laser's bottom
        color_key ( (int, int, int) ): The color to be considered transparent for the converted sprite image. RGB numbers.
    '''
    def __init__(self, centerx, bottom):
        super(Laser, self).__init__()
        self.image = pygame.image.load("img/laser.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom

        self.frame_duration = Laser.LASER_DURATION
        self.kill_on_contact = False
        #Making the laser and player bomb collide is difficult, but possible
        self.enemy_name = "laser"
        self.explode_on_death = False
    '''
    Updates the laser's position and counts down the frames until the laser expires
    Parameters:
        self: The calling object
    '''
    def update(self):
        if self.frame_duration <= 0:
            #If killed by timeout, use Sprite.kill
            pygame.sprite.Sprite.kill(self)
        self.frame_duration -= 1

#An explosion sprite with animation
class Explosion(pygame.sprite.Sprite):

    #define expected columns, rows, total frames, and slowness multiplier
    COLUMNS = 8
    ROWS = 4
    TOTAL_FRAMES = COLUMNS * ROWS
    #This will cause frames to be repeated and make the animation slower.
    SLOW_MULTIPLIER = 3

    '''
    Creates a new explosion
    Parameters:
        self: The object being created
        center: the center of the explosion
    '''
    def __init__(self, target_rect):
        super(Explosion, self).__init__()
        #Get the surface of the spritesheet
        # https://www.pnglot.com/i/hJJxmbR_example-sprite-sheet-animation-sprite-sheet-particle-unity/
        original_surf = pygame.image.load("img/explosion.png").convert_alpha()

        #Get the rectable of the spritesheet
        original_rect = original_surf.get_rect()

        #get the length of the longest side of the target rectangle
        longest_length = max(target_rect.width, target_rect.height) * 2

        #get the width and height of each cell in the spritesheet
        original_col_width = original_rect.width // Explosion.COLUMNS
        original_row_height = original_rect.height // Explosion.ROWS

        #get the width : height ratio of each cell
        aspect_ratio = original_col_width / original_row_height

        #Rescale the height of the sprite_sheet
        scaled_height = longest_length * Explosion.ROWS
        #Rescale the width of the spritesheet
        scaled_width = math.floor(longest_length * aspect_ratio) * Explosion.COLUMNS
        #Rescale the spritesheet so that each cell covers the target rectangle
        self.animation_surf = pygame.transform.scale(original_surf, (scaled_width, scaled_height))
        animation_rect = self.animation_surf.get_rect()
        #Calculate the width and height of each cell in the new spritesheet surface
        self.image_width = animation_rect.width // Explosion.COLUMNS
        self.image_height = animation_rect.height // Explosion.ROWS

        #set the rect of the sprite
        self.rect = pygame.Rect( (0,0), (self.image_width, self.image_height) )
        self.rect.center = target_rect.center

        self.current_frame = 0
        #initialize the surface with the first cell of the spritesheet
        self.image = self.next_surf()
    '''
    Updates the explosion's current surface. Position is unchanged.
    Parameters:
        self: The calling object
    '''
    def update(self):
        if(self.current_frame >= Explosion.TOTAL_FRAMES * Explosion.SLOW_MULTIPLIER):
            self.kill()
        else:
            self.image = self.next_surf()
            self.current_frame += 1
    '''
    Returns a new surface for the explosion based on the current frame
    '''
    def next_surf(self):
        current_column = min((self.current_frame // Explosion.SLOW_MULTIPLIER) % Explosion.COLUMNS, Explosion.COLUMNS - 1)
        current_row = min((self.current_frame // Explosion.SLOW_MULTIPLIER) // Explosion.COLUMNS, Explosion.ROWS - 1)

        current_x = current_column * self.image_width
        current_y = current_row * self.image_width

        return self.animation_surf.subsurface((current_x, current_y, self.image_width, self.image_height))

#A bomb dropped by the player.
class PlayerBomb(pygame.sprite.Sprite):
    #the number of pixels the bomb should horizontally drift per frame
    DRIFT = 4
    '''
    Creates a new player bomb
    Parameters:
        self: The object being created
        centerx: the horizontal center of the bomb
        top: the vertical coordinate of the top of the bomb
        bottom_bound: the bottom of the space in which the bomb is allowed to exist
        fall_speed: the vertical speed at which the bomb falls
    '''
    def __init__(self, centerx, top, bottom_bound, fall_speed):
        super(PlayerBomb, self).__init__()
        # https://opengameart.org/content/2d-retro-fish
        self.image = pygame.image.load("img/fish_bomb.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.top = top
        self.speed = fall_speed

        self.bottom_bound = bottom_bound
    '''
    Updates the bomb's position. Kills bomb if it goes past the bottom of screen
    Parameters:
        self: The calling object
    '''
    def update(self):
        self.rect.move_ip(PlayerBomb.DRIFT, self.speed)
        if self.rect.top > self.bottom_bound:
            self.kill()
    '''
    Posts an explosion event and removes the bomb from all sprite groups it belongs to
    Parameters:
        self: The calling object
    '''
    def kill(self):
        post_explosion(self.rect)
        pygame.sprite.Sprite.kill(self)
#A text sprite that disappears after a certain amount of frames
class TextSprite(pygame.sprite.Sprite):
    '''
    Creates a text sprite
    Parameters:
        self: The object being created
        text: the text to be displayed
        font: the font with which to write the text
        color: the color of the text
        center: the center of the text's rectangle
        frame_duration: the amount of frames the text should stay onscreen
    '''
    def __init__(self, text, font, color, center, frame_duration = 60, is_permanent = True):
        super(TextSprite, self).__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(
        center = center
        )
        self.frame_duration = frame_duration
        self.is_permanent = is_permanent
    '''
    Counts down the frames until the text expires
    Parameters:
        self: the calling object
    '''
    def update(self):
        if not(self.is_permanent) and (self.frame_duration <= 0):
            self.kill()
        self.frame_duration -= 1
# A spacebar prompt that follows a target sprite
class MovingSpaceBarPrompt(pygame.sprite.Sprite):

    '''
    Creates a new spacebar prompt
    Parameters:
        self: the object being created
        target: the sprite the spacebar is following
        offset: the x, y distance the spacebar should be from the target
    '''
    def __init__(self, target, offset):
        super(MovingSpaceBarPrompt, self).__init__()

        # I made this with pixelartmaker.com
        self.image = pygame.image.load("img/spacebar.png").convert_alpha()
        # Use the default image to denote that the spacebar is ready to be used
        self.ready_surf = self.image
        # I pasted the following image on top of the spacebar to show that it's not to be used
        # https://publicdomainvectors.org/en/free-clipart/Stop-process-icon/67213.html
        self.not_ready_surf = pygame.image.load("img/spacebar_no.png").convert_alpha()
        self.rect = self.image.get_rect( center = target.rect.center )

        self.rect.move_ip(offset)
        self.offset = offset

        self.target = target
    '''
    Updates the position and image of the spacebar
    Parameters:
        self: the spacebar to be updated
        is_ready: a boolean indicating if the spacebar is ready to be used
    '''
    def update(self, is_ready):
        if self.target.alive():

            self.image = self.ready_surf if is_ready else self.not_ready_surf

            self.rect.center = self.target.rect.center
            self.rect.move_ip(self.offset)

        else:
            self.kill()
