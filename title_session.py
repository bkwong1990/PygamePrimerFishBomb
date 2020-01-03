import pygame
from sys import (
exit
)
import my_events

from pygame.locals import (
KEYDOWN,
QUIT,
K_SPACE
)



class TitleSession:
    def __init__(self, screen):
        self.screen = screen
        self.background_surface = pygame.image.load("img/title_background.png").convert_alpha()

    def handle_events(self, events):
        running = True
        for event in events:
            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    running = False
        return running

        return running
    def run_loop(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            running = self.handle_events( pygame.event.get() )
            self.screen.blit(self.background_surface, (0, 0) )


            pygame.display.flip()

            clock.tick(60)
