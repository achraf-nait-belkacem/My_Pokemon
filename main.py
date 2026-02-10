import pygame
from frontend.loading import Loading_menu
from frontend.menu import First_screen
from frontend.game_app import GameApp

import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("My_Pokemon")
    fade = GameApp()
    loading = Loading_menu(screen)
    loading.run()
    fade.fade_out()
    menu = First_screen(screen)
    menu.run()
    pygame.quit

if __name__ == "__main__":
    main()