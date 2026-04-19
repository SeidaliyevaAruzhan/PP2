import pygame
import math
from datetime import datetime

pygame.init()


screen = pygame.display.set_mode((1400, 1050))
pygame.display.set_caption("Mickey Clock")

bg = pygame.image.load("Lab9/images/mickeyWithoutArms.png").convert_alpha()
left_hand = pygame.image.load("Lab9/images/leftarm.png").convert_alpha()
right_hand = pygame.image.load("Lab9/images/rightarm.png").convert_alpha()

clock = pygame.time.Clock()
CENTER = (700, 525)

def rotate_hand(image, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(image, -angle)
    rect = rotated_image.get_rect(center=pivot)
    rect.centerx += offset[0]
    rect.centery += offset[1]
    screen.blit(rotated_image, rect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = (minutes / 60) * 360
    second_angle = (seconds / 60) * 360

    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))

    rotate_hand(right_hand, minute_angle, CENTER, (0, -15))
    rotate_hand(left_hand, second_angle, CENTER, (0, -15))

    pygame.display.update()
    clock.tick(1)

pygame.quit()