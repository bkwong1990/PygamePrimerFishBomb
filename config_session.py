import pygame

import math
import my_events
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
#KEYPROMPT_FONT_SIZE = 28

from session import *

#http://guru2.nobody.jp/music/sorato.mid
BGM_PATH = "media/sorato.ogg"

# A class representing a session to edit game settings
class ConfigSession(Session):
    '''
    Creates a new configuration session
    Parameters:
        self: the object being created
        screen: the surface of the gameplay window
        misc_dict: A dictionary with any additional arguments in case the next session needs it
    '''
    def __init__(self, screen, misc_dict):
        super(ConfigSession, self).__init__(screen, misc_dict)
        # https://www.pexels.com/photo/architect-architecture-blueprint-build-271667/ by Pixabay
        self.config_candidate = copy.deepcopy(config_helper.config_info)

        self.background_surface = pygame.image.load("img/config_background.png").convert_alpha()
        self.next_session_key = "title"

        menu_midtop = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.2))

        self.font = pygame.font.Font(None, MENU_FONT_SIZE )


        self.menu = my_menu.VerticalMenu(self.font, BLUE, BLACK, DARK_STEEL, SILVER, menu_midtop)

        '''
        Sets the game to display in either window or fullscreen
        Parameters:
            key: the key being pressed
        '''
        def on_fullscreen_item(key):
            if key == K_SPACE:
                self.config_candidate["fullscreen"] = not(self.config_candidate["fullscreen"])
                self.menu.set_text_current_selection("Fullscreen: " + str(self.config_candidate["fullscreen"]))

        self.menu.add("Fullscreen: " + str(self.config_candidate["fullscreen"]), on_fullscreen_item)

        '''
        Sets the maximum speed of the missiles
        Parameters:
            key: the key being pressed
        '''
        def on_missile_speed_item(key):
            if key == K_LEFT:
                self.config_candidate["missile_maxspeed"] -= 5
            elif key == K_RIGHT:
                self.config_candidate["missile_maxspeed"] += 5
            self.config_candidate["missile_maxspeed"] = config_helper.correct_missile_speed(self.config_candidate["missile_maxspeed"])
            self.menu.set_text_current_selection("Missile Max Speed: " + str(self.config_candidate["missile_maxspeed"]))

        self.menu.add("Missile Max Speed: " + str(self.config_candidate["missile_maxspeed"]), on_missile_speed_item)

        '''
        Sets the maximum tanks that can be onscreen at the same time
        Parameters:
            key: the key being pressed
        '''
        def on_tank_count_item(key):
            if key == K_LEFT:
                self.config_candidate["max_tank_count"] -= 1
            elif key == K_RIGHT:
                self.config_candidate["max_tank_count"] += 1
            self.config_candidate["max_tank_count"] = config_helper.correct_tank_count(self.config_candidate["max_tank_count"])
            self.menu.set_text_current_selection("Max Tank Count: " + str(self.config_candidate["max_tank_count"]))

        self.menu.add("Max Tank Count: " + str(self.config_candidate["max_tank_count"]), on_tank_count_item)

        '''
        Saves the configuration and returns to the title
        Parameters:
            key: the key being pressed
        '''
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

        '''
        Returns to title without saving
        Parameters:
            key: the key being pressed
        '''
        def on_return(key):
            if key == K_SPACE:
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.menu.add("Return", on_return)

    '''
    Executes code based on what events are posted
    Parameters:
        self: the calling object
        events: the collection of events
    Return: a boolean indicating if the main loop should continue
    '''
    def handle_events(self, events):
        running = True
        for event in events:
            if event.type == QUIT:
                force_quit()
            elif event.type == my_events.NEXTSESSION:
                running = False
            elif event.type == KEYDOWN:
                sound_helper.play_clip("tactile_click")
                if event.key == K_ESCAPE:
                    force_quit()
                else:
                    self.menu.process_input(event.key)

        return running

    '''
    Runs the main loop until events force it to quit
    Parameters:
        self: the calling object
    Return: the string key for the next session, a dict containing values needed for the next session
    '''
    def run_loop(self):
        sound_helper.load_music_file(BGM_PATH)
        running = True
        clock = pygame.time.Clock()
        while running:
            running = self.handle_events( pygame.event.get() )
            self.screen.blit(self.background_surface, (0, 0) )

            self.menu.draw(self.screen)

            self.write_key_prompt("Space to confirm, up/down keys to change selection, left/right keys to adjust numerical values")

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key, {}
