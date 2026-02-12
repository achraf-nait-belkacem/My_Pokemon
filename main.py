import pygame
import random
import sys
import os
from SpriteAnimation import PokemonSprite
from frontend.loading import Loading_menu
from frontend.first_screen import First_screen
from backend.combat import Combat
from frontend.utils import Rect 
from backend.data_manager import DataManager

# --- FONCTIONS UI ---

def draw_ui(screen, pokemon, x, y):
    font = pygame.font.SysFont("Arial", 22, bold=True)
    # On affiche le nom actuel (qui change lors de l'évolution)
    txt_header = font.render(f"{pokemon.name.upper()}  Nv. {pokemon.lvl}", True, (255, 255, 255))
    screen.blit(txt_header, (x, y))
    
    ratio = pokemon.hp / pokemon.max_hp if pokemon.max_hp > 0 else 0
    bar_width = 250
    pygame.draw.rect(screen, (30, 30, 30), (x, y + 30, bar_width, 8))
    color = (0, 255, 127) if ratio > 0.5 else (255, 165, 0) if ratio > 0.2 else (255, 50, 50)
    pygame.draw.rect(screen, color, (x, y + 30, int(bar_width * ratio), 8))
    
    txt_pv = font.render(f"{max(0, int(pokemon.hp))} / {pokemon.max_hp}", True, (255, 255, 255))
    screen.blit(txt_pv, txt_pv.get_rect(center=(x + bar_width // 2, y + 50)))

def draw_confirm_popup(screen, text, selected_index, ui_rect_tool, font_button):
    overlay = pygame.Surface((1920, 1000), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    screen.blit(overlay, (0, 0))
    box_rect = pygame.Rect(660, 350, 600, 300)
    pygame.draw.rect(screen, (45, 45, 65), box_rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, 3, border_radius=15)
    font_msg = pygame.font.SysFont("Arial", 35, bold=True)
    msg = font_msg.render(text, True, (255, 255, 255))
    screen.blit(msg, msg.get_rect(center=(960, 420)))
    ui_rect_tool.draw_buttons(screen, "OUI", 710, 520, 200, 60, font_button, selected_index == 0)
    ui_rect_tool.draw_buttons(screen, "NON", 1010, 520, 200, 60, font_button, selected_index == 1)

# --- LOGIQUE DE COMBAT ---

def play_battle(screen, data):
    clock = pygame.time.Clock()
    ui_rect_tool = Rect()
    db = DataManager()
    font_button = pygame.font.SysFont("Arial", 26, bold=True)

    equipe = data["Equipe"][:6] 
    for p in equipe:
        if hasattr(p, 'recalc_stats'):
            p.recalc_stats()

    mon_pkm = next((p for p in equipe if p.hp > 0), equipe[0])
    
    def get_new_ennemi():
        modele = random.choice(data["Ennemis possibles"])
        
        if not os.path.exists(modele.sprite_path):
            print(f"⚠️ Image manquante: {modele.sprite_path}. Utilisation du défaut.")
            modele.sprite_path = "assets/sprites/default.png"

        p_id = getattr(modele, 'id', 'AUCUN')
        print(f"DEBUG: Nouveau combat contre {modele.name} (ID: {p_id})")
        
        if hasattr(modele, 'recalc_stats'):
            modele.recalc_stats()
        modele.hp = modele.max_hp
        modele.processed = False 
        return modele

    adversaire = get_new_ennemi()
    joueur_sprite = PokemonSprite(mon_pkm.sprite_path, (500, 650), size=(200, 200))
    ennemi_sprite = PokemonSprite(adversaire.sprite_path, (1400, 300), size=(200, 200))
    
    combat_moteur = Combat(mon_pkm, adversaire)
    actions = ["ATTAQUER", "EQUIPE", "FUITE"]
    
    action_idx, confirm_idx, team_idx = 0, 1, 0
    show_confirm = False
    show_team = False   
    turn_wait = 0 
    level_up_msg = ""

    while True:
        clock.tick(60)
        screen.fill((30, 30, 40)) 
        equipe_vivante = any(p.hp > 0 for p in equipe)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                if not equipe_vivante:
                    if event.key == pygame.K_RETURN: return "MENU"
                    continue

                if not mon_pkm.is_alive() and adversaire.is_alive() and equipe_vivante:
                    show_team = True

                if show_team:
                    if event.key == pygame.K_UP: team_idx = (team_idx - 1) % len(equipe)
                    elif event.key == pygame.K_DOWN: team_idx = (team_idx + 1) % len(equipe)
                    elif event.key == pygame.K_ESCAPE and mon_pkm.is_alive(): show_team = False
                    elif event.key == pygame.K_RETURN:
                        nouveau = equipe[team_idx]
                        if nouveau != mon_pkm and nouveau.hp > 0:
                            mon_pkm = nouveau
                            joueur_sprite = PokemonSprite(mon_pkm.sprite_path, (500, 650), size=(200, 200))
                            combat_moteur.player_pokemon = mon_pkm 
                            show_team = False
                            turn_wait = 40 
                    continue

                if show_confirm:
                    if event.key == pygame.K_LEFT: confirm_idx = 0
                    if event.key == pygame.K_RIGHT: confirm_idx = 1
                    if event.key == pygame.K_RETURN:
                        if confirm_idx == 0: return "MENU"
                        else: show_confirm = False
                    continue

                if mon_pkm.is_alive() and adversaire.is_alive():
                    if turn_wait == 0:
                        if event.key == pygame.K_LEFT: action_idx = (action_idx - 1) % len(actions)
                        if event.key == pygame.K_RIGHT: action_idx = (action_idx + 1) % len(actions)
                        if event.key == pygame.K_RETURN:
                            chosen = actions[action_idx]
                            if chosen == "ATTAQUER":
                                joueur_sprite.set_state("attack")
                                combat_moteur.attack(mon_pkm, adversaire)
                                ennemi_sprite.set_state("hit")
                                turn_wait = 80
                            elif chosen == "EQUIPE":
                                show_team = True
                                team_idx = equipe.index(mon_pkm)
                            elif chosen == "FUITE":
                                show_confirm = True
                                confirm_idx = 1
                
                elif not adversaire.is_alive():
                    if event.key == pygame.K_RETURN:
                        adversaire = get_new_ennemi()
                        ennemi_sprite = PokemonSprite(adversaire.sprite_path, (1400, 300), size=(200, 200))
                        combat_moteur.enemy_pokemon = adversaire
                        level_up_msg = ""
                        turn_wait = 0

        # --- LOGIQUE DE VICTOIRE, ÉVOLUTION ET SAUVEGARDE ---
        if not adversaire.is_alive() and not getattr(adversaire, 'processed', False):
            print(f"Victoire contre {adversaire.name} (ID: {getattr(adversaire, 'id', 'Inconnu')})")
            
            # Stockage du nom avant gain d'XP pour détecter l'évolution
            nom_avant = mon_pkm.name
            
            if combat_moteur.gain_xp(mon_pkm, adversaire):
                level_up_msg = f"LEVEL UP ! {mon_pkm.name} est Nv. {mon_pkm.lvl}"
                
                # SI LE NOM A CHANGÉ -> ÉVOLUTION !
                if mon_pkm.name != nom_avant:
                    print(f"✨ ÉVOLUTION : {nom_avant} -> {mon_pkm.name}")
                    level_up_msg = f"INCROYABLE ! {nom_avant} devient {mon_pkm.name} !"
                    # Mise à jour immédiate du visuel
                    joueur_sprite = PokemonSprite(mon_pkm.sprite_path, (500, 650), size=(200, 200))
            
            # Sauvegarde de l'équipe (XP + Nouveau Nom)
            db.save_team(equipe)
            
            # Ajout de l'ennemi au pokedex (Capture)
            db.add_to_save(adversaire)
            
            adversaire.processed = True

        if not show_confirm and not show_team and turn_wait > 0:
            turn_wait -= 1
            if turn_wait == 40 and adversaire.is_alive() and mon_pkm.is_alive():
                ennemi_sprite.set_state("attack")
                combat_moteur.attack(adversaire, mon_pkm)
                joueur_sprite.set_state("hit")

        joueur_sprite.update()
        ennemi_sprite.update()
        joueur_sprite.draw(screen)
        ennemi_sprite.draw(screen)
        
        if mon_pkm.is_alive(): draw_ui(screen, mon_pkm, 375, 790)
        if adversaire.is_alive(): draw_ui(screen, adversaire, 1275, 80)

        if mon_pkm.is_alive() and adversaire.is_alive() and not show_confirm and not show_team:
            for i, label in enumerate(actions):
                ui_rect_tool.draw_buttons(screen, label, 550 + i * 350, 850, 300, 80, font_button, i == action_idx)
        
        if not equipe_vivante:
            overlay = pygame.Surface((1920, 1000), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0,0))
            txt = pygame.font.SysFont("Arial", 60, bold=True).render("GAME OVER", True, (255, 50, 50))
            screen.blit(txt, txt.get_rect(center=(960, 500)))

        elif not mon_pkm.is_alive():
            txt = pygame.font.SysFont("Arial", 40, bold=True).render("Choisissez un autre Pokémon", True, (255, 100, 100))
            screen.blit(txt, txt.get_rect(center=(960, 500)))

        elif not adversaire.is_alive():
            msg = f"{adversaire.name.upper()} vaincu ! (+XP)"
            txt = pygame.font.SysFont("Arial", 40, bold=True).render(msg, True, (0, 255, 127))
            screen.blit(txt, txt.get_rect(center=(960, 450)))
            if level_up_msg:
                # Couleur dorée pour l'évolution/level up
                color = (255, 215, 0) if "devent" in level_up_msg or "!" in level_up_msg else (255, 255, 255)
                lvl_txt = pygame.font.SysFont("Arial", 30, bold=True).render(level_up_msg, True, color)
                screen.blit(lvl_txt, lvl_txt.get_rect(center=(960, 510)))

        if show_team and equipe_vivante:
            overlay = pygame.Surface((1920, 1000), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (35, 35, 55), (710, 150, 500, 650), border_radius=15)
            for i, p in enumerate(equipe):
                y_pos = 260 + (i * 85)
                is_sel = (i == team_idx)
                ui_rect_tool.draw_buttons(screen, f"{p.name} (Nv. {p.lvl})", 760, y_pos, 400, 70, font_button, is_sel)
                if is_sel:
                    txt = font_button.render(f"{p.name} (HP: {max(0, int(p.hp))}/{p.max_hp})", True, (0, 0, 0))
                    screen.blit(txt, txt.get_rect(center=(960, y_pos + 35)))

        if show_confirm: draw_confirm_popup(screen, "Voulez-vous vraiment fuir ?", confirm_idx, ui_rect_tool, font_button)
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1000))
    pygame.display.set_caption("My_Pokemon - Evolution & Persistent Stats")
    loader = Loading_menu(screen)
    loader.run()
    state = "MENU"
    while state != "QUIT":
        if state == "MENU":
            menu = First_screen(screen)
            data = menu.run()
            state = "COMBAT" if data and data != "QUIT" else "QUIT"
        elif state == "COMBAT":
            state = play_battle(screen, data)
    pygame.quit()

if __name__ == "__main__":
    main()