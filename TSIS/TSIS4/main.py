import pygame
import random
import json
import os
from db import create_tables, save_result, get_leaderboard, get_personal_best

pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
dark_red = (120, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (180, 180, 180)
purple = (160, 32, 240)
orange = (255, 165, 0)
cyan = (0, 255, 255)

snake_block = 10
base_speed = 15

font_big = pygame.font.SysFont("arial", 35)
font = pygame.font.SysFont("arial", 25)
font_small = pygame.font.SysFont("arial", 18)

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"snake_color": [0, 0, 0], "grid": False, "sound": True}
    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

settings = load_settings()

def draw_text(text, color, x, y, size="normal"):
    f = font
    if size == "big":
        f = font_big
    if size == "small":
        f = font_small
    img = f.render(text, True, color)
    screen.blit(img, (x, y))

def button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, white, rect)
    pygame.draw.rect(screen, black, rect, 2)
    draw_text(text, black, x + 20, y + 10)
    if rect.collidepoint(mouse) and click[0]:
        pygame.time.delay(200)
        return True
    return False

def random_position(snake_list, obstacles):
    while True:
        x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        y = round(random.randrange(40, height - snake_block) / 10.0) * 10.0
        if [x, y] not in snake_list and [x, y] not in obstacles:
            return x, y

def draw_grid():
    for x in range(0, width, snake_block):
        pygame.draw.line(screen, (80, 180, 230), (x, 0), (x, height))
    for y in range(0, height, snake_block):
        pygame.draw.line(screen, (80, 180, 230), (0, y), (width, y))

def username_screen():
    username = ""
    active = True

    while active:
        screen.fill(blue)
        draw_text("Enter username:", white, 180, 120, "big")
        pygame.draw.rect(screen, white, [150, 180, 300, 45])
        draw_text(username, black, 160, 188)
        draw_text("Press ENTER to continue", white, 170, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip() != "":
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:
                        username += event.unicode

        pygame.display.update()
        clock.tick(30)

def main_menu():
    while True:
        screen.fill(blue)
        draw_text("SNAKE GAME", white, 200, 60, "big")

        if button("Play", 220, 130, 160, 45):
            username = username_screen()
            game_loop(username)

        if button("Leaderboard", 220, 190, 160, 45):
            leaderboard_screen()

        if button("Settings", 220, 250, 160, 45):
            settings_screen()

        if button("Quit", 220, 310, 160, 45):
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(30)

def leaderboard_screen():
    while True:
        screen.fill(blue)
        draw_text("Leaderboard Top 10", white, 170, 30, "big")

        data = get_leaderboard()
        y = 90

        draw_text("Rank   User        Score   Level", yellow, 120, 65, "small")

        for i, row in enumerate(data):
            username, score, level, played_at = row
            draw_text(f"{i + 1}.     {username[:10]}        {score}       {level}", white, 120, y, "small")
            y += 25

        if button("Back", 230, 340, 140, 40):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(30)

def settings_screen():
    global settings

    colors = [
        [0, 0, 0],
        [0, 255, 0],
        [255, 255, 102],
        [213, 50, 80],
        [160, 32, 240]
    ]

    while True:
        screen.fill(blue)
        draw_text("Settings", white, 230, 40, "big")

        draw_text("Snake color:", white, 80, 120)
        x = 260
        for c in colors:
            pygame.draw.rect(screen, c, [x, 120, 35, 35])
            pygame.draw.rect(screen, white, [x, 120, 35, 35], 2)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if pygame.Rect(x, 120, 35, 35).collidepoint(mouse) and click[0]:
                settings["snake_color"] = c
                save_settings(settings)
                pygame.time.delay(200)
            x += 45

        grid_text = "Grid: ON" if settings["grid"] else "Grid: OFF"
        sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"

        if button(grid_text, 210, 180, 180, 40):
            settings["grid"] = not settings["grid"]
            save_settings(settings)

        if button(sound_text, 210, 235, 180, 40):
            settings["sound"] = not settings["sound"]
            save_settings(settings)

        if button("Save & Back", 210, 300, 180, 40):
            save_settings(settings)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(30)

def game_over_screen(username, score, level, best):
    save_result(username, score, level)

    while True:
        screen.fill(blue)
        draw_text("GAME OVER", red, 200, 70, "big")
        draw_text(f"Score: {score}", white, 230, 130)
        draw_text(f"Level: {level}", white, 230, 165)
        draw_text(f"Personal Best: {max(best, score)}", yellow, 190, 200)

        if button("Retry", 150, 280, 130, 45):
            game_loop(username)

        if button("Main Menu", 320, 280, 150, 45):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(30)

def game_loop(username):
    global settings

    snake_speed = base_speed
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    direction = None

    snake_list = []
    length_of_snake = 1

    level = 1
    food_eaten = 0
    score = 0

    foods = [(green, 1), (yellow, 2), (red, 3)]
    current_food = random.choice(foods)
    obstacles = []

    foodx, foody = random_position(snake_list, obstacles)
    food_time = pygame.time.get_ticks()

    poison_active = True
    poisonx, poisony = random_position(snake_list, obstacles)

    power_active = False
    power_type = None
    powerx, powery = 0, 0
    power_spawn_time = 0
    power_effect = None
    power_effect_time = 0
    shield = False

    best = get_personal_best(username)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        hit_wall = x1 >= width or x1 < 0 or y1 >= height or y1 < 40
        hit_obstacle = [x1, y1] in obstacles

        if hit_wall or hit_obstacle:
            if shield:
                shield = False
                x1 = width / 2
                y1 = height / 2
                snake_list = []
                length_of_snake = max(1, length_of_snake)
            else:
                game_over_screen(username, score, level, best)
                return

        screen.fill(blue)

        if settings["grid"]:
            draw_grid()

        now = pygame.time.get_ticks()

        if now - food_time > 5000:
            current_food = random.choice(foods)
            foodx, foody = random_position(snake_list, obstacles)
            food_time = now

        if not power_active and random.randint(1, 250) == 1:
            power_active = True
            power_type = random.choice(["speed", "slow", "shield"])
            powerx, powery = random_position(snake_list, obstacles)
            power_spawn_time = now

        if power_active and now - power_spawn_time > 8000:
            power_active = False

        if power_effect in ["speed", "slow"] and now - power_effect_time > 5000:
            power_effect = None
            snake_speed = base_speed + (level - 1) * 5

        pygame.draw.rect(screen, current_food[0], [foodx, foody, snake_block, snake_block])

        if poison_active:
            pygame.draw.rect(screen, dark_red, [poisonx, poisony, snake_block, snake_block])

        if power_active:
            color = orange
            if power_type == "slow":
                color = cyan
            elif power_type == "shield":
                color = purple
            pygame.draw.rect(screen, color, [powerx, powery, snake_block, snake_block])

        for obs in obstacles:
            pygame.draw.rect(screen, gray, [obs[0], obs[1], snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for part in snake_list[:-1]:
            if part == snake_head:
                if shield:
                    shield = False
                    snake_list = snake_list[-length_of_snake:]
                else:
                    game_over_screen(username, score, level, best)
                    return

        for part in snake_list:
            pygame.draw.rect(screen, tuple(settings["snake_color"]), [part[0], part[1], snake_block, snake_block])

        draw_text(f"Score: {score}", yellow, 5, 5, "small")
        draw_text(f"Level: {level}", yellow, 170, 5, "small")
        draw_text(f"Best: {best}", yellow, 300, 5, "small")
        if shield:
            draw_text("Shield", purple, 470, 5, "small")

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            length_of_snake += current_food[1]
            score += current_food[1]
            food_eaten += 1
            current_food = random.choice(foods)
            foodx, foody = random_position(snake_list, obstacles)
            food_time = now

            if food_eaten % 4 == 0:
                level += 1
                snake_speed += 5

                if level >= 3:
                    for i in range(level):
                        ox, oy = random_position(snake_list, obstacles)
                        if abs(ox - x1) > 30 or abs(oy - y1) > 30:
                            obstacles.append([ox, oy])

        if poison_active and x1 == poisonx and y1 == poisony:
            length_of_snake -= 2
            if length_of_snake <= 1:
                game_over_screen(username, score, level, best)
                return
            snake_list = snake_list[-length_of_snake:]
            poisonx, poisony = random_position(snake_list, obstacles)

        if power_active and x1 == powerx and y1 == powery:
            if power_type == "speed":
                snake_speed += 8
                power_effect = "speed"
                power_effect_time = now
            elif power_type == "slow":
                snake_speed = max(5, snake_speed - 8)
                power_effect = "slow"
                power_effect_time = now
            elif power_type == "shield":
                shield = True

            power_active = False

        clock.tick(snake_speed)

create_tables()
main_menu()