import pygame
from pygame.locals import QUIT

from backend.data_manager import DataManager
from frontend.utils import Rect
class First_screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.button_tool = Rect()
        self.font = pygame.font.SysFont("Arial", 30)
        self.font_small = pygame.font.SysFont("Arial", 20, bold=True)
        self.db = DataManager()
        self.pokemons = self.db.load_pokedex()
        self.ennemi = self.db.load_all_ennemi()
        self.moving_index = None
        self.selected_ennemi_ids = [p.id for p in self.ennemi]
        self.bg = pygame.transform.scale(pygame.image.load("assets/sprites/backgrounds/poke_bg.png").convert_alpha(), (1920, 1000))
        self.bg_pokedex = pygame.transform.scale(pygame.image.load("assets/sprites/backgrounds/bg_pokedex.png").convert_alpha(), (1920, 1000))
        self.bg_workshop = pygame.transform.scale(pygame.image.load("assets/sprites/backgrounds/workshop.png").convert_alpha(), (1920, 1000))
        self.state = "MENU"
        self.selected_index = 0
        self.buttons_count = 4
        self.replace_ko_phase = "select_slot"  # "select_slot" | "select_replacement"
        self.replace_ko_slot = 0
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
                            team = self.pokemons[:6]
                            ko_in_team = [i for i, p in enumerate(team) if not p.is_alive()]
                            if ko_in_team:
                                self.state = "REPLACE_KO"
                                self.replace_ko_phase = "select_slot"
                                self.replace_ko_slot = ko_in_team[0]
                                self.selected_index = self.replace_ko_slot
                            else:
                                if not self.selected_ennemi_ids:
                                    self.selected_ennemi_ids = [p.id for p in self.ennemi]
                                return {
                                    "Equipe": self.pokemons[:6],
                                    "Ennemis possibles": [p for p in self.ennemi if p.id in self.selected_ennemi_ids]
                                }
                        elif self.selected_index == 1: 
                            self.state = "POKEDEX"
                            self.selected_index = 0
                        elif self.selected_index == 2: 
                            self.state = "ENNEMI"
                            self.selected_index = 0
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
                        self.selected_index = 1
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
                        self.selected_index = 2
                elif self.state == "REPLACE_KO":
                    if self.replace_ko_phase == "select_slot":
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % 6
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % 6
                        elif event.key == pygame.K_RETURN:
                            if not self.pokemons[self.selected_index].is_alive():
                                self.replace_ko_slot = self.selected_index
                                self.replace_ko_phase = "select_replacement"
                                self._replacement_list = [(i, p) for i, p in enumerate(self.pokemons) if i >= 6 and p.is_alive()]
                                self.selected_index = 0 if self._replacement_list else 0
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                            self.selected_index = 0
                    elif self.replace_ko_phase == "select_replacement":
                        repl = getattr(self, "_replacement_list", [])
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % max(1, len(repl))
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % max(1, len(repl))
                        elif event.key == pygame.K_RETURN and repl:
                            _, replacement_pokemon = repl[self.selected_index]
                            repl_idx = repl[self.selected_index][0]
                            self.pokemons[self.replace_ko_slot], self.pokemons[repl_idx] = self.pokemons[repl_idx], self.pokemons[self.replace_ko_slot]
                            self.db.save_team(self.pokemons)
                            ko_left = [i for i in range(6) if not self.pokemons[i].is_alive()]
                            if ko_left:
                                self.replace_ko_phase = "select_slot"
                                self.replace_ko_slot = ko_left[0]
                                self.selected_index = self.replace_ko_slot
                            else:
                                self.state = "MENU"
                                self.selected_index = 0
                        elif event.key == pygame.K_ESCAPE:
                            self.replace_ko_phase = "select_slot"
                            self.selected_index = self.replace_ko_slot
                            self._replacement_list = []
        return None
    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.state == "MENU":
            self.screen.blit(self.bg, (0, 0))
            self.button_tool.draw_buttons(self.screen, "JOUER", 860, 220, 200, 60, self.font, self.selected_index == 0)
            self.button_tool.draw_buttons(self.screen, "POKEDEX", 860, 350, 200, 60, self.font, self.selected_index == 1)
            self.button_tool.draw_buttons(self.screen, "ENNEMI", 860, 500, 200, 60, self.font, self.selected_index == 2)
            self.button_tool.draw_buttons(self.screen, "QUIT", 860, 650, 200, 60, self.font, self.selected_index == 3, (255, 50, 50))
        elif self.state == "REPLACE_KO":
            self.screen.blit(self.bg_workshop, (0, 0))
            # Dark rectangle behind title text for readability
            title_rect = pygame.Rect(380, 100, 1160, 95)
            pygame.draw.rect(self.screen, (40, 40, 55), title_rect, border_radius=10)
            pygame.draw.rect(self.screen, (80, 80, 100), title_rect, 2, border_radius=10)
            msg = self.font.render("Des Pokémon sont K.O. Remplacez-les pour continuer.", True, (255, 255, 255))
            self.screen.blit(msg, (400, 115))
            sub = pygame.font.SysFont("Arial", 22).render("Sélectionnez un slot K.O. (Entrée), puis choisissez un remplaçant. ESC = annuler.", True, (220, 220, 220))
            self.screen.blit(sub, (400, 155))
            if self.replace_ko_phase == "select_slot":
                for i in range(min(6, len(self.pokemons))):
                    p = self.pokemons[i]
                    y_pos = 250 + i * 90
                    label = f"Slot {i+1}: {p.name} (Nv.{p.lvl})" + (" — K.O." if not p.is_alive() else "")
                    color = (255, 80, 80) if not p.is_alive() else (80, 200, 80)
                    self.button_tool.draw_buttons(self.screen, label, 400, y_pos, 500, 75, self.font, self.selected_index == i, color)
            else:
                repl = getattr(self, "_replacement_list", [])
                for idx, (_, p) in enumerate(repl):
                    y_pos = 250 + idx * 90
                    label = f"{p.name} (Nv.{p.lvl}) — HP: {int(p.hp)}/{p.max_hp}"
                    self.button_tool.draw_buttons(self.screen, label, 400, y_pos, 500, 75, self.font, self.selected_index == idx)
                if not repl:
                    no_repl = pygame.font.SysFont("Arial", 26).render("Aucun autre Pokémon valide. Allez au Pokedex pour en soigner.", True, (255, 200, 200))
                    self.screen.blit(no_repl, (400, 350))
        elif self.state in ["ENNEMI", "POKEDEX"]:
            self.screen.blit(self.bg_pokedex, (0, 0))
            liste = self.ennemi if self.state == "ENNEMI" else self.pokemons
            start_index = max(0, self.selected_index - 2)
            end_index = min(len(liste), start_index + 5)
            for relative_i, i in enumerate(range(start_index, end_index)):
                poke = liste[i]
                y_pos = 350 + (relative_i * 100)
                is_selected = (i == self.selected_index)
                color = None
                if self.state == "ENNEMI" and poke.id in self.selected_ennemi_ids:
                    color = (50, 200, 50)
                if i == self.moving_index:
                    color = (200, 150, 0)
                self.button_tool.draw_buttons(self.screen, poke.name, 750, y_pos, 400, 80, self.font, is_selected, color)
                if self.state == "POKEDEX" and i < 6:
                    txt_team = self.font_small.render("ÉQUIPE", True, (0, 255, 127))
                    self.screen.blit(txt_team, (1170, y_pos + 30))
                if self.state == "POKEDEX" and i == 5:
                    pygame.draw.line(self.screen, (255, 255, 255), (750, y_pos + 90), (1150, y_pos + 90), 2)
                if is_selected:
                    try:
                        sprite = pygame.image.load(poke.sprite_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (300, 300))
                        self.screen.blit(sprite, (200, 300)) 
                        stats = f"HP: {int(poke.hp)}/{poke.max_hp} | ATK: {poke.attack} | DEF: {poke.defense}"
                        self.screen.blit(self.font.render(stats, True, (255, 255, 255)), (80, 720))
                    except:
                        pass
        pygame.display.flip()
    def run(self):
        while self.running:
            result = self.handle_events()
            if result: return result
            self.draw()
            self.clock.tick(60)