import pygame
import random
import os
import json
import math
import unicodedata
from pygame.locals import (
    QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION,
    K_ESCAPE, K_RETURN, K_LEFT, K_RIGHT, K_UP, K_DOWN,
    K_SPACE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
    K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z,
    SRCALPHA, HWSURFACE, DOUBLEBUF, FULLSCREEN
)
from config.colors import (
    COLORS, WHITE, BLACK, SHADOW, BG_DARK, PANEL, ACCENT,
    HP_GREEN, HP_YELLOW, HP_RED, VICTORY, ALERT, OVERLAY, get_hp_color
)
from config.game_balance import (
    XP_PER_LEVEL, XP_ACTIVE_MULTIPLIER, XP_INACTIVE_MULTIPLIER,
    XP_TO_LEVEL_UP, calculate_xp_gain,
    MISS_CHANCE, DAMAGE_BASE_MULTIPLIER, MINIMUM_DAMAGE,
    HP_LEVEL_BONUS, HP_BASE_BONUS, ATTACK_LEVEL_BONUS, DEFENSE_LEVEL_BONUS
)
from SpriteAnimation import PokemonSprite
from backend.combat import Combat
from backend.data_manager import DataManager
from frontend.loading import Loading_menu
from frontend.first_screen import First_screen
__all__ = [
    'pygame', 'random', 'os', 'json', 'math', 'unicodedata',
    'QUIT', 'KEYDOWN', 'KEYUP', 'MOUSEBUTTONDOWN', 'MOUSEBUTTONUP', 'MOUSEMOTION',
    'K_ESCAPE', 'K_RETURN', 'K_LEFT', 'K_RIGHT', 'K_UP', 'K_DOWN', 'K_SPACE',
    'K_a', 'K_b', 'K_c', 'K_d', 'K_e', 'K_f', 'K_g', 'K_h', 'K_i', 'K_j', 'K_k', 'K_l', 'K_m',
    'K_n', 'K_o', 'K_p', 'K_q', 'K_r', 'K_s', 'K_t', 'K_u', 'K_v', 'K_w', 'K_x', 'K_y', 'K_z',
    'SRCALPHA', 'HWSURFACE', 'DOUBLEBUF', 'FULLSCREEN',
    'COLORS', 'WHITE', 'BLACK', 'SHADOW', 'BG_DARK', 'PANEL', 'ACCENT',
    'HP_GREEN', 'HP_YELLOW', 'HP_RED', 'VICTORY', 'ALERT', 'OVERLAY', 'get_hp_color',
    'XP_PER_LEVEL', 'XP_ACTIVE_MULTIPLIER', 'XP_INACTIVE_MULTIPLIER',
    'XP_TO_LEVEL_UP', 'calculate_xp_gain',
    'MISS_CHANCE', 'DAMAGE_BASE_MULTIPLIER', 'MINIMUM_DAMAGE',
    'HP_LEVEL_BONUS', 'HP_BASE_BONUS', 'ATTACK_LEVEL_BONUS', 'DEFENSE_LEVEL_BONUS',
    'PokemonSprite',
    'Combat', 'DataManager',
    'Loading_menu', 'First_screen',
]