import pygame
from pygame.locals import *

class Loading_menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("../assets/sprites/bg.png").convert_alpha()
        self.text = pygame.image.load("../assets/sprites/txt.png").convert_alpha()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.bg,(0, 0))
        self.screen.blit(self.text,(0, 0))
        pygame.display.flip()

    def run(self):
        while self.running == True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption("My_Pokemon")
    menu = Loading_menu(screen)
    menu.run()
    pygame.quit

main()

