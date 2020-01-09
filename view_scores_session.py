import pygame

from sys import (
exit
)
import math

import my_events
import session
import score_helper
import sound_helper
import my_menu

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE,
K_ESCAPE
)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
SILVER = (192, 192, 192)
DARK_STEEL = (24,24,24)

BGM_PATH = "media/sorato.ogg"

SCORE_FONT_SIZE = 50
KEYPROMPT_FONT_SIZE = 28

SHADOW_OFFSET = 3

class ViewScoresSession(session.Session):
    def __init__(self, screen, misc_dict):
        super(ViewScoresSession, self).__init__(screen, misc_dict)
        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE )

        self.next_session_key = "title"
        # https://www.pexels.com/photo/advertisements-batch-blur-business-518543/
        self.background_surface = self.background_surface = pygame.image.load("img/newspaper.png").convert_alpha()
        menu_midtop = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.3))

        self.score_menu = my_menu.VerticalMenu(self.score_font, BLUE, BLACK, RED, WHITE, menu_midtop)
        def on_score_entry(key):
            if key == K_SPACE:
                sound_helper.play_clip("ovation")

        for i in range(0, len(score_helper.scores) ):
            name = score_helper.scores[i]["name"]
            score = score_helper.scores[i]["score"]
            line = "%d %s %d" % ( (i + 1) , name, score)
            self.score_menu.add(line, on_score_entry)
        def on_return(key):
            if key == K_SPACE:
                pygame.event.post( pygame.event.Event( my_events.NEXTSESSION ) )
        self.score_menu.add("Return", on_return)

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
                    pygame.event.post(pygame.event.Event(QUIT))
                else:
                    self.score_menu.process_input(event.key)
        return running

    def run_loop(self):
        sound_helper.load_music_file(BGM_PATH)
        running = True
        clock = pygame.time.Clock()
        while running:
            running = self.handle_events( pygame.event.get() )
            self.screen.blit(self.background_surface, (0, 0) )
            #self.menu.init_surf_rect_list()
            self.score_menu.draw(self.screen)

            self.write_key_prompt("Space to confirm selection. Confirm a score to hear the Republic's gratitude.")

            pygame.display.flip()

            clock.tick(60)
        return self.next_session_key, {}
