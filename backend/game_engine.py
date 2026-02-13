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
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((1920, 1000))
        pygame.display.set_caption("My_Pokemon")
        self.clock = pygame.time.Clock()
        
        # Outils et gestion des données
        self.ui_rect_tool = Rect()
        self.db = DataManager()
        
        # Polices
        self.font_button = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 22, bold=True)
        
        # Chargement des données globales
        self.pokedex_dict = self._load_pokedex_data()

    def _load_pokedex_data(self):
        """Charge les données du Pokédex pour gérer les évolutions."""
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pokemon.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {p["id"]: p for p in data}
        except Exception as e:
            print(f"Erreur chargement pokedex: {e}")
            return {}

    def draw_ui(self, pokemon, x, y):
        """Affiche le nom, le niveau et la barre de PV d'un Pokémon."""
        # Nom et Niveau
        txt_header = self.font_ui.render(f"{pokemon.name.upper()}  Nv. {pokemon.lvl}", True, (255, 255, 255))
        self.screen.blit(txt_header, (x, y))
        
        # Barre de PV (Fond noir)
        pygame.draw.rect(self.screen, (30, 30, 30), (x, y + 30, 250, 8))
        
        # Calcul de la largeur de la barre de vie
        ratio = min(1.0, pokemon.hp / pokemon.max_hp if pokemon.max_hp > 0 else 0)
        color = (0, 255, 127) if ratio > 0.5 else (255, 165, 0) if ratio > 0.2 else (255, 50, 50)
        pygame.draw.rect(self.screen, color, (x, y + 30, int(250 * ratio), 8))
        
        # Texte des PV
        txt_pv = self.font_ui.render(f"{max(0, int(pokemon.hp))} / {pokemon.max_hp}", True, (255, 255, 255))
        self.screen.blit(txt_pv, txt_pv.get_rect(center=(x + 125, y + 50)))

    def draw_confirm_popup(self, text, selected_index):
        """Affiche une fenêtre de confirmation (Oui/Non)."""
        overlay = pygame.Surface((1920, 1000), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        self.screen.blit(overlay, (0, 0))
        
        box_rect = pygame.Rect(660, 350, 600, 300)
        pygame.draw.rect(self.screen, (45, 45, 65), box_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 3, border_radius=15)
        
        msg = pygame.font.SysFont("Arial", 35, bold=True).render(text, True, (255, 255, 255))
        self.screen.blit(msg, msg.get_rect(center=(960, 420)))
        
        self.ui_rect_tool.draw_buttons(self.screen, "OUI", 710, 520, 200, 60, self.font_button, selected_index == 0)
        self.ui_rect_tool.draw_buttons(self.screen, "NON", 1010, 520, 200, 60, self.font_button, selected_index == 1)

    def play_battle(self, data):
        """Boucle principale de la scène de combat."""
        equipe = data["Equipe"][:6]
        for p in equipe:
            if hasattr(p, 'recalc_stats'): p.recalc_stats()
        
        mon_pkm = next((p for p in equipe if p.hp > 0), equipe[0])
        
        def get_new_ennemi():
            modele = random.choice(data["Ennemis possibles"])
            if hasattr(modele, 'recalc_stats'): modele.recalc_stats()
            modele.hp = modele.max_hp
            modele.processed = False 
            return modele

        adversaire = get_new_ennemi()
        joueur_sprite = PokemonSprite(mon_pkm.sprite_path, (500, 650))
        ennemi_sprite = PokemonSprite(adversaire.sprite_path, (1400, 300))
        combat_moteur = Combat(mon_pkm, adversaire)
        
        actions = ["ATTAQUER", "EQUIPE", "FUITE"]
        action_idx, confirm_idx, team_idx = 0, 1, 0
        show_confirm, show_team = False, False
        turn_wait = 0 
        level_up_msg = ""

        while True:
            self.clock.tick(60)
            self.screen.fill((30, 30, 40)) 
            equipe_vivante = any(p.hp > 0 for p in equipe)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                
                if event.type == pygame.KEYDOWN:
                    if not equipe_vivante:
                        if event.key == pygame.K_RETURN: return "MENU"
                        continue

                    # Gestion du menu d'équipe (Switch)
                    if show_team:
                        if event.key == pygame.K_UP: team_idx = (team_idx - 1) % len(equipe)
                        elif event.key == pygame.K_DOWN: team_idx = (team_idx + 1) % len(equipe)
                        elif event.key == pygame.K_ESCAPE and mon_pkm.is_alive(): show_team = False
                        elif event.key == pygame.K_RETURN:
                            nouveau = equipe[team_idx]
                            if nouveau != mon_pkm and nouveau.hp > 0:
                                mon_pkm = nouveau
                                joueur_sprite = PokemonSprite(mon_pkm.sprite_path, (500, 650))
                                combat_moteur.player_pokemon = mon_pkm 
                                show_team, turn_wait = False, 40 
                        continue

                    # Gestion de la confirmation de fuite
                    if show_confirm:
                        if event.key == pygame.K_LEFT: confirm_idx = 0
                        elif event.key == pygame.K_RIGHT: confirm_idx = 1
                        if event.key == pygame.K_RETURN:
                            if confirm_idx == 0:
                                for p in equipe: p.hp = p.max_hp # Soin à la fuite
                                self.db.save_team(equipe)
                                return "MENU"
                            else: show_confirm = False
                        continue

                    # Actions de combat standards
                    if mon_pkm.is_alive() and adversaire.is_alive():
                        if turn_wait == 0:
                            if event.key == pygame.K_LEFT: action_idx = (action_idx - 1) % 3
                            elif event.key == pygame.K_RIGHT: action_idx = (action_idx + 1) % 3
                            if event.key == pygame.K_RETURN:
                                if actions[action_idx] == "ATTAQUER":
                                    joueur_sprite.set_state("attack")
                                    combat_moteur.attack(mon_pkm, adversaire)
                                    ennemi_sprite.set_state("hit")
                                    turn_wait = 80
                                elif actions[action_idx] == "EQUIPE":
                                    show_team, team_idx = True, equipe.index(mon_pkm)
                                elif actions[action_idx] == "FUITE":
                                    show_confirm, confirm_idx = True, 1
                    
                    # Passer au prochain ennemi si vaincu
                    elif not adversaire.is_alive() and event.key == pygame.K_RETURN:
                        adversaire = get_new_ennemi()
                        ennemi_sprite = PokemonSprite(adversaire.sprite_path, (1400, 300))
                        combat_moteur.enemy_pokemon = adversaire
                        level_up_msg, turn_wait = "", 0

            # --- Logique post-attaque et XP ---
            if not adversaire.is_alive() and not getattr(adversaire, 'processed', False):
                nom_avant = mon_pkm.name
                if combat_moteur.gain_xp(mon_pkm, adversaire):
                    level_up_msg = f"LEVEL UP ! {mon_pkm.name} est Nv. {mon_pkm.lvl}"
                    p_data = self.pokedex_dict.get(mon_pkm.id)
                    if p_data and "evolution" in p_data:
                        if mon_pkm.evolve(p_data["evolution"]):
                            level_up_msg = f"EVOLUTION ! {nom_avant} -> {mon_pkm.name}"
                            joueur_sprite = PokemonSprite(mon_pkm.sprite_path, (500, 650))
                self.db.save_team(equipe)
                self.db.add_to_save(adversaire)
                adversaire.processed = True

            # Attaque de l'adversaire (délai)
            if not show_confirm and not show_team and turn_wait > 0:
                turn_wait -= 1
                if turn_wait == 40 and adversaire.is_alive() and mon_pkm.is_alive():
                    ennemi_sprite.set_state("attack")
                    combat_moteur.attack(adversaire, mon_pkm)
                    joueur_sprite.set_state("hit")

            # --- Affichage ---
            joueur_sprite.update()
            ennemi_sprite.update()
            joueur_sprite.draw(self.screen)
            ennemi_sprite.draw(self.screen)
            
            if mon_pkm.is_alive(): self.draw_ui(mon_pkm, 375, 790)
            if adversaire.is_alive(): self.draw_ui(adversaire, 1275, 80)

            # Interface de sélection
            if mon_pkm.is_alive() and adversaire.is_alive() and not show_confirm and not show_team:
                for i, label in enumerate(actions):
                    self.ui_rect_tool.draw_buttons(self.screen, label, 550 + i * 350, 850, 300, 80, self.font_button, i == action_idx)
            
            # Messages d'état (Game Over / Victoire)
            if not equipe_vivante:
                txt = pygame.font.SysFont("Arial", 60, bold=True).render("GAME OVER", True, (255, 50, 50))
                self.screen.blit(txt, txt.get_rect(center=(960, 500)))
            elif not mon_pkm.is_alive():
                txt = pygame.font.SysFont("Arial", 40, bold=True).render("Sélectionnez un autre Pokémon", True, (255, 100, 100))
                self.screen.blit(txt, txt.get_rect(center=(960, 500)))
            elif not adversaire.is_alive():
                txt = pygame.font.SysFont("Arial", 40, bold=True).render(f"{adversaire.name.upper()} VAINCU !", True, (0, 255, 127))
                self.screen.blit(txt, txt.get_rect(center=(960, 450)))
                if level_up_msg:
                    lvl_txt = pygame.font.SysFont("Arial", 30, bold=True).render(level_up_msg, True, (255, 255, 255))
                    self.screen.blit(lvl_txt, lvl_txt.get_rect(center=(960, 510)))

            if show_team:
                pygame.draw.rect(self.screen, (35, 35, 55), (710, 150, 500, 650), border_radius=15)
                for i, p in enumerate(equipe):
                    self.ui_rect_tool.draw_buttons(self.screen, f"{p.name} ({int(p.hp)} HP)", 760, 200 + (i * 85), 400, 70, self.font_button, i == team_idx)
            
            if show_confirm: self.draw_confirm_popup("Voulez-vous fuir ?", confirm_idx)
            
            pygame.display.flip()

    def run(self):
        """Lance l'application et gère la transition entre les menus."""
        Loading_menu(self.screen).run()
        state = "MENU"
        while state != "QUIT":
            if state == "MENU":
                data = First_screen(self.screen).run()
                state = "COMBAT" if data and data != "QUIT" else "QUIT"
            elif state == "COMBAT":
                state = self.play_battle(data)
        pygame.quit()