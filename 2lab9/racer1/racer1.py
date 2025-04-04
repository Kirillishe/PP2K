import pygame, sys, math
from pygame.locals import *
import random, time

pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 255, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
SPEED_INC_COINS = 5  # Number of coins needed to increase speed

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("source/AnimatedStree.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("source/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom - self.rect.height> 600):
            SCORE += 1
            self.rect.top = 0 - self.rect.height
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("source/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.current_coins = 0  # Track coins collected since last speed increase
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create coins with different weights (sizes)
        self.weights = {}
        self.weight = 1  # Default weight
        # Create 3 different coin sizes with different weights
        for i in range(3):
            self.weights[i] = pygame.transform.scale_by(pygame.image.load("source/coin.png"), 0.025 + 0.01*i)
        self.respawn()  # Initialize with random weight
    
    def move(self):
        self.rect.move_ip(0,SPEED/1.5)
        if (self.rect.bottom - self.rect.height> 600):
            self.respawn()

    def respawn(self):
        # Randomly select weight (1-3) and corresponding image
        self.weight = random.randint(1, 3)
        self.image = self.weights[self.weight-1]
        self.rect = self.image.get_rect()
        self.rect.top = 0 - self.rect.height
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED == math.log(SPEED*SPEED + 2)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    text_coins = font_small.render(str(COINS), True, GOLD)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(text_coins, (SCREEN_WIDTH-28, 10))  # Adjusted position

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound("source/crash.wav").play()
          time.sleep(1)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()

    #Collision between Player and Coin
    if pygame.sprite.spritecollideany(P1, coins):
        pygame.mixer.Sound("source/retro-coin.mp3").play()
        for coin in coins:
            COINS += coin.weight  # Add coin's weight to total coins
            P1.current_coins += coin.weight  # Add to current coin counter
            
            # Increase speed if enough coins collected
            if P1.current_coins >= SPEED_INC_COINS:
                P1.current_coins = 0  # Reset counter
                SPEED += 1  # Increase game speed
            
            coin.respawn()  # Respawn coin with new random weight
        
    pygame.display.update()
    FramePerSec.tick(FPS)