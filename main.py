import pygame
import random
from frontend.loading import Loading_menu
from frontend.first_screen import First_screen

def fade_out(screen):
    fade = pygame.Surface((1920, 1000))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(15)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1000))
    pygame.display.set_caption("My_Pokemon")
    
    loader = Loading_menu(screen)
    loader.run()
    
    fade_out(screen)

    menu = First_screen(screen)
    data = menu.run()

    if data and data != "QUIT":
        fade_out(screen)
        equipe = data["Equipe"]
        ennemis = data["Ennemis possibles"]
        adversaire = random.choice(ennemis)
        print(f"Joueur: {equipe[0].name} vs Ennemi: {adversaire.name}")

    pygame.quit()

if __name__ == "__main__":
    main()