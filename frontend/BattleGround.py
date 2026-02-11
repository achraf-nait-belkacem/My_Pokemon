import pygame

class BattleGround:
    def __init__(self, image_path, position):
        self.img = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (300, 120))

        self.x, self.y = position

    def display(self, surface):
        surface.blit(self.img, (self.x, self.y))
