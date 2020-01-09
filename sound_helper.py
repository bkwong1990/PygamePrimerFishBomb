import pygame

pygame.mixer.init()
pygame.init()

SOUND_DICT = {
# http://soundbible.com/1986-Bomb-Exploding.html by Sound Explorer
"explosion": pygame.mixer.Sound("media/explosion.ogg"),
# http://soundbible.com/1771-Laser-Cannon.html by Mike Koenig
"laser": pygame.mixer.Sound("media/Laser.ogg"),
# voiced by Bradley Wong
"reloaded": pygame.mixer.Sound("media/reloaded.ogg"),
# Recorded the sound of a Kailh Navy switch by Bradley Wong
"tactile_click": pygame.mixer.Sound("media/kailh_navy.ogg"),
# http://soundbible.com/1647-Ovation.html by Mike Koenig
"ovation": pygame.mixer.Sound("media/ovation.ogg")
}

current_filename = ""

'''
Plays one of the clips in the dictionary
Parameters:
    key: the string key indicating which clip should be played
'''
def play_clip(key):
    SOUND_DICT[key].play()


'''
Sets volume of game BGM
Parameters:
    multiplier: the value by which to multiply the current volume
'''
def set_volume(multiplier):
    #Set volume once
    volume = pygame.mixer.music.get_volume() * multiplier
    pygame.mixer.music.set_volume(volume)

'''
Loads a BGM file and sets it to loop indefinitely. If the file is already being
played, do nothing.
Parameters:
    filename: the name of the music file to be played
'''
def load_music_file(filename):
    global current_filename
    if current_filename != filename:
        pygame.mixer.music.stop()
        if filename != "":
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=-1)
            current_filename = filename
