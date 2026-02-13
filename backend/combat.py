import random
import json
import os

class Combat:
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.turn = 1
        self.type_chart = self.load_type_chart()

    def load_type_chart(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(base_path), "data", "types.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return {}

    def get_multiplier(self, attacker, defender):
        atk_type = str(getattr(attacker, 'type', attacker)).strip().capitalize()
        def_type = str(getattr(defender, 'type', defender)).strip().capitalize()
        return self.type_chart.get(atk_type, {}).get(def_type, 1.0)

    def calculate_damage(self, attacker, defender):
        multiplier = self.get_multiplier(attacker, defender)
        ratio = attacker.attack / max(1, defender.defense)
        damage = (ratio * 15) * multiplier
        return max(1, int(damage) + 2)

    def attack(self, attacker, defender):
        if random.random() < 0.05: return 0
        damage = self.calculate_damage(attacker, defender)
        defender.take_damage(damage)
        return damage

    def gain_xp(self, winner, loser):
        # Gain d'XP équilibré : 20 XP par niveau de l'adversaire
        xp_amount = loser.lvl * 20
        return winner.gain_xp(xp_amount) 

    def switch_turn(self):
        self.turn *= -1

    def win_check(self):
        return self.player_pokemon.hp <= 0 or self.enemy_pokemon.hp <= 0