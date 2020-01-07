import pygame

pygame.mixer.init()
pygame.init()

SOUND_DICT = {
# http://soundbible.com/1986-Bomb-Exploding.html
"explosion": pygame.mixer.Sound("media/explosion.ogg"),
# http://soundbible.com/1771-Laser-Cannon.html
"laser": pygame.mixer.Sound("media/Laser.ogg"),
# voiced by Bradley Wong
"reloaded": pygame.mixer.Sound("media/reloaded.ogg"),
# Recorded the sound of a Kailh Navy switch
"tactile_click": pygame.mixer.Sound("media/kailh_navy.ogg")
}

current_filename = ""

def play_clip(key):
    SOUND_DICT[key].play()



def set_volume(multiplier):
    #Set volume once
    volume = pygame.mixer.music.get_volume() * multiplier
    pygame.mixer.music.set_volume(volume)

def load_music_file(filename):
    global current_filename
    if current_filename != filename:
        pygame.mixer.music.stop()
        if filename != "":
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=-1)
            current_filename = filename
