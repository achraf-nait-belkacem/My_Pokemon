import pygame
from pygame.locals import *

class First_screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.button_tool = Rect()
        self.font = pygame.font.SysFont("Arial", 30)

        self.pokemons = ["Pikachu", "Bulbizarre", "Salamèche", "Carapuce"]
        self.moving_index = None


        self.bg = pygame.image.load("assets/sprites/poke_bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1920, 1000))
        self.bg_pokedex = pygame.image.load("assets/sprites/bg_pokedex.png").convert_alpha()
        self.bg_pokedex = pygame.transform.scale(self.bg_pokedex,(1920, 1000))
        
        self.state = "MENU"
        self.selected_index = 0
        self.buttons_count = 3
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % self.buttons_count                       
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % self.buttons_count
                    elif event.key == pygame.K_RETURN:
                        if self.selected_index == 0:
                            self.running = False
                        elif self.selected_index == 1:
                            self.state = "POKEDEX"
                        elif self.selected_index == 2:
                            self.running = False
                            pygame.quit()

                elif self.state == "POKEDEX":
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.pokemons)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.pokemons)
                    elif event.key == pygame.K_RETURN:
                        if self.moving_index is None:
                            self.moving_index = self.selected_index
                        else : 
                            i1, i2 = self.moving_index, self.selected_index
                            self.pokemons[i1], self.pokemons[i2] = self.pokemons[i2], self.pokemons[i1]
                            self.moving_index = None
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        self.moving_index = None

    def draw(self):
        self.screen.fill((30, 30, 30))

        if self.state == "MENU":
            self.screen.blit(self.bg, (0, 0))
            self.button_tool.draw_buttons(self.screen, "JOUER", 860, 300, 200, 60, self.font, self.selected_index == 0)
            self.button_tool.draw_buttons(self.screen, "POKEDEX", 860, 450, 200, 60, self.font, self.selected_index == 1)
            self.button_tool.draw_buttons(self.screen, "QUIT", 860, 600, 200, 60, self.font, self.selected_index == 2, self.button_tool.danger_color)
        
        elif self.state == "POKEDEX":
            self.screen.blit(self.bg_pokedex, (0, 0))

            for i, name in enumerate(self.pokemons):
                y_pos = 350 + (i * 100)
                current_color = (200, 150, 0) if i == self.moving_index else None

                self.button_tool.draw_buttons(
                    self.screen, name, 750, y_pos, 400, 80,
                    self.font, (i == self.selected_index), current_color
                )
            
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

class Rect:
    def __init__(self):
        self.white = (255, 255, 255)
        self.danger_color = (255, 50, 50)
        self.default_accent = (140, 100, 40)

    def draw_buttons(self, screen, text, x, y, w, h, font, is_selected, color = None):
        if color is None:
            color = self.default_accent

        button_rect = pygame.Rect(x, y , w, h)
        bg_color = (min(color[0]+30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255)) if is_selected else color
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
        
        if is_selected:
            pygame.draw.rect(screen, self.white, button_rect, 3, border_radius=12)

        text_surf = font.render(text, True, self.white)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        return button_rect