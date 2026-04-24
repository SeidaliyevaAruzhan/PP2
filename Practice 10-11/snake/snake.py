import pygame
import time
import random

pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()

score_style = pygame.font.SysFont('comicsansms', 35)
font_style = pygame.font.SysFont("arial", 25)
direct = 'u'
fix = direct


def your_score(score):
    value = score_style.render("Your Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


def your_level(level):
    level_value = score_style.render("Level: " + str(level), True, yellow)
    screen.blit(level_value, [width - 150, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])


def gameLoop():
    global snake_speed
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1

    level = 1
    food_eaten = 0

    foods = [(green, 1), (yellow, 2), (red, 3)]
    foood = random.choice(foods)
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    food_time = pygame.time.get_ticks()

    while not game_over:
        global direct, fix
        while game_close:
            screen.fill(blue)
            message("You lost! Press C-Play Again or Q-Quit", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fix = 'l'
                elif event.key == pygame.K_RIGHT:
                    fix = 'r'
                elif event.key == pygame.K_UP:
                    fix = 'u'
                elif event.key == pygame.K_DOWN:
                    fix = 'd'

            if direct != 'u' and fix == 'd':
                direct = 'd'
            if direct != 'd' and fix == 'u':
                direct = 'u'
            if direct != 'l' and fix == 'r':
                direct = 'r'
            if direct != 'r' and fix == 'l':
                direct = 'l'

            if direct == 'l':
                x1_change = -snake_block
                y1_change = 0
            if direct == 'r':
                x1_change = snake_block
                y1_change = 0
            if direct == 'u':
                y1_change = -snake_block
                x1_change = 0
            if direct == 'd':
                y1_change = snake_block
                x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)

        now = pygame.time.get_ticks()
        if now - food_time > 5000:
            foood = random.choice(foods)
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            food_time = now

        pygame.draw.rect(screen, foood[0], [foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(length_of_snake - 1)
        your_level(level)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += foood[1]
            food_eaten += 1

            if food_eaten % 4 == 0:
                level += 1
                snake_speed += 5

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()