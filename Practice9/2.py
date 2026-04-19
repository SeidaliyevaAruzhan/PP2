import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Music Player")

music_folder = "music"
playlist = [file for file in os.listdir(music_folder) if file.endswith(".mp3") or file.endswith(".wav")]

current = 0
playing = False

font = pygame.font.Font(None, 36)

def play_music():
    global playing
    if playlist:
        pygame.mixer.music.load(os.path.join(music_folder, playlist[current]))
        pygame.mixer.music.play()
        playing = True

def stop_music():
    global playing
    pygame.mixer.music.stop()
    playing = False

def next_music():
    global current
    if playlist:
        current = (current + 1) % len(playlist)
        play_music()

def prev_music():
    global current
    if playlist:
        current = (current - 1) % len(playlist)
        play_music()

running = True
while running:
    screen.fill((255, 255, 255))

    if playlist:
        text = font.render("Track: " + playlist[current], True, (0, 0, 0))
    else:
        text = font.render("No music files found", True, (0, 0, 0))

    screen.blit(text, (20, 80))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_music()
            if event.key == pygame.K_s:
                stop_music()
            if event.key == pygame.K_n:
                next_music()
            if event.key == pygame.K_b:
                prev_music()
            if event.key == pygame.K_q:
                running = False

pygame.quit()