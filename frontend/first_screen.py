import pygame
from pygame.locals import *
from frontend.utils import Rect
# On importe la classe DataManager et non des fonctions qui n'existent pas seules
from backend.data_manager import DataManager 

class First_screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.button_tool = Rect()
        self.font = pygame.font.SysFont("Arial", 30)

        # On crée l'outil de gestion des données
        self.db = DataManager()
        
        # On utilise l'outil pour charger les listes
        self.pokemons = self.db.load_pokedex()
        self.ennemi = self.db.load_all_ennemi()

        self.moving_index = None
        
        # --- MODIFICATION : Liste d'ennemis par défaut ---
        # On remplit la liste avec tous les IDs d'ennemis chargés automatiquement
        self.selected_ennemi_ids = [p.id for p in self.ennemi]
        
        self.bg = pygame.transform.scale(pygame.image.load("assets/sprites/poke_bg.png").convert_alpha(), (1920, 1000))
        self.bg_pokedex = pygame.transform.scale(pygame.image.load("assets/sprites/bg_pokedex.png").convert_alpha(), (1920, 1000))
        
        self.state = "MENU"
        self.selected_index = 0
        self.buttons_count = 4

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_UP: 
                        self.selected_index = (self.selected_index - 1) % self.buttons_count
                    elif event.key == pygame.K_DOWN: 
                        self.selected_index = (self.selected_index + 1) % self.buttons_count
                    elif event.key == pygame.K_RETURN:
                        if self.selected_index == 0:
                            # --- SÉCURITÉ : On vérifie s'il y a des ennemis, sinon on remet tout ---
                            if not self.selected_ennemi_ids:
                                self.selected_ennemi_ids = [p.id for p in self.ennemi]
                                
                            return {
                                "Equipe": self.pokemons, 
                                "Ennemis possibles": [p for p in self.ennemi if p.id in self.selected_ennemi_ids]
                            }
                        elif self.selected_index == 1: 
                            self.state = "POKEDEX"
                            self.selected_index = 0 # Reset index
                        elif self.selected_index == 2: 
                            self.state = "ENNEMI"
                            self.selected_index = 0 # Reset index
                        elif self.selected_index == 3: return "QUIT"

                elif self.state == "POKEDEX":
                    if event.key == pygame.K_UP: 
                        self.selected_index = (self.selected_index - 1) % len(self.pokemons)
                    elif event.key == pygame.K_DOWN: 
                        self.selected_index = (self.selected_index + 1) % len(self.pokemons)
                    elif event.key == pygame.K_RETURN:
                        if self.moving_index is None:
                            self.moving_index = self.selected_index
                        else:
                            i1, i2 = self.moving_index, self.selected_index
                            self.pokemons[i1], self.pokemons[i2] = self.pokemons[i2], self.pokemons[i1]
                            self.moving_index = None
                            self.db.save_team(self.pokemons)
                    elif event.key == pygame.K_ESCAPE: 
                        self.state = "MENU"
                        self.selected_index = 1 # Focus sur POKEDEX
                        self.moving_index = None

                elif self.state == "ENNEMI":
                    if event.key == pygame.K_UP: 
                        self.selected_index = (self.selected_index - 1) % len(self.ennemi)
                    elif event.key == pygame.K_DOWN: 
                        self.selected_index = (self.selected_index + 1) % len(self.ennemi)
                    elif event.key == pygame.K_RETURN:
                        target_id = self.ennemi[self.selected_index].id
                        if target_id in self.selected_ennemi_ids:
                            self.selected_ennemi_ids.remove(target_id)
                        else:
                            self.selected_ennemi_ids.append(target_id)
                    elif event.key == pygame.K_ESCAPE: 
                        self.state = "MENU"
                        self.selected_index = 2 # Focus sur ENNEMI
        return None

    def draw(self):
        self.screen.fill((30, 30, 30))
        
        if self.state == "MENU":
            self.screen.blit(self.bg, (0, 0))
            self.button_tool.draw_buttons(self.screen, "JOUER", 860, 220, 200, 60, self.font, self.selected_index == 0)
            self.button_tool.draw_buttons(self.screen, "POKEDEX", 860, 350, 200, 60, self.font, self.selected_index == 1)
            self.button_tool.draw_buttons(self.screen, "ENNEMI", 860, 500, 200, 60, self.font, self.selected_index == 2)
            self.button_tool.draw_buttons(self.screen, "QUIT", 860, 650, 200, 60, self.font, self.selected_index == 3, (255, 50, 50))
        
        elif self.state in ["ENNEMI", "POKEDEX"]:
            self.screen.blit(self.bg_pokedex, (0, 0))
            liste = self.ennemi if self.state == "ENNEMI" else self.pokemons
            
            start_index = max(0, self.selected_index - 2)
            end_index = min(len(liste), start_index + 5)
            
            for relative_i, i in enumerate(range(start_index, end_index)):
                poke = liste[i]
                y_pos = 350 + (relative_i * 100)
                is_selected = (i == self.selected_index)
                
                # Couleur verte si l'ennemi est dans la liste de combat
                color = None
                if self.state == "ENNEMI" and poke.id in self.selected_ennemi_ids:
                    color = (50, 200, 50)
                if i == self.moving_index:
                    color = (200, 150, 0)
                
                self.button_tool.draw_buttons(self.screen, poke.name, 750, y_pos, 400, 80, self.font, is_selected, color)
                
                if is_selected:
                    try:
                        sprite = pygame.image.load(poke.sprite_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (300, 300))
                        self.screen.blit(sprite, (200, 300)) 
                        stats = f"HP: {poke.hp} | ATK: {poke.attack} | DEF: {poke.defense}"
                        self.screen.blit(self.font.render(stats, True, (255, 255, 255)), (80, 720))
                    except:
                        pass
        
        pygame.display.flip()

    def run(self):
        while self.running:
            result = self.handle_events()
            if result: 
                return result
            self.draw()
            self.clock.tick(60)