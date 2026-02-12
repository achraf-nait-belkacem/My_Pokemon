import random
from combat import Combat

class Setcombat :
    def __init__(self, player_pokemon_list, enemy_pokemon_list):
        self.player_pokemon = player_pokemon_list
        self.enemy_pokemon = enemy_pokemon_list

    def pick_player(self, index):
        return self.player_pokemon[index]

    def pick_enemy(self):
        choice = random.choice(self.enemy_pokemon)
        return choice

    def create_combat(self):
        player_pokemon = self.pick_player()
        enemy_pokemon = self.pick_enemy()
        return Combat(player_pokemon, enemy_pokemon)

    def start_combat(self):
        combat = self.create_combat()
        return combat.start()