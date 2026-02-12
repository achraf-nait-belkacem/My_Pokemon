import json
import os
from backend.pokemon import Pokemon

class DataManager:
    def __init__(self):
        self.data_path = "data/pokemon.json"
        self.save_path = "data/save.json"

    def load_pokedex(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        
        data_by_id = {p["id"]: p for p in all_data}
        
        if not os.path.exists(self.save_path):
            owned_ids = [1]
            with open(self.save_path, "w") as f:
                json.dump(owned_ids, f)
        else:
            with open(self.save_path, "r") as f:
                owned_ids = json.load(f)

        owned = []
        for p_id in owned_ids[:6]:
            if p_id in data_by_id:
                p = data_by_id[p_id]
                poke = Pokemon(p["name"], p["hp"], p["level"], p["attack"], p["defense"], p["type"])
                poke.id = p_id
                owned.append(poke)
        return owned

    def load_all_ennemi(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        
        ennemis = []
        for p in all_data:
            poke = Pokemon(p["name"], p["hp"], p["level"], p["attack"], p["defense"], p["type"])
            poke.id = p["id"]
            ennemis.append(poke)
        return ennemis

    def save_team(self, pokemons):
        owned_ids = [poke.id for poke in pokemons]
        with open(self.save_path, "w") as f:
            json.dump(owned_ids, f)

    def load_type_chart(self):
        try : 
            with open("data/types.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("ERROR : File don't exist")
            return {}