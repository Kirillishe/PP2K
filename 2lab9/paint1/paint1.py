import pygame
import sys
import math
import os


pygame.init()

WIDTH, HEIGHT = 800, 600

# Create main screen and drawing layer
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))  # White background

def load_image(path, size=(60, 60)):
   
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except:
        placeholder = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (200, 200, 200, 128), (0, 0, *size), 2)
        
        font = pygame.font.SysFont('Arial', 12)
        text = font.render(os.path.basename(path).split('.')[0][:5], True, (0, 0, 0))
        text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
        placeholder.blit(text, text_rect)
        
        return placeholder

icons = {
    'brush': 'icons/pencil.png',
    'eraser': 'icons/eraser.png',
    'rectangle': 'icons/rectangle1.png',
    'square': 'icons/square.png',
    'circle': 'icons/circle1.png',
    'right_triangle': 'icons/right_triangle.png',
    'equilateral_triangle': 'icons/equilateral_triangle.png',
    'rhombus': 'icons/rhombus.png'
}

# Load all tool icons
tool_images = {name: load_image(path) for name, path in icons.items()}

# Color palette
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (255, 165, 0), (128, 0, 128), (255, 192, 203)
]

# Tool settings
current_tool = 'brush'
current_color = (0, 0, 0)
brush_size = 10
thickness = 5

# Tool buttons configuration
tool_buttons = []
for i, (tool, image) in enumerate(tool_images.items()):
    tool_buttons.append({
        "tool": tool,
        "image": image,
        "rect": pygame.Rect(10 + i * 70, 10, 60, 60)
    })

# Color buttons configuration
color_buttons = []
for i, color in enumerate(colors):
    color_buttons.append({
        "color": color,
        "rect": pygame.Rect(10 + i * 70, 80, 60, 30)  # Smaller color buttons
    })

def draw_brush(pos, prev_pos):
    """Draw with brush tool"""
    if prev_pos:
        pygame.draw.line(base_layer, current_color, prev_pos, pos, brush_size * 2)
    pygame.draw.circle(base_layer, current_color, pos, brush_size)

def draw_eraser(pos, prev_pos):
    """Erase by drawing white"""
    if prev_pos:
        pygame.draw.line(base_layer, (255, 255, 255), prev_pos, pos, brush_size * 2)
    pygame.draw.circle(base_layer, (255, 255, 255), pos, brush_size)

def draw_shape(start, end, shape_type):
    """Draw various shapes"""
    temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    if shape_type == 'rectangle':
        rect = pygame.Rect(
            min(start[0], end[0]),
            min(start[1], end[1]),
            abs(end[0] - start[0]),
            abs(end[1] - start[1])
        )
        pygame.draw.rect(temp_surface, current_color, rect, thickness)
    
    elif shape_type == 'square':
        size = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
        rect = pygame.Rect(
            min(start[0], end[0]),
            min(start[1], end[1]),
            size, size
        )
        pygame.draw.rect(temp_surface, current_color, rect, thickness)
    
    elif shape_type == 'circle':
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        pygame.draw.circle(temp_surface, current_color, start, radius, thickness)
    
    elif shape_type == 'right_triangle':
        points = [(start[0], start[1]), (start[0], end[1]), (end[0], end[1])]
        pygame.draw.polygon(temp_surface, current_color, points, thickness)
    
    elif shape_type == 'equilateral_triangle':
        height = end[1] - start[1]
        side_length = abs(end[0] - start[0])
        points = [
            (start[0] + side_length // 2, start[1]),
            (start[0], end[1]),
            (end[0], end[1])
        ]
        pygame.draw.polygon(temp_surface, current_color, points, thickness)
    
    elif shape_type == 'rhombus':
        center_x = (start[0] + end[0]) // 2
        center_y = (start[1] + end[1]) // 2
        width = abs(end[0] - start[0]) // 2
        height = abs(end[1] - start[1]) // 2
        
        points = [
            (center_x, center_y - height),
            (center_x + width, center_y),
            (center_x, center_y + height),
            (center_x - width, center_y)
        ]
        pygame.draw.polygon(temp_surface, current_color, points, thickness)
    
    return temp_surface

def draw_buttons():
    """Draw all interface buttons"""
    # Draw color buttons
    for button in color_buttons:
        pygame.draw.rect(screen, button['color'], button['rect'])
    
    # Draw tool buttons
    for button in tool_buttons:
        screen.blit(button['image'], button['rect'])
    
    # Highlight selected tool
    for button in tool_buttons:
        if button['tool'] == current_tool:
            pygame.draw.rect(screen, (0, 200, 0), button['rect'], 3)
    
    # Highlight selected color
    for button in color_buttons:
        if button['color'] == current_color:
            pygame.draw.rect(screen, (0, 200, 0), button['rect'], 3)

# Main game state
running = True
drawing = False
start_pos = None
prev_pos = None
clock = pygame.time.Clock()

# Main game loop
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check buttons
                button_clicked = False
                for button in tool_buttons + color_buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        if 'tool' in button:
                            current_tool = button['tool']
                        else:
                            current_color = button['color']
                        button_clicked = True
                        break
                
                # Start drawing if clicked on canvas
                if not button_clicked and mouse_pos[1] > 120:
                    drawing = True
                    start_pos = mouse_pos
                    prev_pos = mouse_pos
        
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                # For brush and eraser
                if current_tool == 'brush':
                    draw_brush(mouse_pos, prev_pos)
                    prev_pos = mouse_pos
                elif current_tool == 'eraser':
                    draw_eraser(mouse_pos, prev_pos)
                    prev_pos = mouse_pos
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                
                # Finalize shapes
                if current_tool not in ['brush', 'eraser']:
                    shape_surface = draw_shape(start_pos, mouse_pos, current_tool)
                    base_layer.blit(shape_surface, (0, 0))
                
                start_pos = None
                prev_pos = None
    
    # Drawing
    screen.fill((255, 255, 255))
    screen.blit(base_layer, (0, 0))
    
    # Show preview for shapes
    if drawing and current_tool not in ['brush', 'eraser']:
        preview_surface = draw_shape(start_pos, mouse_pos, current_tool)
        screen.blit(preview_surface, (0, 0))
    
    draw_buttons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

