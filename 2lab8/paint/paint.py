import pygame
import sys
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))  # White background

def load_image(path, size=(60, 60)):
    try:
        image = pygame.image.load(path).convert_alpha()
        # Remove white background
        pixel_array = pygame.PixelArray(image)
        pixel_array.replace((255, 255, 255), (0, 0, 0, 0))  # White to transparent
        del pixel_array
        return pygame.transform.scale(image, size)
    except:
        # Placeholder if image fails to load
        placeholder = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (200, 200, 200), (0, 0, *size), 2)
        return placeholder

# Load tool and color icons
tools = {
    'brush': load_image('icons/pencil.png'),
    'eraser': load_image('icons/eraser.png'),
    'rectangle': load_image('icons/rectangle2.png'),
    'circle': load_image('icons/circle1.png')
}

colors = {
    (255, 0, 0): load_image('icons/red.png'),
    (0, 255, 0): load_image('icons/green.png'),
    (0, 0, 255): load_image('icons/blue.png'),
    (0, 0, 0): load_image('icons/black.png')
}

# Tool settings
current_tool = 'brush'
current_color = (0, 0, 0)
BRUSH_SIZE = 10
THICKNESS = 5

# Buttons configuration
tool_buttons = [{'tool': t, 'image': img, 'rect': pygame.Rect(10 + i * 70, 10, 60, 60)}
                for i, (t, img) in enumerate(tools.items())]
color_buttons = [{'color': c, 'image': img, 'rect': pygame.Rect(290 + i * 70, 10, 60, 60)}
                 for i, (c, img) in enumerate(colors.items())]

def draw_brush(pos, prev_pos):
    if prev_pos:
        pygame.draw.line(base_layer, current_color, prev_pos, pos, BRUSH_SIZE * 2)
    pygame.draw.circle(base_layer, current_color, pos, BRUSH_SIZE)

def draw_eraser(pos, prev_pos):
    if prev_pos:
        pygame.draw.line(base_layer, (255, 255, 255), prev_pos, pos, BRUSH_SIZE * 2)
    pygame.draw.circle(base_layer, (255, 255, 255), pos, BRUSH_SIZE)

def draw_shape(start, end, tool, surface):
    if tool == 'rectangle':
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                          abs(end[0] - start[0]), abs(end[1] - start[1]))
        pygame.draw.rect(surface, current_color, rect, THICKNESS)
    elif tool == 'circle':
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        pygame.draw.circle(surface, current_color, start, radius, THICKNESS)

def draw_buttons():
    for button in tool_buttons + color_buttons:
        screen.blit(button['image'], button['rect'])
    # Highlight selected
    for button in tool_buttons:
        if button['tool'] == current_tool:
            pygame.draw.rect(screen, (0, 200, 0), button['rect'], 2)
    for button in color_buttons:
        if button['color'] == current_color:
            pygame.draw.rect(screen, (0, 200, 0), button['rect'], 2)

# Main game state
running = True
drawing = False
start_pos = None
prev_pos = None
clock = pygame.time.Clock()

# Main loop
while running:
    screen.blit(base_layer, (0, 0))  # Draw base layer directly
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_clicked = False
            for button in tool_buttons + color_buttons:
                if button['rect'].collidepoint(mouse_pos):
                    if 'tool' in button:
                        current_tool = button['tool']
                    else:
                        current_color = button['color']
                    button_clicked = True
                    break
            if not button_clicked and mouse_pos[1] > 70:
                drawing = True
                start_pos = mouse_pos
                prev_pos = mouse_pos

        elif event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == 'brush':
                draw_brush(mouse_pos, prev_pos)
                prev_pos = mouse_pos
            elif current_tool == 'eraser':
                draw_eraser(mouse_pos, prev_pos)
                prev_pos = mouse_pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            drawing = False
            if current_tool in ['rectangle', 'circle']:
                draw_shape(start_pos, mouse_pos, current_tool, base_layer)
            start_pos = None
            prev_pos = None

    # Shape preview
    if drawing and current_tool in ['rectangle', 'circle']:
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        draw_shape(start_pos, mouse_pos, current_tool, temp_surface)
        screen.blit(temp_surface, (0, 0))

    draw_buttons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()