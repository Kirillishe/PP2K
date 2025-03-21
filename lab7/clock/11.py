import pygame
import os
import datetime

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

def Rotate(image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    return rotated_image, new_rect

pygame.init()
size = pygame.Vector2(800, 600)
screen = pygame.display.set_mode((size.x, size.y))
flak = True
clock = pygame.time.Clock()

while flak:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        flak = False

        watch = get_image("/Users/kirillchumikov/Desktop/lab7/clock.png")
        h_arrow = get_image("/Users/kirillchumikov/Desktop/lab7/min_hand.png")
        m_arrow = get_image("/Users/kirillchumikov/Desktop/lab7/sec_hand.png")
        time = datetime.datetime.now()
        h_angle = time.hour * 30
        m_angle = time.minute * 6

        h_arrow, h_rect = Rotate(h_arrow, (100, 0), -60 - h_angle)
        m_arrow, m_rect = Rotate(m_arrow, (100, 0), 60 - m_angle)

        screen.blit(watch, (0, 0))
        screen.blit(m_arrow, m_rect)
        screen.blit(h_arrow, h_rect)

        pygame.display.flip()
        clock.tick(60)