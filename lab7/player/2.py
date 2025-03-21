import pygame
import os
from tinytag import TinyTag

path = r"/Users/kirillchumikov/Desktop/lab7/player/songs"

_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    return sound

pygame.init()
size = pygame.Vector2(800, 600)
screen = pygame.display.set_mode((size.x, size.y))
flak = True
clock = pygame.time.Clock()

font = pygame.font.Font(None, 72)
song_index = 0

for element in os.listdir(path):
        play_sound(path+r'//'+element)
list(_sound_library.values())[song_index].play()
is_paused = False

while flak:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flak = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if is_paused: 
                pygame.mixer.unpause()
                is_paused = False
            else: 
                pygame.mixer.pause()
                is_paused = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            song_index = (song_index+1)%(len(_sound_library))
            pygame.mixer.fadeout(300)
            list(_sound_library.values())[song_index].play()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            song_index = (song_index-1)%(len(_sound_library))
            pygame.mixer.fadeout(300)
            list(_sound_library.values())[song_index].play()

    screen.fill((255, 255, 255))

    tag = TinyTag.get(list(_sound_library.keys())[song_index])
    title = font.render(tag.title, True, (0, 0, 0))
    artist = font.render(tag.artist, True, (0, 0, 0))

    screen.blit(title, (size.x/2 - title.get_width() // 2, size.y/2 - title.get_height() // 2 - 50))
    screen.blit(artist, (size.x/2 - artist.get_width() // 2, size.y/2 - artist.get_height() // 2 + 50))

    pygame.display.flip()
    clock.tick(60)