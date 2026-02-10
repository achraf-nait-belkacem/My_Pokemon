import SpriteAnimation
import pygame
import constantes
import sys

pokemon = SpriteAnimation("pokemon.png", (300, 200))

# dans la boucle
pygame.init()
screen = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
pygame.display.set_caption("Pokemon")
clock = pygame.time.Clock()
pokemon.update(screen)

# contrôles
running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 40))
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.key == pygame.K_SPACE:
            pokemon.set_state("attack")
        if event.key == pygame.K_h:
            pokemon.set_state("hit")
        if event.key == pygame.K_k:
            pokemon.set_state("ko")
    pygame.display.flip()

pygame.quit()
sys.exit()