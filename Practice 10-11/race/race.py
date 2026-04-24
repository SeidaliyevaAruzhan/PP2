import pygame
import sys
from pygame.locals import *
import random, time

size = w, h = 400, 600
speed = 5
score = 0
coin1 = 0
coinnum = 0
pygame.init()
screen = pygame.display.set_mode((size))
clock = pygame.time.Clock()

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

screen.fill(white)

font = pygame.font.SysFont('Verdana', 60)
font_small = pygame.font.SysFont('Verdana', 20)
game_over = font.render('Game Over', True, black)

backround = pygame.image.load("images/street.png")

pygame.display.set_caption('Game')


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, w - 40), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > 600:
            score += 1
            self.rect.bottom = 0
            self.rect.center = (random.randint(40, w - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed[pygame.K_UP]:
                self.rect.move_ip(0, -5)

        if self.rect.bottom < 600:
            if pressed[pygame.K_DOWN]:
                self.rect.move_ip(0, 5)

        if self.rect.left > 0:
            if pressed[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < w:
            if pressed[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self, size1, size2):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/coin.jpeg'), (size1, size2))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, w - 40), 0)

    def move(self):
        global coin
        self.rect.move_ip(0, 5)
        if self.rect.top > 600:
            self.rect.bottom = 0
            self.rect.center = (random.randint(40, w - 40), 0)

P1 = Player()
E1 = Enemy()
C1 = Coin(15, 15)
C2 = Coin(25, 25)
C3 = Coin(35, 35)

enemies = pygame.sprite.Group(E1)

coins = pygame.sprite.Group(C1, C2, C3)

all_sprites = pygame.sprite.Group(P1, E1, C1, C2, C3)

#timer for increase speed
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

while True:

    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 0.1

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(backround, (0, 0))

    #score
    scores = font_small.render('car:' + str(score), True, black)
    coinsc = font_small.render('coin:' + str(coin1), True, black)
    screen.blit(scores, (10, 10))
    screen.blit(coinsc, (w - scores.get_width() - 30, 10))

    if pygame.sprite.spritecollideany(P1, coins):
        coin1 += 1
        coinnum += 1
        pygame.mixer.Sound('sounds/coinsound.mp3').play()
        C1.rect.center = (random.randint(40, w - 40), 0)
        if coinnum % 4 == 0 and coinnum != 0:
            speed += 0.2

    for object in all_sprites:
        screen.blit(object.image, object.rect)
        object.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('sounds/crash.wav').play()
        time.sleep(0.5)
        screen.fill(red)
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)