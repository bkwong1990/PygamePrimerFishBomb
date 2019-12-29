import pygame

ADDMISSILE   = pygame.USEREVENT + 1
ADDCLOUD     = pygame.USEREVENT + 2
ADDTANK      = pygame.USEREVENT + 3
ADDLASER     = pygame.USEREVENT + 4
MAKESOUND    = pygame.USEREVENT + 5
ADDEXPLOSION = pygame.USEREVENT + 6
RELOADBOMB   = pygame.USEREVENT + 7
SCOREBONUS   = pygame.USEREVENT + 8

def post_explosion(rect):
    explosion_event = pygame.event.Event(ADDEXPLOSION, rect = rect)
    pygame.event.post(explosion_event)

def post_score_bonus(score, rect):
    score_bonus_event = pygame.event.Event(SCOREBONUS, score = score, rect = rect)
    pygame.event.post(score_bonus_event)
