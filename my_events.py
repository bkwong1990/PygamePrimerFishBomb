import pygame

ADDMISSILE   = pygame.USEREVENT + 1
ADDCLOUD     = pygame.USEREVENT + 2
ADDTANK      = pygame.USEREVENT + 3
ADDLASER     = pygame.USEREVENT + 4
MAKESOUND    = pygame.USEREVENT + 5
ADDEXPLOSION = pygame.USEREVENT + 6
RELOADBOMB   = pygame.USEREVENT + 7
SCOREBONUS   = pygame.USEREVENT + 8
TANKDEATH    = pygame.USEREVENT + 9
NEXTSESSION  = pygame.USEREVENT + 10

'''
A function to simplify the process of posting an explosion event
Parameters:
    rect: the rectangle needed to determine the explosion's size and position
'''
def post_explosion(rect):
    explosion_event = pygame.event.Event(ADDEXPLOSION, rect = rect)
    pygame.event.post(explosion_event)
'''
A function to simplify the process of posting a score bonus event
Parameters:
    enemy_name: the name of the destroyed enemy, which is used to look up their score value
    center: the center of the text showing the score bonus
'''
def post_score_bonus(enemy_name, center):
    score_bonus_event = pygame.event.Event(SCOREBONUS, enemy_name = enemy_name, center = center)
    pygame.event.post(score_bonus_event)
