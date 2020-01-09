import pygame
import math
from sys import (
exit
)

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
SILVER = (192, 192, 192)
DARK_STEEL = (24,24,24)
WHITE = (255, 255, 255)

KEYPROMPT_FONT_SIZE = 28

'''
Terminates pygame modules and forces the game to quit
'''
def force_quit():
    pygame.mixer.quit()
    pygame.quit()
    print("Force quit")
    exit(0)
# A superclass for all sessions objects representing specific sections of the game
class Session:
    '''
    Creates a new session
    Parameters:
        self: the object being created
        screen: the surface of the gameplay window
        misc_dict: A dictionary with any additional arguments in case the next session needs it
    '''
    def __init__(self, screen, misc_dict):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.misc_dict = misc_dict
        self.key_prompt_font = pygame.font.Font(None, KEYPROMPT_FONT_SIZE )



    '''
    Writes a line of input instructions at the bottom of the screen
    Parameters:
        self: the calling object
        text: the text to be written in the prompt
    '''
    def write_key_prompt(self, text):
        prompt_surface = self.key_prompt_font.render(text, True, BLACK, WHITE)
        prompt_rect = prompt_surface.get_rect(center = (math.floor(self.screen_rect.width * 0.5), math.floor(self.screen_rect.height * 0.97)) )

        self.screen.blit(prompt_surface, prompt_rect)
