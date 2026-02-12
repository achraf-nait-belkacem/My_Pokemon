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
        active_player = self.pick_player()
        active_enemy = self.pick_enemy()
        return combat(active_player, active_enemy)
        

    def start_combat(self):
        battle_instance = self.create_combat()
        battle_instance.start()

        return battle_instance