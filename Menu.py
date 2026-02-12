import pygame
import math
import sys


pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon ")
clock = pygame.time.Clock()


sprite = pygame.image.load("assets/sprites/pokemon.png").convert_alpha()
sprite = pygame.transform.scale(sprite, (120, 120))


state = "idle"
timer = 0
base_pos = (WIDTH // 2, HEIGHT // 2)


def draw_idle(img, time):
    offset = math.sin(time * 0.1) * 4
    rect = img.get_rect(center=(base_pos[0], base_pos[1] + offset))
    screen.blit(img, rect)

def draw_attack(img, frame):
    shake = [-10, 10, -6, 6, -3, 3, 0]
    offset = shake[min(frame, len(shake) - 1)]
    rect = img.get_rect(center=(base_pos[0] + offset, base_pos[1]))
    screen.blit(img, rect)

def draw_hit(img, frame):
    flash = img.copy()
    flash.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_ADD)
    rect = flash.get_rect(center=base_pos)
    screen.blit(flash, rect)

def draw_ko(img, frame):
    alpha = max(0, 255 - frame * 5)
    fade = img.copy()
    fade.set_alpha(alpha)
    rect = fade.get_rect(center=base_pos)
    screen.blit(fade, rect)


running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 40))
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = "attack"
                timer = 0
            if event.key == pygame.K_h:
                state = "hit"
                timer = 0
            if event.key == pygame.K_k:
                state = "ko"
                timer = 0


    if state == "idle":
        draw_idle(sprite, timer)

    elif state == "attack":
        draw_attack(sprite, timer)
        if timer > 20:
            state = "idle"
            timer = 0

    elif state == "hit":
        draw_hit(sprite, timer)
        if timer > 15:
            state = "idle"
            timer = 0

    elif state == "ko":
        draw_ko(sprite, timer)

    pygame.display.flip()

pygame.quit()
sys.exit()
