WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHADOW = (40, 40, 40)
BG_DARK = (30, 30, 40)
PANEL = (35, 35, 55)
ACCENT = (20, 150, 140)
HP_GREEN = (0, 255, 127)
HP_YELLOW = (255, 215, 0)
HP_RED = (255, 69, 0)
VICTORY = (0, 255, 127)
ALERT = (255, 80, 80)
OVERLAY = (0, 0, 0, 180)
COLORS = {
    "white": WHITE,
    "black": BLACK,
    "shadow": SHADOW,
    "bg_dark": BG_DARK,
    "panel": PANEL,
    "accent": ACCENT,
    "hp_green": HP_GREEN,
    "hp_yellow": HP_YELLOW,
    "hp_red": HP_RED,
    "victory": VICTORY,
    "alert": ALERT,
    "overlay": OVERLAY,
}
def get_hp_color(hp_ratio):
    if hp_ratio > 0.5:
        return HP_GREEN
    elif hp_ratio > 0.2:
        return HP_YELLOW
    else:
        return HP_RED