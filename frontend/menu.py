import pygame
from pygame.locals import *
from backend.pokemon import Pokemon
import os
import json

class First_screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.button_tool = Rect()
        self.font = pygame.font.SysFont("Arial", 30)

        self.pokemons = self.load_pokedex_from_json()
        self.ennemi = self.load_ennemi_from_json()
        self.moving_index = None


        self.bg = pygame.image.load("assets/sprites/poke_bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1920, 1000))
        self.bg_pokedex = pygame.image.load("assets/sprites/bg_pokedex.png").convert_alpha()
        self.bg_pokedex = pygame.transform.scale(self.bg_pokedex,(1920, 1000))
        
        self.state = "MENU"
        self.selected_index = 0
        self.buttons_count = 4

    def load_pokedex_from_json(self):
        with open ("data/pokemon.json", "r", encoding="utf-8") as f:
            all_pokemons_data = json.load(f)
        
        data_by_id = {p["id"]: p for p in all_pokemons_data}

        save_path = "data/save.json"
        if not os.path.exists(save_path):
            owned_ids = [1]
            with open (save_path, "w") as f:
                json.dump(owned_ids, f)
        else : 
            with open (save_path, "r") as f:
                owned_ids = json.load(f)

        owned_pokemons = []
        for p_id in owned_ids:
            if p_id in data_by_id:
                p_data = data_by_id[p_id]
                new_poke = Pokemon(
                p_data["name"], 
                p_data["hp"], 
                p_data["level"], 
                p_data["attack"], 
                p_data["defense"], 
                p_data["type"]
            )
                new_poke.id = p_id
                owned_pokemons.append(new_poke)
    
        return owned_pokemons
    
    def load_ennemi_from_json(self):
        with open ("data/pokemon.json", "r", encoding="utf-8") as f:
            all_pokemons_data = json.load(f)
        
        data_by_id = {p["id"]: p for p in all_pokemons_data}

        save_path = "data/ennemi.json"
        if not os.path.exists(save_path):
            owned_ids = [1]
            with open (save_path, "w") as f:
                json.dump(owned_ids, f)
        else : 
            with open (save_path, "r") as f:
                owned_ids = json.load(f)

        ennemi_pokemons = []
        for p_id in owned_ids:
            if p_id in data_by_id:
                p_data = data_by_id[p_id]
                new_poke = Pokemon(
                p_data["name"], 
                p_data["hp"], 
                p_data["level"], 
                p_data["attack"], 
                p_data["defense"], 
                p_data["type"]
            )
                new_poke.id = p_id
                ennemi_pokemons.append(new_poke)
    
        return ennemi_pokemons
    
    def save_current_order(self):
        owned_ids = [poke.id for poke in self.pokemons]
        with open("data/save.json", "w") as f:
            json.dump(owned_ids, f)
    
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
                            self.state == "ENNEMI"
                        elif self.selected_index == 3:
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
                            self.save_current_order()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        self.moving_index = None

                elif self.state == "ENNEMI":
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
                            self.save_current_order()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        self.moving_index = None

    def draw(self):
        self.screen.fill((30, 30, 30))

        if self.state == "MENU":
            self.screen.blit(self.bg, (0, 0))
            self.button_tool.draw_buttons(self.screen, "JOUER", 860, 220, 200, 60, self.font, self.selected_index == 0)
            self.button_tool.draw_buttons(self.screen, "POKEDEX", 860, 350, 200, 60, self.font, self.selected_index == 1)
            self.button_tool.draw_buttons(self.screen, "QUIT", 860, 650, 200, 60, self.font, self.selected_index == 3, self.button_tool.danger_color)
            self.button_tool.draw_buttons(self.screen, "ENNEMI", 860, 500, 200, 60, self.font, self.selected_index == 2)
        
        elif self.state == "ENNEMI":
            self.screen.blit(self.bg_pokedex, (0, 0))
            max_visible = 5

            start_index = max(0, self.selected_index - max_visible // 2)
            end_index = min(len(self.ennemi), start_index + max_visible)
            if end_index - start_index < max_visible:
                start_index = max(0, end_index - max_visible)

            for relative_i, i in enumerate(range(start_index, end_index)):
                poke = self.ennemi[i]
                y_pos = 350 + (relative_i * 100)
                is_selected = (i == self.selected_index)
                current_color = (200, 150, 0) if i == self.moving_index else None

                self.button_tool.draw_buttons(
                    self.screen, poke.name, 750, y_pos, 400, 80,
                    self.font, is_selected, current_color
                )

                if is_selected:
                    try:
                        sprite = pygame.image.load(poke.sprite_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (300, 300))
                        self.screen.blit(sprite, (200, 300)) 
                        
                        stats = f"HP: {poke.hp} | ATK: {poke.attack} | DEF: {poke.defense} TYPE : {poke.type}"
                        txt_surf = self.font.render(stats, True, (255, 255, 255))
                        self.screen.blit(txt_surf, (150, 720))
                    except:
                        error_txt = self.font.render("Image non trouvée", True, (255, 0, 0))
                        self.screen.blit(error_txt, (200, 400))

        
        elif self.state == "POKEDEX":
            self.screen.blit(self.bg_pokedex, (0, 0))
            max_visible = 5

            start_index = max(0, self.selected_index - max_visible // 2)
            end_index = min(len(self.pokemons), start_index + max_visible)
            if end_index - start_index < max_visible:
                start_index = max(0, end_index - max_visible)

            for relative_i, i in enumerate(range(start_index, end_index)):
                poke = self.pokemons[i]
                y_pos = 350 + (relative_i * 100)
                is_selected = (i == self.selected_index)
                current_color = (200, 150, 0) if i == self.moving_index else None

                self.button_tool.draw_buttons(
                    self.screen, poke.name, 750, y_pos, 400, 80,
                    self.font, is_selected, current_color
                )

                if is_selected:
                    try:
                        sprite = pygame.image.load(poke.sprite_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (300, 300))
                        self.screen.blit(sprite, (200, 300)) 
                        
                        stats = f"HP: {poke.hp} | ATK: {poke.attack} | DEF: {poke.defense} TYPE : {poke.type}"
                        txt_surf = self.font.render(stats, True, (255, 20, 20))
                        self.screen.blit(txt_surf, (80, 720))
                    except:
                        error_txt = self.font.render("Image non trouvée", True, (255, 0, 0))
                        self.screen.blit(error_txt, (200, 400))
            
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
        self.default_accent = (20, 150, 140)

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