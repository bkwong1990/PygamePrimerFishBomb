import pygame

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE
)

import my_sprites

import my_events
import session
import sound_helper
import config_helper
import score_helper


'''
#initialize mixer and pygame
pygame.mixer.init()
pygame.init()
'''
FONT_SIZE = 28

#Score indicators should expire in 60 frames or 1 second
SCORE_FRAME_DURATION = 60

#Some colors not used in other session classes
SKY_COLOR = (135, 206, 235)
DARK_GREEN = (0, 100, 0)
#other variables for gameplay
PLAYER_SPEED = 7
CLOUD_SPEED = 2
TANK_SPEED = 1
BOMB_DROP_SPEED = 10
BOMB_RELOAD_TIME = 4000

# "Go Without Seeing Back" by Makoto Saita https://big-up.style/musics/34958?wovn=en
BGM_PATH = "media/01_go_without_seeing_back_.ogg"

# a class representing a single session of gameplay
class BattleSession(session.Session):

    '''
    Creates a new battle session
    Parameters:
        self: the object being created
        screen: the surface of the gameplay window
        misc_dict: A dictionary with any additional arguments in case the next session needs it
    '''
    def __init__(self, screen, misc_dict):
        super(BattleSession, self).__init__(screen, misc_dict)
        self.can_bomb = True
        self.score = 0
        self.current_tank_count = 0

        self.missile_top_speed = config_helper.config_info["missile_maxspeed"]

        self.max_tank_count = config_helper.config_info["max_tank_count"]

        self.init_sprite_groups()

        self.font = pygame.font.Font(None, FONT_SIZE )

        self.init_battle_area()

        self.player = my_sprites.Player(self.battle_rect.x, self.screen_rect.width, self.battle_rect.y, self.screen_rect.height, PLAYER_SPEED)
        self.spacebar_prompt = my_sprites.MovingSpaceBarPrompt(self.player, (0, self.player.rect.height))
        self.all_sprites.add(self.player, self.spacebar_prompt)

        self.click_on_keypress = False

        self.event_handler_dict[my_events.ADDMISSILE] = self.on_add_missile
        self.event_handler_dict[my_events.ADDCLOUD] = self.on_add_cloud
        self.event_handler_dict[my_events.ADDTANK] = self.on_add_tank
        self.event_handler_dict[my_events.ADDLASER] = self.on_add_laser
        self.event_handler_dict[my_events.ADDEXPLOSION] = self.on_add_explosion
        self.event_handler_dict[my_events.RELOADBOMB] = self.on_reload_bomb
        self.event_handler_dict[my_events.SCOREBONUS] = self.on_score_bonus
        self.event_handler_dict[my_events.TANKDEATH] = self.on_tank_death

    '''
    Initializes the session's sprite groups
    Parameters:
        self: the calling object
    '''
    def init_sprite_groups(self):
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.misc_sprites = pygame.sprite.Group()
        self.temp_text_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    '''
    Initializes the surface and rectangle used to display the gameplay combat
    Parameters:
        self: the calling object
    '''
    def init_battle_area(self):
        # create battle surface based on the screen dimensions
        battle_width = 1000
        battle_height = self.screen_rect.height
        battle_x = self.screen_rect.width - battle_width

        self.battle_surf = pygame.Surface( (battle_width, battle_height) )
        self.battle_surf.fill(SKY_COLOR)
        self.battle_rect = self.battle_surf.get_rect(x = battle_x, y = 0)


    '''
    Sets the timer for events that must occur periodically
    Parameters:
        self: the calling object
        missile_interval: the interval of missile spawn in milliseconds
        cloud_interval: the interval of cloud spawn in milliseconds
        tank_interval: the interval of tank spawn in milliseconds
    '''
    def set_event_timers(self, missile_interval, cloud_interval, tank_interval):
        # timers for missiles, clouds, and the tank
        pygame.time.set_timer(my_events.ADDMISSILE, missile_interval)
        pygame.time.set_timer(my_events.ADDCLOUD, cloud_interval)
        pygame.time.set_timer(my_events.ADDTANK, tank_interval)

    '''
    Stops all the repeating event timers
    Parameters:
        self: the calling object
    '''
    def stop_event_timers(self):
        #Setting the time interval to 0 stop the events from being posted.
        pygame.time.set_timer(my_events.ADDMISSILE, 0)
        pygame.time.set_timer(my_events.ADDCLOUD, 0)
        pygame.time.set_timer(my_events.ADDTANK, 0)
        print("Battle event timers have been stopped")
    '''
    Updates all sprite groups that use the empty update method
    Parameters:
        self: the calling object
    '''
    def simple_update_all(self):
        self.enemies.update()
        self.misc_sprites.update()
        self.player_projectiles.update()
        self.temp_text_sprites.update()

    '''
    Checks if the player has collided with an enemy and adds points if they survived. If not,
    prepare to end the gameplay session.
    Parameters:
        self: the calling object
    '''
    def check_player_life(self):
        if self.player.alive():
            #If a collision occured, enemy_collider will be non-None, an actual enemy
            enemy_collider = pygame.sprite.spritecollideany(self.player, self.enemies)
            #if a collision occured, remove the player and stop the loop in a few seconds
            if enemy_collider:
                self.player.kill()
                #The enemy dies depending on its kill_on_contact instance var
                if enemy_collider.kill_on_contact:
                    enemy_collider.kill()
                #Prepare to quit
                pygame.time.set_timer(my_events.NEXTSESSION, 3000, True)
            # Add survival points to score
            self.score += self.missile_top_speed + (score_helper.SCORE_PER_LIVING_TANK * self.current_tank_count)

    '''
    Writes information to the info section of the screen
    Parameters:
        self: the calling object
        clock: the clock that manages the game's speed
    '''
    def write_info(self, clock):
        #display current score
        score_text = self.font.render("Score: %d" % self.score, True, session.BLACK )
        self.screen.blit(score_text, (5, 5))

        top_score = 0 if len(score_helper.scores) == 0 else score_helper.scores[0]["score"]

        #display top score
        top_score_text = self.font.render("Top Score: %d" % top_score, True, session.BLACK )
        self.screen.blit(top_score_text, (5, self.font.get_height() * 2))
        #display speed
        speed_text = self.font.render("Speed: %d" % self.missile_top_speed, True, session.BLACK )
        self.screen.blit(speed_text, (5, self.font.get_height() * 4))

        #display max tank count
        tank_text = self.font.render("Max allowed tanks: %d" % self.max_tank_count, True, session.BLACK )
        self.screen.blit(tank_text, (5, self.font.get_height() * 6))

        #Display FPS
        fps_text = self.font.render("FPS: %.2f" % clock.get_fps(), True, session.BLACK )
        self.screen.blit(fps_text, (5, self.font.get_height() * 8))

    def on_keydown(self, event):
        session.Session.on_keydown(self, event)
        if event.key == K_SPACE:
            #The player shouldn't be able to launch bombs if they're dead
            if self.can_bomb & self.player.alive():
                new_bomb = my_sprites.PlayerBomb(self.player.rect.centerx, self.player.rect.bottom, self.battle_rect.height, BOMB_DROP_SPEED)
                self.all_sprites.add(new_bomb)
                self.player_projectiles.add(new_bomb)
                self.can_bomb = False
                #The bomb has a reload time to force the player to fight accurately
                pygame.time.set_timer(my_events.RELOADBOMB, BOMB_RELOAD_TIME, True)
        elif event.key == K_ESCAPE:
            session.force_quit()

    def on_add_missile(self, event):
        #create a new enemy and add it to sprite groups
        new_missile = my_sprites.Missile(self.battle_rect.x, self.screen_rect.width, self.battle_rect.y, self.battle_rect.height, self.missile_top_speed)
        self.enemies.add(new_missile)
        self.all_sprites.add(new_missile)

    def on_add_cloud(self, event):
        #create new cloud
        new_cloud = my_sprites.Cloud(self.battle_rect.x, self.screen_rect.width, self.battle_rect.y, self.battle_rect.height, CLOUD_SPEED)
        self.misc_sprites.add(new_cloud)
        self.all_sprites.add(new_cloud)

    def on_add_tank(self, event):
        if self.current_tank_count < self.max_tank_count:
            #Creates a new tank and increments the counter of tanks
            new_tank = my_sprites.LaserTank(self.battle_rect.x, self.screen_rect.width, self.battle_rect.height, TANK_SPEED,  self.player)
            self.enemies.add(new_tank)
            self.all_sprites.add(new_tank)
            self.current_tank_count += 1
        else:
            print("Too many tanks, can't spawn more")

    def on_add_laser(self, event):
        new_laser = my_sprites.Laser(event.centerx, event.bottom)
        self.enemies.add(new_laser)
        self.all_sprites.add(new_laser)

    def on_add_explosion(self, event):
        new_explosion = my_sprites.Explosion(event.rect)
        self.all_sprites.add(new_explosion)
        self.misc_sprites.add(new_explosion)
        sound_helper.play_clip("explosion")

    def on_reload_bomb(self, event):
        #Reloading is impossible if the player is dead
        if self.player.alive():
            self.can_bomb = True
            sound_helper.play_clip("reloaded")

    def on_score_bonus(self, event):
        bonus_score = score_helper.ENEMY_SCORES[event.enemy_name]
        self.score += bonus_score
        text_sprite = my_sprites.TextSprite("+ %d" % bonus_score, self.font, DARK_GREEN, event.center, SCORE_FRAME_DURATION, False)
        self.temp_text_sprites.add(text_sprite)

    def on_tank_death(self, event):
        #the max statement might not be needed, but it's there in case the count was not incremented properly in ADDTANK
        self.current_tank_count -= 1
        self.current_tank_count = max(self.current_tank_count, 0)


    '''
    Runs the main loop until events force it to quit
    Parameters:
        self: the calling object
    Return: the string key for the next session, a dict containing values needed for the next session
    '''
    def run_loop(self):
        clock = pygame.time.Clock()
        self.set_event_timers(missile_interval = 500, cloud_interval = 1000, tank_interval = 6000)

        #create info Surface
        info_surface = pygame.Surface( (self.battle_rect.x, self.screen_rect.height) )
        info_surface.fill( session.WHITE )

        self.running = True
        #self.start_bgm()
        sound_helper.load_music_file(BGM_PATH)
        while self.running:
            self.handle_events(pygame.event.get())

            #Get the key press list and update the player's position
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)
            self.spacebar_prompt.update(self.can_bomb)

            self.simple_update_all()

            #fill screen with white
            self.screen.fill( session.WHITE )

            #draw battle portion of screen
            self.screen.blit(self.battle_surf, self.battle_rect )

            #draw all sprites
            self.all_sprites.draw(self.screen)

            #Temporary text is drawn separately and later to ensure z-order
            self.temp_text_sprites.draw(self.screen)
            #draw info Surface
            self.screen.blit(info_surface, (0, 0) )
            self.write_info(clock)

            #Handle collision between player projectiles and enemies
            pygame.sprite.groupcollide(self.player_projectiles, self.enemies, True, True)
            self.check_player_life()

            pygame.display.flip()

            #Force fps
            clock.tick(60)
        self.stop_event_timers()
        #pygame.mixer.music.stop()
        print("Final score: %015d" % self.score)
        # The score should get added if it's higher than 5th place and the game difficulty is maxed
        if score_helper.is_score_high_enough(self.score) and config_helper.is_on_hardest_setting():
            return "input_score", {"score": self.score}
        # If the score and difficulty are insufficient, return to title
        return "title", {}
