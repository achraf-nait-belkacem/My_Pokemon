import pygame

class Rect:
    def __init__(self):
        self.white = (255, 255, 255)
        self.danger_color = (255, 50, 50)
        self.default_accent = (20, 150, 140)

    def draw_buttons(self, screen, text, x, y, w, h, font, is_selected, color=None):
        if color is None:
            color = self.default_accent
        button_rect = pygame.Rect(x, y, w, h)
        bg_color = (min(color[0]+30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255)) if is_selected else color
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
        if is_selected:
            pygame.draw.rect(screen, self.white, button_rect, 3, border_radius=12)
        text_surf = font.render(text, True, self.white)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        return button_rect