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

from battle_session import (
HARD_SPEED_MIN,
HARD_SPEED_MAX,
HARD_TANK_COUNT_MIN,
HARD_TANK_COUNT_MAX
)

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

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SILVER = (192, 192, 192)
DARK_STEEL = (24,24,24)

class ConfigSession(session.Session):
    def __init__(self, screen, config_info):
        super(ConfigSession, self).__init__(screen, config_info)
        #https://www.pexels.com/photo/architect-architecture-blueprint-build-271667/
        self.config_candidate = copy.deepcopy(self.config_info)

        self.background_surface = pygame.image.load("img/config_background.png").convert_alpha()
        self.next_session_key = "title"

        menu_midtop = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.2))

        self.font = pygame.font.Font(None, MENU_FONT_SIZE )
        self.shadow_font = pygame.font.Font(None, MENU_FONT_SIZE)

        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )

        self.menu = my_menu.BaseMenu(self.font, BLUE, self.shadow_font, BLACK, DARK_STEEL, SILVER, menu_midtop)

        def on_fullscreen_item(key):
            if key == K_SPACE:
                self.config_candidate["fullscreen"] = not(self.config_candidate["fullscreen"])
                self.menu.set_text_current_selection("Fullscreen: " + str(self.config_candidate["fullscreen"]))

        self.menu.add("Fullscreen: " + str(self.config_candidate["fullscreen"]), on_fullscreen_item)

        def on_missile_speed_item(key):
            if key == K_LEFT:
                self.config_candidate["missile_maxspeed"] -= 5
                self.config_candidate["missile_maxspeed"] = max(self.config_candidate["missile_maxspeed"], HARD_SPEED_MIN)
            elif key == K_RIGHT:
                self.config_candidate["missile_maxspeed"] += 5
                self.config_candidate["missile_maxspeed"] = min(self.config_candidate["missile_maxspeed"], HARD_SPEED_MAX)
            self.menu.set_text_current_selection("Missile Max Speed: " + str(self.config_candidate["missile_maxspeed"]))

        self.menu.add("Missile Max Speed: " + str(self.config_candidate["missile_maxspeed"]), on_missile_speed_item)

        def on_tank_count_item(key):
            if key == K_LEFT:
                self.config_candidate["max_tank_count"] -= 1
                self.config_candidate["max_tank_count"] = max(self.config_candidate["max_tank_count"], HARD_TANK_COUNT_MIN)
            elif key == K_RIGHT:
                self.config_candidate["max_tank_count"] += 1
                self.config_candidate["max_tank_count"] = min(self.config_candidate["max_tank_count"], HARD_TANK_COUNT_MAX)
            self.menu.set_text_current_selection("Max Tank Count: " + str(self.config_candidate["max_tank_count"]))

        self.menu.add("Max Tank Count: " + str(self.config_candidate["max_tank_count"]), on_tank_count_item)

        def on_save_and_return(key):
            if key == K_SPACE:
                if self.config_info["fullscreen"] != self.config_candidate["fullscreen"]:
                    if self.config_candidate["fullscreen"]:
                        pygame.display.set_mode( self.screen_rect.size , flags=pygame.SCALED|pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode( self.screen_rect.size , flags=pygame.SCALED)
                self.config_info.update(self.config_candidate)
                config_helper.save_config(self.config_info)
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
                if event.key == K_ESCAPE:
                    #pygame.quit()
                    #exit(0)
                    pygame.event.post(pygame.event.Event(QUIT))
                else:
                    self.menu.process_input(event.key)

        return running

    def write_key_prompt(self):
        text_surface = self.key_prompt_font.render("Space to confirm, up/down keys to change selection, left/right keys to adjust numerical values", True, RED)
        text_rect = text_surface.get_rect(center = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.97)) )

        back_rect = text_rect.copy()
        back_rect.width += 10
        back_rect.height += 5
        back_rect.center = text_rect.center

        back_surf = pygame.Surface(back_rect.size)
        back_surf.fill(DARK_STEEL)
        self.screen.blit(back_surf, back_rect)
        self.screen.blit(text_surface, text_rect)

    def run_loop(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            running = self.handle_events( pygame.event.get() )
            self.screen.blit(self.background_surface, (0, 0) )
            #self.menu.init_surf_rect_list()
            self.menu.draw(self.screen)

            self.write_key_prompt()

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key
