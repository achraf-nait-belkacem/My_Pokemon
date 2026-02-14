import pygame
import random
import os
import json
from SpriteAnimation import PokemonSprite
from frontend.loading import Loading_menu
from frontend.first_screen import First_screen
from backend.combat import Combat
from frontend.utils import Rect 
from backend.data_manager import DataManager

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1000))
        pygame.display.set_caption("My_Pokemon")
        self.clock = pygame.time.Clock()
        self.ui_rect_tool = Rect() # Ta classe dans frontend/utils.py
        self.db = DataManager()
        self.pokedex_dict = self._load_pokedex_data()
        
        # Configuration Visuelle
        self.colors = {
            "white": (255, 255, 255), "shadow": (40, 40, 40),
            "bg_dark": (30, 30, 40), "hp_green": (0, 255, 127),
            "hp_yellow": (255, 215, 0), "hp_red": (255, 69, 0),
            "victory": (0, 255, 127), "alert": (255, 80, 80),
            "overlay": (0, 0, 0, 180), "panel": (35, 35, 55)
        }
        self.font_btn = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_lg = pygame.font.SysFont("Arial", 40, bold=True)
        self.background = self._load_background()

    # --- Chargement & Utilitaires ---
    def _load_background(self):
        path = os.path.join("assets/sprites", "battle_bg.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert()
            return pygame.transform.scale(img, (1920, 1000))
        return None

    def _load_pokedex_data(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_path, "data", "pokemon.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return {p["id"]: p for p in json.load(f)}
        except Exception: return {}

    def _spawn_ennemi(self, ennemis_possibles):
        e = random.choice(ennemis_possibles)
        e.recalc_stats()
        e.hp, e.processed = e.max_hp, False
        return e

    # --- Initialisation du Combat ---
    def _init_battle(self, data):
        self.battle_running = True
        self.next_state = "MENU"
        self.equipe = data["Equipe"][:6]
        self.ennemis_possibles = data["Ennemis possibles"]
        
        for p in self.equipe: 
            if hasattr(p, 'recalc_stats'): p.recalc_stats()
            
        self.mon_pkm = next((p for p in self.equipe if p.hp > 0), self.equipe[0])
        self.adversaire = self._spawn_ennemi(self.ennemis_possibles)
        
        self.p_sprite = PokemonSprite(self.mon_pkm.sprite_path, (450, 550))
        self.e_sprite = PokemonSprite(self.adversaire.sprite_path, (1350, 250))
        self.combat = Combat(self.mon_pkm, self.adversaire)
        
        self.state = {"idx": 0, "conf": 1, "team": 0, "show_conf": False, "show_team": False, "wait": 0, "msg": ""}
        self.actions = ["ATTAQUER", "EQUIPE", "FUITE"]

    # --- Gestion des Entrées (Input) ---
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.battle_running = False
                self.next_state = "QUIT"
            
            if event.type == pygame.KEYDOWN:
                if self.state["show_team"]: self._handle_team_input(event)
                elif self.state["show_conf"]: self._handle_conf_input(event)
                else: self._handle_main_input(event)

    def _handle_main_input(self, event):
        if self.mon_pkm.is_alive() and self.adversaire.is_alive() and self.state["wait"] == 0:
            if event.key == pygame.K_LEFT: self.state["idx"] = (self.state["idx"] - 1) % 3
            elif event.key == pygame.K_RIGHT: self.state["idx"] = (self.state["idx"] + 1) % 3
            elif event.key == pygame.K_RETURN:
                act = self.actions[self.state["idx"]]
                if act == "ATTAQUER":
                    self.p_sprite.set_state("attack")
                    self.combat.attack(self.mon_pkm, self.adversaire)
                    self.e_sprite.set_state("hit")
                    self.state["wait"] = 80
                elif act == "EQUIPE": self.state["show_team"] = True
                elif act == "FUITE": self.state["show_conf"] = True
        
        elif not self.adversaire.is_alive() and event.key == pygame.K_RETURN:
            self._reset_battle()

    def _handle_team_input(self, event):
        if event.key == pygame.K_UP: self.state["team"] = (self.state["team"] - 1) % len(self.equipe)
        elif event.key == pygame.K_DOWN: self.state["team"] = (self.state["team"] + 1) % len(self.equipe)
        elif event.key == pygame.K_ESCAPE and self.mon_pkm.is_alive(): self.state["show_team"] = False
        elif event.key == pygame.K_RETURN:
            new_p = self.equipe[self.state["team"]]
            if new_p.is_alive():
                self.mon_pkm = new_p
                self.p_sprite = PokemonSprite(self.mon_pkm.sprite_path, (450, 550))
                self.combat.player_pokemon = self.mon_pkm
                self.state["show_team"], self.state["wait"] = False, 0

    def _handle_conf_input(self, event):
        if event.key == pygame.K_LEFT: self.state["conf"] = 0
        elif event.key == pygame.K_RIGHT: self.state["conf"] = 1
        elif event.key == pygame.K_RETURN:
            if self.state["conf"] == 0:
                for p in self.equipe: p.hp = p.max_hp
                self.db.save_team(self.equipe)
                self.battle_running = False
            else: self.state["show_conf"] = False

    def _reset_battle(self):
        self.adversaire = self._spawn_ennemi(self.ennemis_possibles)
        self.e_sprite = PokemonSprite(self.adversaire.sprite_path, (1350, 250))
        self.combat.enemy_pokemon = self.adversaire
        self.state["msg"] = ""

    # --- Logique de Mise à Jour ---
    def _update_logic(self):
        self.p_sprite.update()
        self.e_sprite.update()
        
        if not self.adversaire.is_alive() and not getattr(self.adversaire, 'processed', False):
            self._process_victory()

        if not self.state["show_conf"] and not self.state["show_team"] and self.state["wait"] > 0:
            self.state["wait"] -= 1
            if self.state["wait"] == 40 and self.adversaire.is_alive() and self.mon_pkm.is_alive():
                self.e_sprite.set_state("attack")
                self.combat.attack(self.adversaire, self.mon_pkm)
                self.p_sprite.set_state("hit")
        
        if not self.mon_pkm.is_alive() and not self.state["show_team"] and self.state["wait"] == 0:
            self.state["show_team"] = True
            self.state["team"] = self.equipe.index(self.mon_pkm)

    def _process_victory(self):
        base_xp = self.adversaire.lvl * 20 
        level_ups = []
        for pkm in self.equipe:
            if pkm.is_alive():
                gain = base_xp if pkm == self.mon_pkm else base_xp // 4
                if pkm.gain_xp(gain): level_ups.append(f"{pkm.name} Nv.{pkm.lvl}")
        
        self.state["msg"] = f"UP: {', '.join(level_ups)}" if level_ups else f"{self.mon_pkm.name} gagne {base_xp} XP"
        self.db.add_to_save(self.adversaire)
        self.db.save_team(self.equipe)
        self.adversaire.processed = True

    # --- Rendu Graphique (Délégué à self.ui_rect_tool) ---
    def _render_all(self):
        # Fond & Sprites
        if self.background: self.screen.blit(self.background, (0, 0))
        else: self.screen.fill(self.colors["bg_dark"])
        self.p_sprite.draw(self.screen)
        self.e_sprite.draw(self.screen)
        
        # UI Pokemons (Maintenant géré par Rect)
        if self.mon_pkm.is_alive(): 
            self.ui_rect_tool.draw_pokemon_stats(self.screen, self.mon_pkm, 375, 750, self.font_ui)
        if self.adversaire.is_alive(): 
            self.ui_rect_tool.draw_pokemon_stats(self.screen, self.adversaire, 1275, 80, self.font_ui)

        # Victoire Screen
        if not self.adversaire.is_alive():
            txt = self.font_lg.render(f"{self.adversaire.name.upper()} VAINCU !", True, self.colors["victory"])
            self.screen.blit(txt, txt.get_rect(center=(960, 450)))
            if self.state["msg"]:
                l_txt = pygame.font.SysFont("Arial", 30).render(self.state["msg"], True, self.colors["white"])
                self.screen.blit(l_txt, l_txt.get_rect(center=(960, 500)))

        # Menus & Boutons (Appels délégués au front)
        if self.state["show_team"]: 
            self.ui_rect_tool.draw_team_menu(self.screen, self.equipe, self.mon_pkm, self.state["team"], self.font_btn, self.font_ui)
        elif self.state["show_conf"]: 
            self.ui_rect_tool.draw_confirm_popup(self.screen, "Voulez-vous fuir ?", self.state["conf"], self.font_btn)
        elif self.mon_pkm.is_alive() and self.adversaire.is_alive() and self.state["wait"] == 0:
            for i, label in enumerate(self.actions):
                self.ui_rect_tool.draw_buttons(self.screen, label, 700 + i * 350, 800, 300, 80, self.font_btn, i == self.state["idx"])

    # --- Boucle Principale ---
    def play_battle(self, data):
        self._init_battle(data)
        while self.battle_running:
            self.clock.tick(60)
            self._handle_events()
            self._update_logic()
            self._render_all()
            pygame.display.flip()
        return self.next_state

    def run(self):
        Loading_menu(self.screen).run()
        state = "MENU"
        while state != "QUIT":
            if state == "MENU":
                data = First_screen(self.screen).run()
                state = "COMBAT" if data and data != "QUIT" else "QUIT"
            elif state == "COMBAT": state = self.play_battle(data)
        pygame.quit()