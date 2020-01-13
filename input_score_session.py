import pygame

from sys import (
exit
)
import math

import my_events
import session
import sound_helper
import score_helper

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE,
K_BACKSPACE,
K_RETURN,
K_KP_ENTER,
TEXTINPUT
)

from session import *

NAME_INPUT_FONT_SIZE = 70

# A session for inputting a new score
class InputScoreSession(Session):
    '''
    Creates a new session to input a new score
    Parameters:
        self: the object being created
        screen: the surface of the gameplay window
        misc_dict: A dictionary with any additional arguments in case the next session needs it
    '''
    def __init__(self, screen, misc_dict):
        super(InputScoreSession, self).__init__(screen, misc_dict)
        self.namestring = ""
        self.text_input_font = pygame.font.Font(None, NAME_INPUT_FONT_SIZE )
        self.next_session_key = "title"
        # I took this pic with my phone
        self.background_surface = pygame.image.load("img/keyboard.png").convert_alpha()
        self.text_rect = pygame.Rect(0, 0, NAME_INPUT_FONT_SIZE * 6, NAME_INPUT_FONT_SIZE)
        self.text_rect.center = self.screen_rect.center

        self.click_on_keypress = False

        self.event_handler_dict[TEXTINPUT] = self.on_text_input


    def on_keydown(self, event):
        Session.on_keydown(self, event)
        # I accounted for both enter keys
        if (event.key == K_RETURN) or (event.key == K_KP_ENTER):
            if self.namestring != "":
                score_helper.add_score( self.namestring.strip(), self.misc_dict["score"] )
                score_helper.save_scores()
                self.running = False
        elif event.key == K_BACKSPACE:
            # I have to manually erase a character at the end of the name string
            if len(self.namestring) > 0:
                self.namestring = self.namestring[:len(self.namestring) - 1]
        elif event.key == K_ESCAPE:
            force_quit()

    def on_text_input(self, event):
        if len(self.namestring) < score_helper.NAME_CHAR_LIMIT:
            self.namestring += event.text




    '''
    Writes the currently constructed text
    Parameters:
        self: the calling object
    '''
    def write_input_text(self):
        input_back_surf = pygame.Surface(self.text_rect.size)
        input_back_surf.fill(WHITE)
        input_back_surf.set_alpha(255//2)

        text_surface = self.text_input_font.render(self.namestring, True, BLACK, WHITE)
        self.screen.blit(input_back_surf, self.text_rect)
        self.screen.blit(text_surface, self.text_rect)

    '''
    Writes a label near the input area
    Parameters:
        self: the calling object
    '''
    def write_label(self):
        label_surface = self.key_prompt_font.render("Congrats, you scored %d pts" % self.misc_dict["score"], True, BLACK, WHITE)
        label_rect = label_surface.get_rect(midbottom = self.text_rect.midtop)

        label_rect.move_ip(0, -1)
        self.screen.blit(label_surface, label_rect)

    '''
    Runs the main loop until events force it to quit
    Parameters:
        self: the calling object
    Return: the string key for the next session, a dict containing values needed for the next session
    '''
    def run_loop(self):
        self.running = True

        clock = pygame.time.Clock()


        while self.running:
            self.handle_events( pygame.event.get() )

            self.screen.blit(self.background_surface, (0, 0) )

            self.write_key_prompt("Press enter to input your name into high score list")
            self.write_input_text()
            self.write_label()

            pygame.display.flip()

            clock.tick(60)
        return "title", {}
