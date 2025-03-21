import pygame

pygame.init()
size = pygame.Vector2(800, 800)
pos = [size.x/2, size.y/2]
radius = 25
screen = pygame.display.set_mode((size.x, size.y))
flak = True
clock = pygame.time.Clock()
speed = 20

while flak:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flak = False
    screen.fill((255, 255, 255))

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and pos[1]-speed >= radius: pos[1] -= speed
    if pressed[pygame.K_DOWN] and pos[1]+speed <= size.y-radius: pos[1] += speed
    if pressed[pygame.K_LEFT] and pos[0]-speed >= radius: pos[0] -= speed
    if pressed[pygame.K_RIGHT] and pos[0]+speed <= size.x-radius: pos[0] += speed

    pygame.draw.circle(screen, 'red', pos, radius)

    pygame.display.flip()
    clock.tick(60)