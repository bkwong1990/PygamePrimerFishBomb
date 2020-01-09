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
K_KP_ENTER
)

from session import *

NAME_INPUT_FONT_SIZE = 70
KEYPROMPT_FONT_SIZE = 28

class InputScoreSession(Session):
    def __init__(self, screen, misc_dict):
        super(InputScoreSession, self).__init__(screen, misc_dict)
        self.namestring = ""
        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )
        self.text_input_font = pygame.font.Font(None, NAME_INPUT_FONT_SIZE )
        self.next_session_key = "title"
        # I took this pic with my phone
        self.background_surface = pygame.image.load("img/keyboard.png").convert_alpha()
        self.text_rect = pygame.Rect(0, 0, NAME_INPUT_FONT_SIZE * 11, NAME_INPUT_FONT_SIZE)
        self.text_rect.center = self.screen_rect.center


    def handle_events(self, events):
        running = True
        pressed_keys = pygame.key.get_pressed()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            elif event.type == KEYDOWN:
                #keyname = pygame.key.name(event.key)
                if (event.key == K_RETURN) or (event.key == K_KP_ENTER):
                    if self.namestring != "":
                        score_helper.add_score( self.namestring.strip(), self.misc_dict["score"] )
                        score_helper.save_scores()
                        running = False
                elif event.key == K_BACKSPACE:
                    if len(self.namestring) > 0:
                        self.namestring = self.namestring[:len(self.namestring) - 1]
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
            elif event.type == pygame.TEXTINPUT:
                self.namestring += event.text
        return running

    def write_input_text(self):
        input_back_surf = pygame.Surface(self.text_rect.size)
        input_back_surf.fill(WHITE)
        input_back_surf.set_alpha(255//2)

        text_surface = self.text_input_font.render(self.namestring, True, BLACK, WHITE)
        self.screen.blit(input_back_surf, self.text_rect)
        self.screen.blit(text_surface, self.text_rect)

    def write_label(self):
        label_surface = self.key_prompt_font.render("Congrats, you scored %d pts" % self.misc_dict["score"], True, BLACK, WHITE)
        label_rect = label_surface.get_rect(midbottom = self.text_rect.midtop)

        label_rect.move_ip(0, -1)
        self.screen.blit(label_surface, label_rect)

    def run_loop(self):
        running = True
        pygame.key.set_text_input_rect(self.text_rect)
        pygame.key.start_text_input()

        clock = pygame.time.Clock()


        while running:
            running = self.handle_events( pygame.event.get() )

            self.screen.blit(self.background_surface, (0, 0) )

            self.write_key_prompt("Enter to input your name into high score list")
            self.write_input_text()
            self.write_label()

            pygame.display.flip()

            clock.tick(60)
        pygame.key.stop_text_input()
        return "title", {}
