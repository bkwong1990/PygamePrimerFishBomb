import pygame
from sys import (
exit
)

import math
import my_events
import session
import my_menu
import config_helper
import copy
import sound_helper

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE,
K_LEFT,
K_RIGHT,
RLEACCEL
)

MENU_FONT_SIZE = 60
KEYPROMPT_FONT_SIZE = 28

from session import *

#http://guru2.nobody.jp/music/sorato.mid
BGM_PATH = "media/sorato.ogg"

class ConfigSession(Session):
    def __init__(self, screen, misc_dict):
        super(ConfigSession, self).__init__(screen, misc_dict)
        #https://www.pexels.com/photo/architect-architecture-blueprint-build-271667/
        self.config_candidate = copy.deepcopy(config_helper.config_info)

        self.background_surface = pygame.image.load("img/config_background.png").convert_alpha()
        self.next_session_key = "title"

        menu_midtop = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.2))

        self.font = pygame.font.Font(None, MENU_FONT_SIZE )

        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )

        self.menu = my_menu.VerticalMenu(self.font, BLUE, BLACK, DARK_STEEL, SILVER, menu_midtop)

        def on_fullscreen_item(key):
            if key == K_SPACE:
                self.config_candidate["fullscreen"] = not(self.config_candidate["fullscreen"])
                self.menu.set_text_current_selection("Fullscreen: " + str(self.config_candidate["fullscreen"]))

        self.menu.add("Fullscreen: " + str(self.config_candidate["fullscreen"]), on_fullscreen_item)

        def on_missile_speed_item(key):
            if key == K_LEFT:
                self.config_candidate["missile_maxspeed"] -= 5
            elif key == K_RIGHT:
                self.config_candidate["missile_maxspeed"] += 5
            self.config_candidate["missile_maxspeed"] = config_helper.correct_missile_speed(self.config_candidate["missile_maxspeed"])
            self.menu.set_text_current_selection("Missile Max Speed: " + str(self.config_candidate["missile_maxspeed"]))

        self.menu.add("Missile Max Speed: " + str(self.config_candidate["missile_maxspeed"]), on_missile_speed_item)

        def on_tank_count_item(key):
            if key == K_LEFT:
                self.config_candidate["max_tank_count"] -= 1
            elif key == K_RIGHT:
                self.config_candidate["max_tank_count"] += 1
            self.config_candidate["max_tank_count"] = config_helper.correct_tank_count(self.config_candidate["max_tank_count"])
            self.menu.set_text_current_selection("Max Tank Count: " + str(self.config_candidate["max_tank_count"]))

        self.menu.add("Max Tank Count: " + str(self.config_candidate["max_tank_count"]), on_tank_count_item)

        def on_save_and_return(key):
            if key == K_SPACE:
                if config_helper.config_info["fullscreen"] != self.config_candidate["fullscreen"]:
                    if self.config_candidate["fullscreen"]:
                        pygame.display.set_mode( self.screen_rect.size , flags=pygame.SCALED|pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode( self.screen_rect.size , flags=pygame.SCALED)
                config_helper.config_info.update(self.config_candidate)
                config_helper.save_config()
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.menu.add("Save and Return", on_save_and_return)

        def on_return(key):
            if key == K_SPACE:
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.menu.add("Return", on_return)


    def handle_events(self, events):
        running = True
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            elif event.type == my_events.NEXTSESSION:
                running = False
            elif event.type == KEYDOWN:
                sound_helper.play_clip("tactile_click")
                if event.key == K_ESCAPE:
                    #pygame.quit()
                    #exit(0)
                    pygame.event.post(pygame.event.Event(QUIT))
                else:
                    self.menu.process_input(event.key)

        return running
    

    def run_loop(self):
        sound_helper.load_music_file(BGM_PATH)
        running = True
        clock = pygame.time.Clock()
        while running:
            running = self.handle_events( pygame.event.get() )
            self.screen.blit(self.background_surface, (0, 0) )
            #self.menu.init_surf_rect_list()
            self.menu.draw(self.screen)

            self.write_key_prompt("Space to confirm, up/down keys to change selection, left/right keys to adjust numerical values")

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key, {}
