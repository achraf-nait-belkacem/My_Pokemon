from SpriteAnimation import SpriteAnimation
import pygame
import constantes
import sys
from ui.HealthBar import HealthBar
from ui.ActionMenu import ActionMenu
from BattleGround import BattleGround

pygame.init()


screen = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
pygame.display.set_caption("Pokemon")
clock = pygame.time.Clock()


#sprite class
pokemon_back = pygame.image.load("assets/sprites/back_pokemon.png").convert_alpha()
pokemon_back = pygame.transform.scale(pokemon_back, (250, 250))

pokemon_front = pygame.image.load("assets/sprites/front_pokemon.png").convert_alpha()
pokemon_front = pygame.transform.scale(pokemon_front, (180, 180))


# health bar class
my_health_bar = HealthBar((constantes.WIDTH / 10), (constantes.HEIGHT /5 ), 250, 70, "TEST", 100, 100,"assets/icons/1.png")
enemy_health_bar = HealthBar((constantes.WIDTH /1.8), (constantes.HEIGHT /3), 250, 70, "TEST", 100, None)

#fighting ground class
my_fighting_ground = BattleGround("assets/stage/my_plateforme.png", (constantes.WIDTH / 7, constantes.HEIGHT / 2.5))
enemy_fighting_ground = BattleGround("assets/stage/enemy_plateforme.png", (constantes.WIDTH /2, constantes.HEIGHT / 7))

#action menu class
# action_background = ActionMenu((constantes.WIDTH - constantes.WIDTH), (constantes.HEIGHT / 1.75), constantes.WIDTH, constantes.HEIGHT)

fight_button = ActionMenu( "FIGHT", (constantes.WIDTH / 3 + 80, constantes.HEIGHT / 1.5 +40), "assets/buttons/fight.png", (constantes.WIDTH / 3, constantes.HEIGHT / 1.5), (230, 100))
run_button = ActionMenu( "RUN", (constantes.WIDTH / 6 + 40, constantes.HEIGHT / 1.2 + 20), "assets/buttons/run.png", (constantes.WIDTH / 6, constantes.HEIGHT / 1.2), (150, 70))
switch_pokemon_button = ActionMenu( "POKEMON", (constantes.WIDTH / 1.7 + 40, constantes.HEIGHT / 1.2 + 20), "assets/buttons/switch_pokemon.png", (constantes.WIDTH / 1.7, constantes.HEIGHT / 1.2), (150, 70))
# will go to that position when an item button will be made
# run_button = ActionMenu("assets/buttons/run.png", (constantes.WIDTH / 2.7, constantes.HEIGHT / 1.15), (150, 70))




# Positions
back_pos = (constantes.WIDTH / 7 + 20, constantes.HEIGHT / 2.5 - 75)
front_pos = (constantes.WIDTH /2 + 65 , constantes.HEIGHT / 7 - 50)

running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 40))

    #fighting ground
    my_fighting_ground.display(screen)
    enemy_fighting_ground.display(screen)

    #health bar
    my_health_bar.hp = 50
    my_health_bar.draw(screen)
    enemy_health_bar.draw(screen)

    screen.blit(pokemon_back, back_pos)
    screen.blit(pokemon_front, front_pos)

    #Action background
    fight_button.display(screen)
    run_button.display(screen)
    switch_pokemon_button.display(screen)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Sprite animation

    #     if event.type == pygame.KEYDOWN:

    #         if event.key == pygame.K_SPACE:
    #             pokemon.set_state("attack")
    #         if event.key == pygame.K_h:
    #             pokemon.set_state("hit")
    #         if event.key == pygame.K_k:
    #             pokemon.set_state("ko")
    # pokemon.update(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()