from backend.data_manager import DataManager

class Postcombat :
    def __init__(self, winner, loser, player_all_pokemons):
        self.winner = winner
        self.loser = loser
        self.player_all_pokemons = player_all_pokemons
        self.db = DataManager()

    def capture(self):
        new_pokemon_id = self.loser.id
        self.player_all_pokemons.append(self.loser)
        self.db.save_team(self.player_all_pokemons)
        print(f"{self.loser.name} a été ajouté a votre pokedex")

    def update_player_stat(self):
        xp_gagne = self.loser.lvl * 15
        self.winner.gain_xp(xp_gagne)
        self.db.save_team(self.player_all_pokemons)