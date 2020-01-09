import pygame

import math
import my_events

import my_menu
import sound_helper

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE
)

from session import *

MENU_FONT_SIZE = 60

#http://guru2.nobody.jp/music/sorato.mid by Misaki Shin / G2-MIDI
BGM_PATH = "media/sorato.ogg"

# A session for the title screen
class TitleSession(Session):
    '''
    Creates a new title session
    Parameters:
        self: the object being created
        screen: the surface of the gameplay window
        misc_dict: A dictionary with any additional arguments in case the next session needs it
    '''
    def __init__(self, screen, misc_dict):
        super(TitleSession, self).__init__(screen, misc_dict)
        # https://www.pexels.com/photo/photo-of-blue-sky-912110/ by Elia Clerici
        self.background_surface = pygame.image.load("img/title_background.png").convert_alpha()
        self.next_session_key = "battle"
        menu_midtop = (math.floor(self.screen_rect.width * 0.7), math.floor(self.screen_rect.height * 0.3))

        self.font = pygame.font.Font(None, MENU_FONT_SIZE )

        self.menu = my_menu.VerticalMenu(self.font, RED, BLACK, DARK_STEEL, SILVER, menu_midtop)
        '''
        Starts a battle session
        Parameters:
            key: the key being pressed
        '''
        def on_battle_item(key):
            if key == K_SPACE:
                self.next_session_key = "battle"
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )

        self.menu.add("To Battle", on_battle_item)

        '''
        Starts a session to view high scores
        Parameters:
            key: the key being pressed
        '''
        def on_view_scores_item(key):
            if key == K_SPACE:
                self.next_session_key = "view_scores"
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.menu.add("View Scores (Hardest Settings)", on_view_scores_item)

        '''
        Starts a configuration session
        Parameters:
            key: the key being pressed
        '''
        def on_config_item(key):
            if key == K_SPACE:
                self.next_session_key = "config"
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.menu.add("Configuration", on_config_item)

        '''
        Soft quits the game. Generally the safest way to end the game
        Parameters:
            key: the key being pressed
        '''
        def on_quit_item(key):
            if key == K_SPACE:
                self.next_session_key = None
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )

        self.menu.add("Soft Quit", on_quit_item)

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
            #self.menu.init_surf_rect_list()
            self.menu.draw(self.screen)

            self.write_key_prompt("Space to confirm, arrow keys to change menu selection")

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key, {}
