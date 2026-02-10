import pygame
from loading import Loading_menu
from menu import First_screen

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("My_Pokemon")
        self.clock = pygame.time.Clock()
        self.running = True

    def fade_out(self):
        fade = pygame.Surface((1920, 1080))
        fade.fill((0, 0, 0))
        for alpha in range(0, 255, 5):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)

    def run(self):

        loading = Loading_menu(self.screen)
        loading.run()
        self.fade_out()
        menu = First_screen(self.screen)
        menu.run()
        pygame.quit()

if __name__ == "__main__":
    app = GameApp()
    app.run()