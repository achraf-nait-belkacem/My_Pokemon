import pygame

class ActionMenu:
    def __init__(self, text, text_position, image_path, position, size):
        self.img = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, size)

        self.x, self.y = position
        self.tx, self.ty = text_position
        self.text = text

    def display(self, surface):
        surface.blit(self.img, (self.x, self.y))
        self.font = pygame.font.SysFont("assets/fonts/pokemon_font.ttf", 30)
        text = self.font.render(self.text, True, "black")
        surface.blit(text, (self.tx, self.ty))
