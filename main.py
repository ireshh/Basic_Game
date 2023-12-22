# Complete your game here
"""
Nyxclipse

You find yourself running from a relentless monster lurking in the night.
How did you get here? No Idea, but you are here now in this dimension where you can jump boundaries to the other side.
Your need to collect all your coins scattered across this dimension and run as fast as you can to the door to stay alive.
However, reaching the door is no easy task and you can only unlock it when you collect all the coins. Beware, as the monster is hot on your heels,
and if it catches you, it's GAME OVER...

Use the arrow keys to control the player.
"""

import pygame
import sys
import random

pygame.init()

display_width, display_height = 800, 800
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Nyxclipse")

black = (0, 0, 0)
red = (255, 0, 0)

monster_img = pygame.image.load("monster.png")
robot_img = pygame.image.load("robot.png")
coin_img = pygame.image.load("coin.png")
try:
    door1_img = pygame.image.load("door1.png")
    door2_img = pygame.image.load("door2.png")
except FileNotFoundError:
    door1_img = pygame.image.load("door.png")
    door2_img = pygame.image.load("door.png")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = robot_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = monster_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = door1_img
        self.rect = self.image.get_rect(topleft=(x, y))

all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = Player(50, 50)
monster = Monster(700, 700)
door = Door(700, 50)
all_sprites.add(player, monster, door)

def create_coins():
    for _ in range(10):
        coin = Coin(random.randint(100, 700), random.randint(100, 700))
        coins.add(coin)
        all_sprites.add(coin)

create_coins()

score = 0
high_score = 0
clock = pygame.time.Clock()
game_over = False
monster_speed = 3
speed_up_mons = 1.20


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_SPACE:
                player.rect.topleft = (50, 50)
                monster.rect.topleft = (700, 700)
                create_coins()
                door.rect.topleft = (random.randint(100, 700), random.randint(100, 700))
                score = 0

    keys = pygame.key.get_pressed()
    player.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
    player.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

    if player.rect.x > display_width:
        player.rect.x = 0
    elif player.rect.x < 0:
        player.rect.x = display_width

    if player.rect.y > display_height:
        player.rect.y = 0
    elif player.rect.y < 0:
        player.rect.y = display_height

    monster_speed = min(monster_speed, 10)
    if player.rect.x < monster.rect.x:
        monster.rect.x -= monster_speed
    elif player.rect.x > monster.rect.x:
        monster.rect.x += monster_speed
    if player.rect.y < monster.rect.y:
        monster.rect.y -= monster_speed
    elif player.rect.y > monster.rect.y:
        monster.rect.y += monster_speed

    coin_collisions = pygame.sprite.spritecollide(player, coins, True)
    if coin_collisions:
        score += 1

    if len(coins) == 0:
        door.image = door2_img
        if pygame.sprite.collide_rect(player, door):
            score += 5
            monster_speed *= speed_up_mons
            create_coins()
            door.rect.topleft = (random.randint(100, 700), random.randint(100, 700))
            door.image = door1_img


    if pygame.sprite.collide_rect(player, monster):
        if score > high_score:
            high_score = score
        player.rect.topleft = (50, 50)
        monster.rect.topleft = (700, 700)
        score = 0

    display.fill(black)
    all_sprites.draw(display)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, red)
    display.blit(score_text, (10, 10))

    high_score_text = font.render(f"High Score: {high_score}", True, red)
    display.blit(high_score_text, (10, 50))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
