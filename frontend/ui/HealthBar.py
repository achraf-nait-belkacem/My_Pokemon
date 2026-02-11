import pygame

class HealthBar:
    def __init__(self, x, y, width, height ,name ,max_hp ,max_xp=None , icon_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.name = name

        self.hp = max_hp
        self.max_hp = max_hp

        self.max_xp = max_xp
        self.xp = 20

        self.icon = None
        if icon_path:
            self.icon = pygame.image.load(icon_path).convert_alpha()
            self.icon = pygame.transform.scale(self.icon, (60, 60))


    def draw(self, surface):
        #pokemon box
        pygame.draw.rect(surface, "white", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "black", (self.x, self.y, self.width, self.height),2)

        #pokemon name
        self.font = pygame.font.SysFont("arial", 18)
        name_text = self.font.render(self.name, True, "black")
        surface.blit(name_text, (self.x + 10, self.y + 5))

        #pokemon icon
        if self.icon:
            surface.blit(self.icon, (self.x + 200, self.y -10 ))

        #pokemon health bar
        hp_ratio = self.hp / self.max_hp
        hp_bar_width = self.width - 20
        hp_bar_height = 15
        hp_x = self.x + 10
        hp_y = self.y + 30

        pygame.draw.rect(surface, "red", (hp_x, hp_y, hp_bar_width, hp_bar_height))
        pygame.draw.rect(surface, "green", (hp_x, hp_y, hp_bar_width * hp_ratio, hp_bar_height))

        #pokemon xp
        if self.max_xp is not None:
            xp_ratio = self.xp / self.max_xp
            xp_height = 8

            pygame.draw.rect(surface, "blue", (self.x, self.y + self.height + 5, self.width * xp_ratio, xp_height))