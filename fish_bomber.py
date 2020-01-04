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

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) , flags=pygame.SCALED)

config_dict = {
"missile_maxspeed": 20
}

session_dict = {
"title": title_session.TitleSession,
"battle": battle_session.BattleSession
}

#Set title
pygame.display.set_caption("Fish Bomber Vs Laser Tanks")

#Set volume once
volume = pygame.mixer.music.get_volume() * 0.4
pygame.mixer.music.set_volume(volume)

session_key = "title"
running = True
while running:
    current_session = session_dict[session_key](SCREEN, config_dict)
    session_key = current_session.run_loop()
    if not(session_key):
        running = False

pygame.mixer.quit()
pygame.quit()
print("Ended normally")
