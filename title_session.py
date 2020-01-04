import pygame
from sys import (
exit
)
import math
import my_events
import session
import my_sprites
import my_menu

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE
)

MENU_FONT_SIZE = 80
KEYPROMPT_FONT_SIZE = 28

RED = (255, 0, 0)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)
DARK_STEEL = (24,24,24)



class TitleSession(session.Session):
    def __init__(self, screen, config_dict):
        super(TitleSession, self).__init__(screen, config_dict)
        self.background_surface = pygame.image.load("img/title_background.png").convert_alpha()
        self.next_session_key = "battle"
        menu_midtop = (math.floor(self.screen_rect.width * 0.7), math.floor(self.screen_rect.height * 0.3))

        self.font = pygame.font.Font(None, MENU_FONT_SIZE )
        self.shadow_font = pygame.font.Font(None, MENU_FONT_SIZE)

        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )

        self.menu = my_menu.BaseMenu(self.font, RED, self.shadow_font, BLACK, DARK_STEEL, SILVER, menu_midtop)

        def on_battle_item(key):
            if key == K_SPACE:
                self.next_session_key = "battle"
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )

        self.menu.add("To Battle", on_battle_item)

        def on_quit_item(key):
            if key == K_SPACE:
                self.next_session_key = None
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )

        self.menu.add("Soft Quit", on_quit_item)


    def write_key_prompt(self):
        text_surface = self.key_prompt_font.render("Space to confirm, arrow keys to change menu selection", True, BLACK)
        text_rect = text_surface.get_rect(center = (math.floor(self.screen_rect.width * 0.7), math.floor(self.screen_rect.height * 0.97)) )
        self.screen.blit(text_surface, text_rect)


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


    def run_loop(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            running = self.handle_events( pygame.event.get() )
            self.screen.blit(self.background_surface, (0, 0) )
            self.menu.init_draw_list()
            self.menu.draw(self.screen)

            self.write_key_prompt()

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key
