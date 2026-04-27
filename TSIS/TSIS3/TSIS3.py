import pygame
import sys
import random
import json
import os
import time

pygame.init()
pygame.mixer.init()

w, h = 400, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (220, 30, 30)
green = (30, 180, 70)
blue = (40, 90, 220)
yellow = (240, 210, 50)
gray = (120, 120, 120)
dark = (40, 40, 40)
orange = (255, 140, 0)
purple = (150, 70, 220)

font_big = pygame.font.SysFont("Verdana", 42)
font = pygame.font.SysFont("Verdana", 24)
font_small = pygame.font.SysFont("Verdana", 18)

leaderboard_file = "leaderboard.json"
settings_file = "settings.json"

def load_image(path, size=None, color=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        surf = pygame.Surface(size if size else (50, 50), pygame.SRCALPHA)
        surf.fill(color if color else red)
        return surf

def play_sound(path):
    if settings["sound"]:
        try:
            pygame.mixer.Sound(path).play()
        except:
            pass

def load_settings():
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                return json.load(f)
        except:
            pass
    return {"sound": True, "car_color": "red", "difficulty": "medium"}

def save_settings():
    with open(settings_file, "w") as f:
        json.dump(settings, f)

def load_scores():
    if os.path.exists(leaderboard_file):
        try:
            with open(leaderboard_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_score(name, score, distance):
    data = load_scores()
    data.append({"name": name, "score": score, "distance": int(distance)})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    with open(leaderboard_file, "w") as f:
        json.dump(data, f)

settings = load_settings()

background = load_image("images/street.png", (w, h), gray)
enemy_img = load_image("images/enemy.png", (45, 85), blue)
coin_img = load_image("images/coin.jpeg", (28, 28), yellow)
player_base = load_image("images/player.png", (50, 90), red)

def color_car(img, color_name):
    img = img.copy()
    overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
    colors = {
        "red": (255, 0, 0, 90),
        "blue": (0, 80, 255, 90),
        "green": (0, 220, 70, 90),
        "yellow": (255, 220, 0, 90)
    }
    overlay.fill(colors.get(color_name, (255, 0, 0, 90)))
    img.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return img

def draw_text(text, x, y, f=font_small, color=black):
    img = f.render(text, True, color)
    screen.blit(img, (x, y))
    return img

def button(text, x, y, bw, bh, color=dark):
    mx, my = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, bw, bh)
    pygame.draw.rect(screen, color if not rect.collidepoint(mx, my) else gray, rect, border_radius=12)
    label = font.render(text, True, white)
    screen.blit(label, (x + bw // 2 - label.get_width() // 2, y + bh // 2 - label.get_height() // 2))
    return rect

def get_name():
    name = ""
    active = True
    while active:
        screen.fill(white)
        draw_text("Enter your name:", 55, 180, font)
        pygame.draw.rect(screen, black, (60, 240, 280, 45), 2)
        draw_text(name, 70, 250, font)
        draw_text("Press ENTER to start", 80, 320, font_small)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player"
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)

    return name

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = color_car(player_base, settings["car_color"])
        self.rect = self.image.get_rect()
        self.rect.center = (200, 510)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < h:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 25:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < w - 25:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = self.safe_position()

    def safe_position(self):
        x = random.choice([90, 160, 240, 310])
        return (x, random.randint(-700, -80))

    def move(self, game_speed):
        self.rect.y += game_speed + 2
        if self.rect.top > h:
            self.rect.center = self.safe_position()

class Coin(pygame.sprite.Sprite):
    def __init__(self, value, size):
        super().__init__()
        self.value = value
        self.image = pygame.transform.scale(coin_img, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = self.new_pos()

    def new_pos(self):
        return (random.choice([90, 160, 240, 310]), random.randint(-500, -50))

    def move(self, game_speed):
        self.rect.y += game_speed
        if self.rect.top > h:
            self.rect.center = self.new_pos()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((45, 45), pygame.SRCALPHA)
        if kind == "oil":
            pygame.draw.ellipse(self.image, black, (2, 8, 40, 28))
        elif kind == "bump":
            pygame.draw.rect(self.image, orange, (0, 15, 45, 15), border_radius=6)
        else:
            pygame.draw.rect(self.image, gray, (3, 3, 39, 39), border_radius=5)
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice([90, 160, 240, 310]), random.randint(-900, -100))

    def move(self, game_speed):
        self.rect.y += game_speed
        if self.rect.top > h:
            self.rect.center = (random.choice([90, 160, 240, 310]), random.randint(-900, -100))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        color = blue if self.kind == "nitro" else purple if self.kind == "shield" else green
        pygame.draw.circle(self.image, color, (17, 17), 17)
        letter = "N" if self.kind == "nitro" else "S" if self.kind == "shield" else "R"
        t = font_small.render(letter, True, white)
        self.image.blit(t, (17 - t.get_width() // 2, 17 - t.get_height() // 2))
        self.rect = self.image.get_rect()
        self.spawn_time = pygame.time.get_ticks()
        self.rect.center = (random.choice([90, 160, 240, 310]), random.randint(-700, -100))

    def move(self, game_speed):
        self.rect.y += game_speed
        if self.rect.top > h or pygame.time.get_ticks() - self.spawn_time > 7000:
            self.kill()

def game_loop(name):
    base_speed = 4
    if settings["difficulty"] == "easy":
        base_speed = 3
    elif settings["difficulty"] == "hard":
        base_speed = 6

    speed = base_speed
    score = 0
    coins_score = 0
    distance = 0
    active_power = None
    power_start = 0
    shield = False
    running = True
    last_power_spawn = pygame.time.get_ticks()

    player = Player()

    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    for _ in range(2):
        enemies.add(Enemy(speed))

    coins.add(Coin(1, 20))
    coins.add(Coin(2, 28))
    coins.add(Coin(3, 35))

    for _ in range(3):
        obstacles.add(Obstacle(random.choice(["oil", "bump", "barrier"])))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))

        distance += speed * 0.04
        score = int(distance) + coins_score

        if int(distance) % 200 == 0 and len(enemies) < 5:
            enemies.add(Enemy(speed))

        if pygame.time.get_ticks() - last_power_spawn > 6000:
            if len(powerups) < 1:
                powerups.add(PowerUp())
            last_power_spawn = pygame.time.get_ticks()

        if active_power == "nitro":
            speed = base_speed + 4
            if pygame.time.get_ticks() - power_start > 4000:
                active_power = None
                speed = base_speed

        if active_power == "shield":
            shield = True

        draw_text("Score: " + str(score), 10, 10)
        draw_text("Coins: " + str(coins_score), 10, 35)
        draw_text("Distance: " + str(int(distance)), 10, 60)

        if active_power:
            left = max(0, 4 - (pygame.time.get_ticks() - power_start) // 1000)
            if active_power == "shield":
                draw_text("Power: Shield", 230, 10)
            elif active_power == "nitro":
                draw_text("Power: Nitro " + str(left), 230, 10)

        player.move()
        screen.blit(player.image, player.rect)

        for enemy in enemies:
            enemy.move(speed)
            screen.blit(enemy.image, enemy.rect)

        for coin in coins:
            coin.move(speed)
            screen.blit(coin.image, coin.rect)

        for obs in obstacles:
            obs.move(speed)
            screen.blit(obs.image, obs.rect)

        for p in powerups:
            p.move(speed)
            screen.blit(p.image, p.rect)

        hit_coin = pygame.sprite.spritecollideany(player, coins)
        if hit_coin:
            coins_score += hit_coin.value
            play_sound("sounds/coinsound.mp3")
            hit_coin.rect.center = hit_coin.new_pos()

        hit_power = pygame.sprite.spritecollideany(player, powerups)
        if hit_power:
            if active_power is None:
                active_power = hit_power.kind
                power_start = pygame.time.get_ticks()
                if hit_power.kind == "repair":
                    for obs in obstacles:
                        obs.kill()
                        break
                    active_power = None
                hit_power.kill()

        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

        if hit_enemy or hit_obstacle:
            if shield:
                shield = False
                active_power = None
                if hit_enemy:
                    hit_enemy.rect.center = hit_enemy.safe_position()
                if hit_obstacle:
                    hit_obstacle.rect.center = (random.choice([90, 160, 240, 310]), random.randint(-900, -100))
            else:
                play_sound("sounds/crash.wav")
                save_score(name, score, distance)
                return score, coins_score, distance

        pygame.display.update()
        clock.tick(60)

def main_menu():
    while True:
        screen.fill(white)
        draw_text("RACER GAME", 50, 70, font_big)
        play_btn = button("Play", 90, 170, 220, 50)
        lead_btn = button("Leaderboard", 90, 240, 220, 50)
        set_btn = button("Settings", 90, 310, 220, 50)
        quit_btn = button("Quit", 90, 380, 220, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    name = get_name()
                    score, coins, distance = game_loop(name)
                    game_over_screen(score, coins, distance)
                if lead_btn.collidepoint(event.pos):
                    leaderboard_screen()
                if set_btn.collidepoint(event.pos):
                    settings_screen()
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

def game_over_screen(score, coins, distance):
    while True:
        screen.fill(red)
        draw_text("GAME OVER", 55, 90, font_big, white)
        draw_text("Score: " + str(score), 110, 170, font, white)
        draw_text("Coins: " + str(coins), 110, 210, font, white)
        draw_text("Distance: " + str(int(distance)), 110, 250, font, white)

        retry = button("Retry", 90, 330, 220, 50)
        menu = button("Main Menu", 90, 400, 220, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(event.pos):
                    name = get_name()
                    score, coins, distance = game_loop(name)
                    game_over_screen(score, coins, distance)
                if menu.collidepoint(event.pos):
                    return

        pygame.display.update()
        clock.tick(60)

def leaderboard_screen():
    while True:
        screen.fill(white)
        draw_text("LEADERBOARD", 55, 40, font_big)

        scores = load_scores()
        y = 120
        if not scores:
            draw_text("No scores yet", 120, 180, font)
        else:
            for i, s in enumerate(scores[:10]):
                text = f"{i + 1}. {s['name']} - {s['score']} - {s['distance']}m"
                draw_text(text, 40, y, font_small)
                y += 35

        back = button("Back", 90, 520, 220, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    return

        pygame.display.update()
        clock.tick(60)

def settings_screen():
    colors = ["red", "blue", "green", "yellow"]
    difficulties = ["easy", "medium", "hard"]

    while True:
        screen.fill(white)
        draw_text("SETTINGS", 85, 50, font_big)

        sound_btn = button("Sound: " + ("On" if settings["sound"] else "Off"), 70, 150, 260, 45)
        color_btn = button("Car Color: " + settings["car_color"], 70, 220, 260, 45)
        diff_btn = button("Difficulty: " + settings["difficulty"], 70, 290, 260, 45)
        back = button("Back", 70, 430, 260, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings()

                if color_btn.collidepoint(event.pos):
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i + 1) % len(colors)]
                    save_settings()

                if diff_btn.collidepoint(event.pos):
                    i = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(i + 1) % len(difficulties)]
                    save_settings()

                if back.collidepoint(event.pos):
                    save_settings()
                    return

        pygame.display.update()
        clock.tick(60)

main_menu()