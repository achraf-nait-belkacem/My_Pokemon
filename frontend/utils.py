import pygame
from config.colors import COLORS
class Rect:
    def __init__(self):
        self.colors = COLORS
    def draw_text_shadow(self, screen, text, font, color, pos):
        shadow = font.render(text, True, self.colors["shadow"])
        txt = font.render(text, True, color)
        screen.blit(shadow, (pos[0] + 2, pos[1] + 2))
        screen.blit(txt, pos)
    def draw_pokemon_stats(self, screen, pokemon, x, y, font):
        name_txt = f"{pokemon.name.upper()}  Nv. {pokemon.lvl}"
        self.draw_text_shadow(screen, name_txt, font, self.colors["white"], (x, y))
        pygame.draw.rect(screen, self.colors["white"], (x, y + 32, 250, 14), border_radius=7)
        pygame.draw.rect(screen, (30, 30, 30), (x+2, y+34, 246, 10), border_radius=5)
        ratio = min(1.0, pokemon.hp / pokemon.max_hp if pokemon.max_hp > 0 else 0)
        if ratio > 0.5: hp_color = self.colors["hp_green"]
        elif ratio > 0.2: hp_color = self.colors["hp_yellow"]
        else: hp_color = self.colors["hp_red"]
        if ratio > 0:
            pygame.draw.rect(screen, hp_color, (x+2, y+34, int(246 * ratio), 10), border_radius=5)
        hp_txt = f"{max(0, int(pokemon.hp))} / {pokemon.max_hp}"
        txt_surf = font.render(hp_txt, True, self.colors["white"])
        screen.blit(txt_surf, (x + 250 - txt_surf.get_width(), y + 48))
    def draw_buttons(self, screen, text, x, y, w, h, font, is_selected, color=None):
        if color is None:
            color = self.colors["accent"]
        button_rect = pygame.Rect(x, y, w, h)
        bg_color = (min(color[0]+30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255)) if is_selected else color
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
        if is_selected:
            pygame.draw.rect(screen, self.colors["white"], button_rect, 3, border_radius=12)
        text_surf = font.render(text, True, self.colors["white"])
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        return button_rect
    def draw_team_menu(self, screen, equipe, mon_pkm, selected_idx, font_btn, font_ui):
        pygame.draw.rect(screen, self.colors["panel"], (710, 150, 500, 650), border_radius=15)
        if not mon_pkm.is_alive():
            alert = font_ui.render(f"{mon_pkm.name.upper()} EST KO !", True, self.colors["alert"])
            screen.blit(alert, alert.get_rect(center=(960, 180)))
        for i, p in enumerate(equipe):
            status = f"{p.name} (Nv. {p.lvl})" if p.is_alive() else f"{p.name} (KO)"
            self.draw_buttons(screen, status, 760, 220 + (i * 85), 400, 70, font_btn, i == selected_idx)
    def draw_confirm_popup(self, screen, text, selected_index, font_btn):
        overlay = pygame.Surface((1920, 1000), pygame.SRCALPHA)
        overlay.fill(self.colors["overlay"])
        screen.blit(overlay, (0, 0))
        box = pygame.Rect(660, 350, 600, 300)
        pygame.draw.rect(screen, (45, 45, 65), box, border_radius=15)
        pygame.draw.rect(screen, self.colors["white"], box, 3, border_radius=15)
        msg = pygame.font.SysFont("Arial", 35, bold=True).render(text, True, self.colors["white"])
        screen.blit(msg, msg.get_rect(center=(960, 420)))
        self.draw_buttons(screen, "OUI", 710, 520, 200, 60, font_btn, selected_index == 0)
        self.draw_buttons(screen, "NON", 1010, 520, 200, 60, font_btn, selected_index == 1)