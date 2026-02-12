import random
from pokemon import Pokemon


class Combat :
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.turn = 1

    def start(self):
        while not self.win_check():
            attacker, defender = self.get_attacker_defendre()
            self.attack(attacker, defender)
            
            self.switch_turn()

        return self.get_winner()

    def attack(self, attacker, defender):

        if self.miss_attack():
            return 0

        damage = self.calculate_damage(attacker, defender)

        defender.take_damage (damage)
        
    def get_attacker_defendre(self):

        if self.turn == 1:
            return self.player_pokemon, self.enemy_pokemon
        else:
            return self.enemy_pokemon, self.player_pokemon

    def matching(self, type1, type2):

        table = {
        "Acier": {"Acier": 0.5, "Eau": 0.5, "Electrik": 0.5, "Feu": 0.5, "Fée": 2.0, "Glace": 2.0, "Roche": 2.0},
        "Combat": {"Acier": 2.0, "Fée": 0.5, "Glace": 2.0, "Insecte": 0.5, "Normal": 2.0, "Poison": 0.5, "Psy": 0.5, "Roche": 2.0, "Spectre": 0.0, "Ténèbres": 2.0},
        "Dragon": {"Acier": 0.5, "Dragon": 2.0, "Fée": 0.0},
        "Eau": {"Dragon": 0.5, "Eau": 0.5, "Feu": 2.0, "Plante": 0.5, "Roche": 2.0, "Sol": 2.0},
        "Electrik": {"Dragon": 0.5, "Eau": 2.0, "Electrik": 0.5, "Plante": 0.5, "Sol": 0.0, "Vol": 2.0},
        "Feu": {"Acier": 2.0, "Dragon": 0.5, "Eau": 0.5, "Feu": 0.5, "Glace": 2.0, "Insecte": 2.0, "Plante": 2.0, "Roche": 0.5},
        "Fée": {"Acier": 0.5, "Combat": 2.0, "Dragon": 2.0, "Feu": 0.5, "Poison": 0.5, "Ténèbres": 2.0},
        "Glace": {"Acier": 0.5, "Dragon": 2.0, "Eau": 0.5, "Feu": 0.5, "Glace": 0.5, "Plante": 2.0, "Sol": 2.0, "Vol": 2.0},
        "Insecte": {"Acier": 0.5, "Combat": 0.5, "Feu": 0.5, "Fée": 0.5, "Plante": 2.0, "Poison": 0.5, "Psy": 2.0, "Spectre": 0.5, "Ténèbres": 2.0, "Vol": 0.5},
        "Normal": {"Acier": 0.5, "Roche": 0.5, "Spectre": 0.0},
        "Plante": {"Acier": 0.5, "Dragon": 0.5, "Eau": 2.0, "Feu": 0.5, "Insecte": 0.5, "Plante": 0.5, "Poison": 0.5, "Roche": 2.0, "Sol": 2.0, "Vol": 0.5},
        "Poison": {"Acier": 0.0, "Fée": 2.0, "Plante": 2.0, "Poison": 0.5, "Roche": 0.5, "Sol": 0.5, "Spectre": 0.5},
        "Psy": {"Acier": 0.5, "Combat": 2.0, "Poison": 2.0, "Psy": 0.5, "Ténèbres": 0.0},
        "Roche": {"Acier": 0.5, "Combat": 0.5, "Feu": 2.0, "Glace": 2.0, "Insecte": 2.0, "Sol": 0.5, "Vol": 2.0},
        "Sol": {"Acier": 2.0, "Electrik": 2.0, "Feu": 2.0, "Insecte": 0.5, "Plante": 0.5, "Poison": 2.0, "Roche": 2.0, "Vol": 0.0},
        "Spectre": {"Normal": 0.0, "Psy": 2.0, "Spectre": 2.0, "Ténèbres": 0.5},
        "Ténèbres": {"Combat": 0.5, "Fée": 0.5, "Psy": 2.0, "Spectre": 2.0, "Ténèbres": 0.5},
        "Vol": {"Electrik": 0.5, "Insecte": 2.0, "Plante": 2.0, "Roche": 0.5, "Combat": 2.0}
        }

        return table.get(type1, {}).get(type2, 1.0)

    def miss_attack(self):
        return random.random() < 0.1
    

    def calculate_damage(self, attacker, defender):

        multiplier = self.matching(attacker.type, defender.type)

        damage = attacker.attack * multiplier

        return max(1, int(damage))

    def switch_turn(self):
        if self.turn == 1 :
            attacker = self.player_pokemon
            defender = self.enemy_pokemon
            self.turn *= -1
            return attacker, defender
        elif self.turn == -1 :
            attacker = self.enemy_pokemon
            defender = self.player_pokemon
            self.turn *= -1
            return attacker, defender

    def win_check(self):
        return self.player_pokemon.hp <= 0 or self.enemy_pokemon.hp <= 0

    def get_winner(self):
        if self.enemy_pokemon.hp <= 0:
            return self.player_pokemon
        elif self.player_pokemon.hp <= 0:
            return self.enemy_pokemon
