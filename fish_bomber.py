import pygame
import math
import battle_session
import title_session

#initialize mixer and pygame, init functions can be called multiple times safely
pygame.mixer.init()
pygame.init()
# 1280x720
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Create screen object

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

config_dict = {
"missile_maxspeed": 20
}

#Set title
pygame.display.set_caption("Fish Bomber Vs Laser Tanks")

running = True
while running:
    session = title_session.TitleSession(SCREEN)
    session.run_loop()

    session = battle_session.BattleSession(SCREEN, config_dict)
    session.run_loop()

pygame.mixer.quit()
