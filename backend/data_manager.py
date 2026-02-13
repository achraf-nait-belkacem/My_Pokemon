import json
import os
from backend.pokemon import Pokemon

class DataManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, "data", "pokemon.json")
        self.save_path = os.path.join(self.base_dir, "data", "save.json")

    def load_pokedex(self):
        if not os.path.exists(self.data_path): 
            return []

        with open(self.data_path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        data_by_id = {p["id"]: p for p in all_data}
        
        if not os.path.exists(self.save_path):
            owned_data = [{"id": 1, "name": "Bulbizarre", "level": 5, "xp": 0, "current_hp": 45}] 
            self.save_team_raw(owned_data)
        else:
            with open(self.save_path, "r", encoding="utf-8") as f:
                owned_data = json.load(f)

        owned = []
        for data in owned_data:
            p_id = data["id"]
            if p_id not in data_by_id: 
                continue
            
            p_info = data_by_id[p_id]
            p_name = data.get("name", p_info["name"])
            p_hp_base = p_info["hp"]
            p_atk_base = p_info["attack"]

            if p_name != p_info["name"] and "evolution" in p_info:
                evo = p_info["evolution"]
                if p_name == evo["next_form"]:
                    p_hp_base += evo.get("hp_bonus", 0)
                    p_atk_base += evo.get("attack_bonus", 0)

            poke = Pokemon(
                p_name, 
                p_hp_base, 
                data.get("level", 5), 
                p_atk_base, 
                p_info["defense"], 
                p_info["type"], 
                current_hp=data.get("current_hp")
            )
            
            poke.update_sprite()
            poke.id = p_id
            poke.xp = data.get("xp", 0)
            owned.append(poke)
            
        return owned

    def save_team(self, pokemons_list):
        new_save_data = []
        for p in pokemons_list:
            new_save_data.append({
                "id": p.id,
                "name": p.name,
                "level": p.lvl,
                "xp": getattr(p, 'xp', 0),
                "current_hp": p.hp
            })
        self.save_team_raw(new_save_data)

    def load_save_raw(self):
        if not os.path.exists(self.save_path): return []
        with open(self.save_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_team_raw(self, data):
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_all_ennemi(self):
        if not os.path.exists(self.data_path): return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        ennemis = []
        for p in data:
            poke = Pokemon(p["name"], p["hp"], p["level"], p["attack"], p["defense"], p["type"])
            poke.id = p.get("id") 
            poke.update_sprite()
            ennemis.append(poke)
        return ennemis

    def add_to_save(self, pokemon_to_add):
        owned_data = self.load_save_raw()
        already_owned = any(p["id"] == pokemon_to_add.id for p in owned_data)
        if not already_owned:
            owned_data.append({
                "id": pokemon_to_add.id,
                "name": pokemon_to_add.name,
                "level": pokemon_to_add.lvl,
                "xp": 0,
                "current_hp": pokemon_to_add.max_hp
            })
            self.save_team_raw(owned_data)
            return True 
        return False