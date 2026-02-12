import json
import os
from backend.pokemon import Pokemon

class DataManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, "data", "pokemon.json")
        self.save_path = os.path.join(self.base_dir, "data", "save.json")

    def load_pokedex(self):
        """Charge l'équipe en tenant compte du nom sauvegardé (pour l'évolution)."""
        if not os.path.exists(self.data_path):
            return []

        with open(self.data_path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        
        data_by_id = {p["id"]: p for p in all_data}
        
        if not os.path.exists(self.save_path):
            owned_data = [{"id": 1, "name": "Bulbizarre", "level": 5, "xp": 0}] 
            self.save_team_raw(owned_data)
        else:
            with open(self.save_path, "r", encoding="utf-8") as f:
                owned_data = json.load(f)

        owned = []
        for data in owned_data[:6]:
            p_id = data["id"]
            p_lvl = data.get("level", 5)
            p_xp = data.get("xp", 0)
            # ON RÉCUPÈRE LE NOM SAUVEGARDÉ (Evolution !)
            # Si pas de nom dans la sauvegarde, on prend celui du pokedex par défaut
            p_name = data.get("name", data_by_id.get(p_id, {}).get("name", "Inconnu"))

            if p_id in data_by_id:
                p = data_by_id[p_id]
                # On utilise p_name ici au lieu de p["name"]
                poke = Pokemon(p_name, p["hp"], p_lvl, p["attack"], p["defense"], p["type"])
                poke.id = p_id
                poke.xp = p_xp
                poke.base_hp = p["hp"]
                poke.base_attack = p["attack"]
                poke.base_defense = p["defense"]
                
                if hasattr(poke, 'recalc_stats'):
                    poke.recalc_stats()
                owned.append(poke)
        return owned

    def save_team(self, pokemons):
        """Sauvegarde l'état actuel incluant le nom (essentiel pour l'évolution)."""
        # On charge tout le contenu actuel pour ne pas supprimer les pokemons hors équipe
        full_save = self.load_save_raw()
        
        # On crée un dictionnaire des pokemons de l'équipe pour mise à jour facile
        team_ids = {p.id: p for p in pokemons}

        new_save_data = []
        
        # 1. On parcourt l'ancienne sauvegarde
        for entry in full_save:
            p_id = entry["id"]
            if p_id in team_ids:
                # On met à jour avec les infos de l'équipe (XP, Level, Nom)
                p_obj = team_ids[p_id]
                new_save_data.append({
                    "id": p_obj.id,
                    "name": p_obj.name, # Sauvegarde "Herbizarre" par ex.
                    "level": p_obj.lvl,
                    "xp": getattr(p_obj, 'xp', 0)
                })
            else:
                # On garde tel quel les pokémons qui ne sont pas dans l'équipe actuelle
                new_save_data.append(entry)

        self.save_team_raw(new_save_data)

    def load_save_raw(self):
        """Charge le JSON de sauvegarde brut."""
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
            poke.base_hp = p["hp"]
            poke.base_attack = p["attack"]
            poke.base_defense = p["defense"]
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
                "xp": 0
            })
            self.save_team_raw(owned_data)
            print(f"✅ {pokemon_to_add.name} ajouté à la sauvegarde !")
            return True 
        return False