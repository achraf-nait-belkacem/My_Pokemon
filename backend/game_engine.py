import json
import os
import random
import sys
import ctypes

import pygame

from backend.combat import Combat
from backend.data_manager import DataManager
from backend.pokemon import Pokemon
from config.colors import COLORS
from config.game_balance import calculate_xp_gain
from frontend.first_screen import First_screen
from frontend.loading import Loading_menu
from frontend.utils import Rect
from SpriteAnimation import PokemonSprite


if sys.platform == "win32":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class BattleScene:
    def __init__(self, screen, clock, db, pokedex_dict, colors, ui_rect_tool, font_btn, font_ui, font_lg, background):
        self.screen = screen
        self.clock = clock
        self.db = db
        self.pokedex_dict = pokedex_dict
        self.colors = colors
        self.ui_rect_tool = ui_rect_tool
        self.font_btn = font_btn
        self.font_ui = font_ui
        self.font_lg = font_lg
        self.background = background

    def _spawn_ennemi(self, ennemis_possibles):
        original = random.choice(ennemis_possibles)
        e = Pokemon(original.name, original.base_hp, random.randint(3, 8),
                    original.base_attack, original.base_defense, original.type)
        e.id = original.id
        e.update_sprite()
        e.recalc_stats()
        e.hp = e.max_hp
        e.processed = False
        return e

    def _init_battle(self, data):
        self.battle_running = True
        self.next_state = "MENU"
        self.equipe = data["Equipe"][:6]
        self.ennemis_possibles = data["Ennemis possibles"]
        for p in self.equipe:
            if hasattr(p, 'recalc_stats'):
                p.recalc_stats()
        self.mon_pkm = next((p for p in self.equipe if p.hp > 0), self.equipe[0])
        self.adversaire = self._spawn_ennemi(self.ennemis_possibles)
        self.p_sprite = PokemonSprite(self.mon_pkm.sprite_path, (450, 550))
        self.e_sprite = PokemonSprite(self.adversaire.sprite_path, (1350, 250))
        self.combat = Combat(self.mon_pkm, self.adversaire)
        self.state = {"idx": 0, "conf": 1, "team": 0, "show_conf": False, "show_team": False, "wait": 0, "msg": ""}
        self.actions = ["ATTAQUER", "EQUIPE", "FUITE"]

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.battle_running = False
                self.next_state = "QUIT"
            if event.type == pygame.KEYDOWN:
                if self.state["show_team"]:
                    self._handle_team_input(event)
                elif self.state["show_conf"]:
                    self._handle_conf_input(event)
                else:
                    self._handle_main_input(event)

    def _handle_main_input(self, event):
        if self.mon_pkm.is_alive() and self.adversaire.is_alive() and self.state["wait"] == 0:
            if event.key == pygame.K_LEFT:
                self.state["idx"] = (self.state["idx"] - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.state["idx"] = (self.state["idx"] + 1) % 3
            elif event.key == pygame.K_RETURN:
                act = self.actions[self.state["idx"]]
                if act == "ATTAQUER":
                    self.p_sprite.set_state("attack")
                    self.combat.attack(self.mon_pkm, self.adversaire)
                    self.e_sprite.set_state("hit")
                    self.state["wait"] = 80
                elif act == "EQUIPE":
                    self.state["show_team"] = True
                elif act == "FUITE":
                    self.state["show_conf"] = True
        elif not self.adversaire.is_alive() and event.key == pygame.K_RETURN:
            self._reset_battle()

    def _handle_team_input(self, event):
        if event.key == pygame.K_UP:
            self.state["team"] = (self.state["team"] - 1) % len(self.equipe)
        elif event.key == pygame.K_DOWN:
            self.state["team"] = (self.state["team"] + 1) % len(self.equipe)
        elif event.key == pygame.K_ESCAPE and self.mon_pkm.is_alive():
            self.state["show_team"] = False
        elif event.key == pygame.K_RETURN:
            new_p = self.equipe[self.state["team"]]
            if new_p.is_alive():
                self.mon_pkm = new_p
                self.p_sprite = PokemonSprite(self.mon_pkm.sprite_path, (450, 550))
                self.combat.player_pokemon = self.mon_pkm
                self.state["show_team"], self.state["wait"] = False, 0

    def _handle_conf_input(self, event):
        if event.key == pygame.K_LEFT:
            self.state["conf"] = 0
        elif event.key == pygame.K_RIGHT:
            self.state["conf"] = 1
        elif event.key == pygame.K_RETURN:
            if self.state["conf"] == 0:
                for p in self.equipe:
                    p.hp = p.max_hp
                self.db.save_team(self.equipe)
                self.battle_running = False
            else:
                self.state["show_conf"] = False

    def _reset_battle(self):
        self.adversaire = self._spawn_ennemi(self.ennemis_possibles)
        self.e_sprite = PokemonSprite(self.adversaire.sprite_path, (1350, 250))
        self.combat.enemy_pokemon = self.adversaire
        self.state["msg"] = ""

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
        level_ups = []
        for pkm in self.equipe:
            if pkm.is_alive():
                is_active = (pkm == self.mon_pkm)
                xp_gain = calculate_xp_gain(self.adversaire.lvl, is_active)
                if pkm.gain_xp(xp_gain):
                    level_ups.append(f"{pkm.name} Nv.{pkm.lvl}")
                    pkm_data = self.pokedex_dict.get(pkm.id)
                    if pkm_data and pkm_data.get("evolution"):
                        evo = pkm_data["evolution"]
                        if pkm.lvl >= evo["level"] and pkm.name != evo["next_form"]:
                            if pkm.evolve(evo):
                                if pkm == self.mon_pkm:
                                    self.p_sprite = PokemonSprite(pkm.sprite_path, (450, 550))
                                print(f"Félicitations ! {pkm_data['name']} a évolué en {pkm.name} !")
        self.adversaire.processed = True
        self.db.add_to_save(self.adversaire)
        active_xp = calculate_xp_gain(self.adversaire.lvl, is_active_pokemon=True)
        self.state["msg"] = f"UP: {', '.join(level_ups)}" if level_ups else f"{self.mon_pkm.name} gagne {active_xp} XP"
        self.db.save_team(self.equipe)

    def _draw_team_bar(self, pokemons, x, y):
        if not pokemons:
            return
        box_size = 20
        spacing = 6
        for idx, p in enumerate(pokemons):
            rect_x = x + idx * (box_size + spacing)
            rect = pygame.Rect(rect_x, y, box_size, box_size)
            is_alive = getattr(p, "is_alive", None)
            alive = is_alive() if callable(is_alive) else getattr(p, "hp", 0) > 0
            color = self.colors["hp_green"] if alive else self.colors["hp_red"]
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            pygame.draw.rect(self.screen, self.colors["black"], rect, 2, border_radius=4)

    def _render_all(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.colors["bg_dark"])
        self.p_sprite.draw(self.screen)
        self.e_sprite.draw(self.screen)
        if self.mon_pkm.is_alive():
            self.ui_rect_tool.draw_pokemon_stats(self.screen, self.mon_pkm, 375, 750, self.font_ui)
        if self.adversaire.is_alive():
            self.ui_rect_tool.draw_pokemon_stats(self.screen, self.adversaire, 1275, 80, self.font_ui)
        # team status bars (how many Pokémon left)
        self._draw_team_bar(self.equipe, 360, 720)
        self._draw_team_bar([self.adversaire], 1260, 50)
        if not self.adversaire.is_alive():
            txt = self.font_lg.render(f"{self.adversaire.name.upper()} VAINCU !", True, self.colors["victory"])
            self.screen.blit(txt, txt.get_rect(center=(960, 450)))
            if self.state["msg"]:
                l_txt = pygame.font.SysFont("Arial", 30).render(self.state["msg"], True, self.colors["white"])
                self.screen.blit(l_txt, l_txt.get_rect(center=(960, 500)))
        if self.state["show_team"]:
            self.ui_rect_tool.draw_team_menu(self.screen, self.equipe, self.mon_pkm, self.state["team"], self.font_btn, self.font_ui)
        elif self.state["show_conf"]:
            self.ui_rect_tool.draw_confirm_popup(self.screen, "Voulez-vous fuir ?", self.state["conf"], self.font_btn)
        elif self.mon_pkm.is_alive() and self.adversaire.is_alive() and self.state["wait"] == 0:
            for i, label in enumerate(self.actions):
                self.ui_rect_tool.draw_buttons(self.screen, label, 700 + i * 350, 800, 300, 80, self.font_btn, i == self.state["idx"])

    def play_battle(self, data):
        self._init_battle(data)
        while self.battle_running:
            self.clock.tick(60)
            self._handle_events()
            self._update_logic()
            self._render_all()
            pygame.display.flip()
        return self.next_state


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1000))
        pygame.display.set_caption("My_Pokemon")
        self.clock = pygame.time.Clock()
        self.ui_rect_tool = Rect()
        self.db = DataManager()
        self.pokedex_dict = self._load_pokedex_data()
        self.colors = COLORS  
        self.font_btn = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_lg = pygame.font.SysFont("Arial", 40, bold=True)
        self.background = self._load_background()
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
        except Exception:
            return {}

    def play_battle(self, data):
        scene = BattleScene(
            self.screen, self.clock, self.db, self.pokedex_dict, self.colors,
            self.ui_rect_tool, self.font_btn, self.font_ui, self.font_lg, self.background
        )
        return scene.play_battle(data)

    def run(self):
        Loading_menu(self.screen).run()
        state = "MENU"
        while state != "QUIT":
            if state == "MENU":
                data = First_screen(self.screen).run()
                state = "COMBAT" if data and data != "QUIT" else "QUIT"
            elif state == "COMBAT": 
                state = self.play_battle(data)
        pygame.quit()