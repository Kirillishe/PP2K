import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 25
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Load custom graphics
try:
    background = pygame.image.load('sources/background.png').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    head_img = pygame.image.load('sources/snake_head.png').convert_alpha()
    head_img = pygame.transform.scale(head_img, (CELL_SIZE, CELL_SIZE))
    
    body_img = pygame.image.load('sources/snake_body.png').convert_alpha()
    body_img = pygame.transform.scale(body_img, (CELL_SIZE, CELL_SIZE))
    
    # Different food images for different weights (or we'll color them differently)
    food_img = pygame.image.load('sources/food.png').convert_alpha()
    food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))
    
except pygame.error as e:
    print(f"Error loading images: {e}")
    background = None
    head_img = None
    body_img = None
    food_img = None

# Game variables
snake_pos = [WIDTH//2, HEIGHT//2]
snake_body = [
    [WIDTH//2, HEIGHT//2],
    [WIDTH//2 - CELL_SIZE, HEIGHT//2],
    [WIDTH//2 - (2 * CELL_SIZE), HEIGHT//2]
]
direction = 'RIGHT'
change_to = direction
SPEED = 9
score = 0
level = 1
food_pos = [0, 0]
food_spawn = False
growing = False

# New food variables
food_weight = 1  # Standard food weight
food_colors = [RED, BLUE, GOLD]  # Different colors for different weights
food_timer = 0  # Timer for food expiration
FOOD_LIFETIME = 10  # Food disappears after 10 seconds

# Game clock
clock = pygame.time.Clock()

# Font for score display
font = pygame.font.SysFont('arial', 20)

def spawn_food():
    global food_pos, food_spawn, food_weight, food_timer
    while True:
        food_pos = [
            random.randint(0, WIDTH // CELL_SIZE -1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE -1) * CELL_SIZE
        ]
        if food_pos not in snake_body:
            food_spawn = True
            # Randomly assign weight (1-3) to food
            food_weight = random.randint(1, 3)
            # Reset timer when new food spawns
            food_timer = time.time()
            break

def check_collision():
    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or 
        snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
        return True
    for block in snake_body[1:]:
        if snake_pos == block:
            return True
    return False

def check_food_collision():
    global score, level, SPEED, growing
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        # Increase score based on food weight
        score += food_weight
        growing = True  
        if score % 3 == 0:  
            level += 1
            SPEED += 2
        return True
    return False

def show_game_over():
    screen.fill(BLACK)
    game_over_font = pygame.font.SysFont('arial', 30)
    game_over_surface = game_over_font.render('GAME OVER!', True, RED)
    score_surface = font.render(f'Final Score: {score}', True, WHITE)
    level_surface = font.render(f'Final Level: {level}', True, WHITE)
    
    screen.blit(game_over_surface, (WIDTH//2 - 100, HEIGHT//2 - 60))
    screen.blit(score_surface, (WIDTH//2 - 70, HEIGHT//2))
    screen.blit(level_surface, (WIDTH//2 - 70, HEIGHT//2 + 30))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def update_score():
    score_surface = font.render(f'Score: {score}', True, WHITE)
    level_surface = font.render(f'Level: {level}', True, WHITE)
    speed_surface = font.render(f'Speed: {SPEED}', True, WHITE)
    
    screen.blit(score_surface, (10, 10))
    screen.blit(level_surface, (10, 40))
    screen.blit(speed_surface, (10, 70))

def draw_snake():
    for i, pos in enumerate(snake_body):
        if i == 0:
            if head_img:
                screen.blit(head_img, (pos[0], pos[1]))
            else:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        else:
            if body_img:
                screen.blit(body_img, (pos[0], pos[1]))
            else:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_food():
    # Check if food has expired
    if time.time() - food_timer > FOOD_LIFETIME:
        spawn_food()  # Respawn new food if current one expired
    
    # Draw food with different colors based on weight
    if food_img:
        # Create a colored version of the food image
        colored_food = food_img.copy()
        colored_food.fill(food_colors[food_weight-1], special_flags=pygame.BLEND_MULT)
        screen.blit(colored_food, (food_pos[0], food_pos[1]))
    else:
        pygame.draw.rect(screen, food_colors[food_weight-1], pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
    
    # Draw timer bar above food
    time_left = max(0, FOOD_LIFETIME - (time.time() - food_timer))
    timer_width = (time_left / FOOD_LIFETIME) * CELL_SIZE
    pygame.draw.rect(screen, WHITE, (food_pos[0], food_pos[1] - 5, CELL_SIZE, 3))
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1] - 5, timer_width, 3))

# Initial food spawn
spawn_food()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
    
    direction = change_to
    if direction == 'UP':
        snake_pos[1] -= CELL_SIZE
    elif direction == 'DOWN':
        snake_pos[1] += CELL_SIZE
    elif direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE
    elif direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE
    
    snake_body.insert(0, list(snake_pos))
    if not growing:
        snake_body.pop()
    else:
        growing = False  
    
    if check_food_collision():
        spawn_food()
    
    if check_collision():
        show_game_over()
    
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLACK)
    
    draw_snake()
    draw_food()
    update_score()
    
    pygame.display.flip()
    clock.tick(SPEED)

pygame.quit()
sys.exit()