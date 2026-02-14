import json
import os
from backend.pokemon import Pokemon
class DataManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, "data", "pokemon.json")
        self.save_path = os.path.join(self.base_dir, "data", "save.json")
    def load_save_raw(self):
        if not os.path.exists(self.save_path): return []
        with open(self.save_path, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    def save_team_raw(self, data):
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    def add_to_save(self, pokemon_to_add):
        if pokemon_to_add.id is None: return
        all_pkm = self.load_save_raw()
        if any(int(p["id"]) == int(pokemon_to_add.id) for p in all_pkm):
            return
        all_pkm.append({
            "id": int(pokemon_to_add.id),
            "name": str(pokemon_to_add.name),
            "level": int(pokemon_to_add.lvl),
            "xp": int(getattr(pokemon_to_add, 'xp', 0)),
            "current_hp": int(pokemon_to_add.max_hp)
        })
        self.save_team_raw(all_pkm)
    def save_team(self, current_team):
        all_pkm = self.load_save_raw()
        team_ids = [p.id for p in current_team]
        for saved_pkm in all_pkm:
            for active_pkm in current_team:
                if int(saved_pkm["id"]) == int(active_pkm.id):
                    saved_pkm["level"] = int(active_pkm.lvl)
                    saved_pkm["xp"] = int(getattr(active_pkm, 'xp', 0))
                    saved_pkm["current_hp"] = int(active_pkm.hp)
                    saved_pkm["name"] = str(active_pkm.name)
        self.save_team_raw(all_pkm)
    def load_pokedex(self):
        if not os.path.exists(self.data_path): return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            all_dict = {p["id"]: p for p in json.load(f)}
        save_data = self.load_save_raw()
        if not save_data:
            save_data = [{"id": 1, "name": "Bulbizarre", "level": 5, "xp": 0, "current_hp": 45},
                         {"id" : 4, "name": "Salameche", "level": 5, "xp": 0, "current_hp": 39},
                         {"id" : 7, "name": "Carapuce", "level": 5, "xp": 0, "current_hp": 44}
                         ]
            self.save_team_raw(save_data)
        owned = []
        for data in save_data:
            p_id = data["id"]
            if p_id in all_dict:
                info = all_dict[p_id]
                p = Pokemon(data.get("name", info["name"]), info["hp"], data["level"], 
                            info["attack"], info["defense"], info["type"], data["current_hp"])
                p.id = p_id
                p.xp = data.get("xp", 0)
                p.update_sprite()
                owned.append(p)
        return owned
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