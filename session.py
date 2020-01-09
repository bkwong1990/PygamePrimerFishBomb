import pygame
import math

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
SILVER = (192, 192, 192)
DARK_STEEL = (24,24,24)
WHITE = (255, 255, 255)

KEYPROMPT_FONT_SIZE = 28

class Session:
    def __init__(self, screen, misc_dict):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.misc_dict = misc_dict
        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )

    def write_key_prompt(self, text):
        prompt_surface = self.key_prompt_font.render(text, True, BLACK, WHITE)
        prompt_rect = prompt_surface.get_rect(center = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.97)) )

        self.screen.blit(prompt_surface, prompt_rect)
