import random

class Setcombat :
    def __init__(self, player_pokemon_list, enemy_pokemon_list):
        self.player_pokemon = player_pokemon_list
        self.enemy_pokemon = random.choice(enemy_pokemon_list)

    def pick_player(self):
        return self.player_pokemon[0]

    def pick_enemy(self):
        return self.enemy_pokemon

    def create_combat(self):
        pass

    def start_combat(self):
        pass