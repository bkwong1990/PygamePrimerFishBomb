import pygame
from sys import (
exit
)

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

#initialize mixer and pygame
pygame.mixer.init()
pygame.init()

FONT_SIZE = 28

#Speed limits

HARD_SPEED_MAX = 50
HARD_SPEED_MIN = 10

# Tank count limits
HARD_TANK_COUNT_MAX = 4
HARD_TANK_COUNT_MIN = 1

SCORE_FRAME_DURATION = 60

SKY_COLOR = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)

PLAYER_SPEED = 7
CLOUD_SPEED = 2
TANK_SPEED = 1
BOMB_DROP_SPEED = 10
BOMB_RELOAD_TIME = 4000

# "Go Without Seeing Back" by Makoto Saita https://big-up.style/musics/34958?wovn=en
BGM_PATH = "media/01_go_without_seeing_back_.ogg"

# a class representing a single session of gameplay
class BattleSession(session.Session):


    def __init__(self, screen):
        super(BattleSession, self).__init__(screen)
        self.can_bomb = True
        self.score = 0
        self.current_tank_count = 0

        self.missile_maxspeed = config_helper.config_info["missile_maxspeed"]
        self.missile_maxpeed = max(min(HARD_SPEED_MAX, self.missile_maxspeed), HARD_SPEED_MIN)

        self.max_tank_count = config_helper.config_info["max_tank_count"]

        self.init_sprite_groups()

        self.font = pygame.font.Font(None, FONT_SIZE )

        self.init_battle_area()

        self.player = my_sprites.Player(self.battle_rect.x, self.screen_rect.width, self.battle_rect.y, self.screen_rect.height, PLAYER_SPEED)
        self.spacebar_prompt = my_sprites.MovingSpaceBarPrompt(self.player, (0, self.player.rect.height))
        self.all_sprites.add(self.player, self.spacebar_prompt)

    def init_sprite_groups(self):
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.misc_sprites = pygame.sprite.Group()
        self.temp_text_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def init_battle_area(self):
        # create battle surface based on the screen dimensions
        battle_width = 1000
        battle_height = self.screen_rect.height
        battle_x = self.screen_rect.width - battle_width

        self.battle_surf = pygame.Surface( (battle_width, battle_height) )
        self.battle_surf.fill(SKY_COLOR)
        self.battle_rect = self.battle_surf.get_rect(x = battle_x, y = 0)
        #return (battle_surf, battle_rect)

    def set_event_timers(self, missile_interval, cloud_interval, tank_interval):
        # timers for missiles, clouds, and the tank
        pygame.time.set_timer(my_events.ADDMISSILE, missile_interval)
        pygame.time.set_timer(my_events.ADDCLOUD, cloud_interval)
        pygame.time.set_timer(my_events.ADDTANK, tank_interval)

    def stop_event_timers(self):
        #Setting the time interval to 0 stop the events from being posted.
        pygame.time.set_timer(my_events.ADDMISSILE, 0)
        pygame.time.set_timer(my_events.ADDCLOUD, 0)
        pygame.time.set_timer(my_events.ADDTANK, 0)
        print("Battle event timers have been stopped")

    def simple_update_all(self):
        self.enemies.update()
        self.misc_sprites.update()
        self.player_projectiles.update()
        self.temp_text_sprites.update()

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
            self.score += self.missile_maxspeed + (100 * self.current_tank_count)

    def write_info(self, clock):
        #display score
        score_text = self.font.render("Score: %015d" % self.score, True, BLACK )
        self.screen.blit(score_text, (5, 5))
        #displayspeed
        speed_text = self.font.render("Speed: %03d" % self.missile_maxspeed, True, BLACK )
        self.screen.blit(speed_text, (5, self.font.get_height() * 2))

        #Display FPS
        fps_text = self.font.render("FPS: %.2f" % clock.get_fps(), True, BLACK )
        self.screen.blit(fps_text, (5, self.font.get_height() * 4))

    def handle_events(self, events):

        running = True
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.can_bomb & self.player.alive():
                        new_bomb = my_sprites.PlayerBomb(self.player.rect.centerx, self.player.rect.bottom, self.battle_rect.height, BOMB_DROP_SPEED)
                        self.all_sprites.add(new_bomb)
                        self.player_projectiles.add(new_bomb)
                        self.can_bomb = False
                        pygame.time.set_timer(my_events.RELOADBOMB, BOMB_RELOAD_TIME, True)
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        exit(0)
            elif event.type == QUIT:
                pygame.quit()
                exit(0)
            elif event.type == my_events.ADDMISSILE:
                #create a new enemy and add it to sprite groups
                new_missile = my_sprites.Missile(self.battle_rect.x, self.screen_rect.width, self.battle_rect.y, self.battle_rect.height, self.missile_maxspeed)
                self.enemies.add(new_missile)
                self.all_sprites.add(new_missile)
            elif event.type == my_events.ADDCLOUD:
                #create new cloud
                new_cloud = my_sprites.Cloud(self.battle_rect.x, self.screen_rect.width, self.battle_rect.y, self.battle_rect.height, CLOUD_SPEED)
                self.misc_sprites.add(new_cloud)
                self.all_sprites.add(new_cloud)
            elif event.type == my_events.ADDTANK:
                if self.current_tank_count < self.max_tank_count:
                    new_tank = my_sprites.LaserTank(self.battle_rect.x, self.screen_rect.width, self.battle_rect.height, TANK_SPEED,  self.player)
                    self.enemies.add(new_tank)
                    self.all_sprites.add(new_tank)
                    self.current_tank_count += 1
                else:
                    print("Too many tanks, can't spawn more")
            elif event.type == my_events.ADDLASER:
                new_laser = my_sprites.Laser(event.centerx, event.bottom)
                self.enemies.add(new_laser)
                self.all_sprites.add(new_laser)
            elif event.type == my_events.MAKESOUND:
                #SOUND_DICT[event.sound_index].play()
                sound_helper.play_clip(event.sound_index)
            elif event.type == my_events.ADDEXPLOSION:
                new_explosion = my_sprites.Explosion(event.rect)
                self.all_sprites.add(new_explosion)
                self.misc_sprites.add(new_explosion)
                sound_helper.play_clip("explosion")
            elif event.type == my_events.RELOADBOMB:
                if self.player.alive():
                    self.can_bomb = True
                    sound_helper.play_clip("reloaded")
            elif event.type == my_events.SCOREBONUS:
                self.score += event.score
                text_sprite = my_sprites.TextSprite("+ %d" % event.score, self.font, DARK_GREEN, event.center, SCORE_FRAME_DURATION, False)
                self.temp_text_sprites.add(text_sprite)
            elif event.type == my_events.TANKDEATH:
                self.current_tank_count -= 1
                self.current_tank_count = max(self.current_tank_count, 0)
            elif event.type == my_events.NEXTSESSION:
                running = False
        return running

    def run_loop(self):
        clock = pygame.time.Clock()
        self.set_event_timers(missile_interval = 500, cloud_interval = 1000, tank_interval = 6000)

        #create info Surface
        info_surface = pygame.Surface( (self.battle_rect.x, self.screen_rect.height) )
        info_surface.fill( WHITE )

        running = True
        #self.start_bgm()
        sound_helper.load_music_file(BGM_PATH)
        while running:
            running = self.handle_events(pygame.event.get())

            #Get the key press list and update the player's position
            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)
            self.spacebar_prompt.update(self.can_bomb)

            self.simple_update_all()

            #fill screen with white
            self.screen.fill( WHITE )

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
        return "title"
