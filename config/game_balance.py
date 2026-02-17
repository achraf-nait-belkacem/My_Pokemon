XP_PER_LEVEL = 20
XP_ACTIVE_MULTIPLIER = 1.0
XP_INACTIVE_MULTIPLIER = 0.25
XP_TO_LEVEL_UP = 100
def calculate_xp_gain(enemy_level, is_active_pokemon=True):
    base_xp = enemy_level * XP_PER_LEVEL
    if is_active_pokemon:
        return int(base_xp * XP_ACTIVE_MULTIPLIER)
    else:
        return int(base_xp * XP_INACTIVE_MULTIPLIER)
MISS_CHANCE = 0.05
DAMAGE_BASE_MULTIPLIER = 15
MINIMUM_DAMAGE = 1
HP_LEVEL_BONUS = 2.5
HP_BASE_BONUS = 10
ATTACK_LEVEL_BONUS = 1.5
DEFENSE_LEVEL_BONUS = 1.2