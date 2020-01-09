import pygame

from sys import (
exit
)
import math

import my_events

import score_helper
import sound_helper
import my_menu

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE
)

from session import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
SILVER = (192, 192, 192)
DARK_STEEL = (24,24,24)

BGM_PATH = "media/sorato.ogg"

SCORE_FONT_SIZE = 50

# A class to view the current top scores
class ViewScoresSession(Session):
    '''
    Creates a new session to view the high scores
    Parameters:
        self: the object being created
        screen: the surface of the gameplay window
        misc_dict: A dictionary with any additional arguments in case the next session needs it
    '''
    def __init__(self, screen, misc_dict):
        super(ViewScoresSession, self).__init__(screen, misc_dict)
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE )

        self.next_session_key = "title"
        # https://www.pexels.com/photo/advertisements-batch-blur-business-518543/ by brotiN biswaS
        self.background_surface = self.background_surface = pygame.image.load("img/newspaper.png").convert_alpha()
        menu_midtop = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.3))

        self.score_menu = my_menu.VerticalMenu(self.score_font, BLUE, BLACK, RED, WHITE, menu_midtop)
        '''
        Plays a clapping sound when interacting with scores
        Parameters:
            key: the key pressed
        '''
        def on_score_entry(key):
            if key == K_SPACE:
                sound_helper.play_clip("ovation")

        for i in range(0, len(score_helper.scores) ):
            name = score_helper.scores[i]["name"]
            score = score_helper.scores[i]["score"]
            line = "%d.  %s  %d" % ( (i + 1) , name, score)
            self.score_menu.add(line, on_score_entry)
        '''
        Return to title
        Parameters:
            key: the key pressed
        '''
        def on_return(key):
            if key == K_SPACE:
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.score_menu.add("Return", on_return)

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
                    self.score_menu.process_input(event.key)
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
            
            self.score_menu.draw(self.screen)

            self.write_key_prompt("Space to confirm selection. Confirm a score to hear the Republic's gratitude.")

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key, {}
