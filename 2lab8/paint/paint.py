import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Create main screen and drawing layer
screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))  # White background

def load_image(path, size=(60, 60)):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except:
        # Create placeholder if image fails to load
        placeholder = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (200, 200, 200), (0, 0, *size), 2)
        return placeholder

# Load tool icons
brush_image = load_image('icons/pencil.png')
eraser_image = load_image('icons/eraser.png')
rectangle_image = load_image('icons/rectangle1.png')
circle_image = load_image('icons/circle1.png')

# Load color icons
red_image = load_image('icons/red.png')
green_image = load_image('icons/green.png')
blue_image = load_image('icons/blue.png')
black_image = load_image('icons/black.png')

# Tool settings
current_tool = 'brush'
current_color = (0, 0, 0)  
BRUSH_SIZE = 10  
THICKNESS = 5   

# Tool buttons configuration
tool_buttons = [
    {"tool": "brush", "image": brush_image, "rect": pygame.Rect(10, 10, 60, 60)},
    {"tool": "eraser", "image": eraser_image, "rect": pygame.Rect(80, 10, 60, 60)},
    {"tool": "rectangle", "image": rectangle_image, "rect": pygame.Rect(150, 10, 60, 60)},
    {"tool": "circle", "image": circle_image, "rect": pygame.Rect(220, 10, 60, 60)},
]

# Color buttons configuration
color_buttons = [
    {"color": (255, 0, 0), "image": red_image, "rect": pygame.Rect(300, 10, 60, 60)},
    {"color": (0, 255, 0), "image": green_image, "rect": pygame.Rect(370, 10, 60, 60)},
    {"color": (0, 0, 255), "image": blue_image, "rect": pygame.Rect(440, 10, 60, 60)},
    {"color": (0, 0, 0), "image": black_image, "rect": pygame.Rect(510, 10, 60, 60)},
]

def draw_brush(pos, prev_pos):
    if prev_pos:
        # Draw line between current and previous position
        pygame.draw.line(base_layer, current_color, prev_pos, pos, BRUSH_SIZE * 2)
    # Draw circle at current position
    pygame.draw.circle(base_layer, current_color, pos, BRUSH_SIZE)

def draw_eraser(pos, prev_pos):
    if prev_pos:
        # Calculate rectangle between current and previous position
        rect = pygame.Rect(
            min(prev_pos[0], pos[0]),
            min(prev_pos[1], pos[1]),
            abs(pos[0] - prev_pos[0]),
            abs(pos[1] - prev_pos[1])
        )
        pygame.draw.rect(base_layer, (255, 255, 255), rect)

def draw_preview():
    if drawing and current_pos and start_pos:
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        if current_tool == 'rectangle':
            rect = pygame.Rect(
                min(start_pos[0], current_pos[0]),
                min(start_pos[1], current_pos[1]),
                abs(current_pos[0] - start_pos[0]),
                abs(current_pos[1] - start_pos[1])
            )
            pygame.draw.rect(temp_surface, current_color, rect, THICKNESS)
        elif current_tool == 'circle':
            radius = int(math.hypot(current_pos[0] - start_pos[0], 
                                 current_pos[1] - start_pos[1]))
            pygame.draw.circle(temp_surface, current_color, start_pos, radius, THICKNESS)
        
        screen.blit(base_layer, (0, 0))
        screen.blit(temp_surface, (0, 0))
        draw_buttons()

def draw_buttons():
    """Draw all interface buttons"""
    for button in tool_buttons + color_buttons:
        screen.blit(button['image'], button['rect'])
    
    # Highlight selected tool
    for button in tool_buttons:
        if button['tool'] == current_tool:
            pygame.draw.rect(screen, (0, 200, 0), button['rect'], 2)
    
    # Highlight selected color
    for button in color_buttons:
        if button['color'] == current_color:
            pygame.draw.rect(screen, (0, 200, 0), button['rect'], 2)

# Main game state
running = True
drawing = False
start_pos = None
current_pos = None
prev_pos = None

# Initial render
screen.fill((255, 255, 255))
draw_buttons()
pygame.display.flip()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = event.pos
                
                # Check tool buttons
                button_clicked = False
                for button in tool_buttons + color_buttons:
                    if button['rect'].collidepoint(pos):
                        if 'tool' in button:
                            current_tool = button['tool']
                        else:
                            current_color = button['color']
                        button_clicked = True
                        break
                
                # Start drawing if clicked on canvas
                if not button_clicked and pos[1] > 80:  # Ignore toolbar
                    drawing = True
                    start_pos = pos
                    current_pos = pos
                    prev_pos = pos
        
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos
                
                # Real-time drawing for brush and eraser
                if current_tool == 'brush':
                    draw_brush(current_pos, prev_pos)
                    prev_pos = current_pos
                elif current_tool == 'eraser':
                    draw_eraser(current_pos, prev_pos)
                    prev_pos = current_pos
                
                # Preview for shapes
                if current_tool in ['rectangle', 'circle']:
                    draw_preview()
                else:
                    screen.blit(base_layer, (0, 0))
                    draw_buttons()
                
                pygame.display.flip()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                
                # Finalize shapes
                if current_tool in ['rectangle', 'circle']:
                    temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    
                    if current_tool == 'rectangle':
                        rect = pygame.Rect(
                            min(start_pos[0], current_pos[0]),
                            min(start_pos[1], current_pos[1]),
                            abs(current_pos[0] - start_pos[0]),
                            abs(current_pos[1] - start_pos[1])
                        )
                        pygame.draw.rect(temp_surface, current_color, rect, THICKNESS)
                    elif current_tool == 'circle':
                        radius = int(math.hypot(current_pos[0] - start_pos[0], 
                                     current_pos[1] - start_pos[1]))
                        pygame.draw.circle(temp_surface, current_color, start_pos, radius, THICKNESS)
                    
                    base_layer.blit(temp_surface, (0, 0))
                
                # Update display
                screen.blit(base_layer, (0, 0))
                draw_buttons()
                pygame.display.flip()
                
                # Reset positions
                start_pos = None
                current_pos = None
                prev_pos = None
    
    # Cap at 60 FPS
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()