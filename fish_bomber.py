import pygame
import math
import battle_session
import title_session
import config_session
import input_score_session
import view_scores_session
import config_helper
import sound_helper
import score_helper

#initialize mixer and pygame, init functions can be called multiple times safely
pygame.mixer.init()
pygame.init()
# 1280x720
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Create screen object

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) , flags=pygame.SCALED)



session_dict = {
"title": title_session.TitleSession,
"battle": battle_session.BattleSession,
"config": config_session.ConfigSession,
"input_score": input_score_session.InputScoreSession,
"view_scores": view_scores_session.ViewScoresSession
}

config_helper.load_config_info()

if config_helper.config_info["fullscreen"]:
    pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) , flags=pygame.SCALED|pygame.FULLSCREEN)

#Set title
pygame.display.set_caption("Fish Bomber Vs Laser Tanks")

sound_helper.set_volume(0.45)

score_helper.load_scores()

session_key = "title"
misc_dict = {}
running = True
while running:
    current_session = session_dict[session_key](SCREEN, misc_dict)
    session_key, misc_dict = current_session.run_loop()
    if not(session_key):
        running = False

pygame.mixer.quit()
pygame.quit()
print("Ended normally")
