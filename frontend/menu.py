import pygame
from pygame.locals import *

class First_screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.button_tool = Rect()
        self.font = pygame.font.SysFont("Arial", 30)

        self.bg = pygame.image.load("assets/sprites/poke_bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1920, 1000))
        self.play_button_jouer = None
        self.play_button_pokedex = None
        self.play_button_quit = None
        self.selected_index = 0
        self.buttons_count = 3
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % 3                        
                    
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % 3

                
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 0:
                        print("Lancement du jeu")
                        self.running = False
                    if self.selected_index == 1:
                        print("Ouverture du pokedex")
                    if self.selected_index == 2:
                        self.running = False
                        pygame.quit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.bg,(0, 0))
        self.play_button_jouer = self.button_tool.draw_buttons(self.screen, "JOUER", 860, 300, 200, 60, self.font, self.selected_index == 0)
        self.play_button_pokedex = self.button_tool.draw_buttons(self.screen, "POKEDEX", 860, 450, 200, 60, self.font, self.selected_index == 1)
        self.play_button_quit = self.button_tool.draw_buttons(self.screen, "QUIT", 860, 600, 200, 60, self.font, self.selected_index == 2, self.button_tool.danger_color)
        pygame.display.flip()

    def run(self):
        while self.running == True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

class Rect:
    def __init__(self):
        self.white = (255, 255, 255)
        self.gray_hover = (245, 245, 245)
        self.text_dark = (60, 60, 60)
        self.border_color = (230, 230, 230)
        self.danger_color = (255, 50, 50)
        self.default_accent = (140, 100, 40)

    def draw_buttons(self, screen, text, x, y, w, h, font, is_selected, color = None):
        if color is None:
            color = self.default_accent

        button_rect = pygame.Rect(x, y , w, h)

        bg_color = (min(color[0]+30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255)) if is_selected else color
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
        text_surf = font.render(text, True, self.white)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        return button_rect
    
    