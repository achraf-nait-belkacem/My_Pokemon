from SpriteAnimation import SpriteAnimation
import pygame
import constantes
import sys
from HealthBar import HealthBar

pygame.init()


screen = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
pygame.display.set_caption("Pokemon")
clock = pygame.time.Clock()
pokemon = SpriteAnimation("assets/sprites/pokemon.png", (300, 200)
)
# health bar class
health_bar = HealthBar(250, 200, 300, 40, 100)

running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 40))

    #health bar
    health_bar.hp = 50
    health_bar.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                pokemon.set_state("attack")
            if event.key == pygame.K_h:
                pokemon.set_state("hit")
            if event.key == pygame.K_k:
                pokemon.set_state("ko")
    pokemon.update(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()