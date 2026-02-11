import json
import os
from backend.pokemon import Pokemon

def load_pokedex():
    with open("data/pokemon.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)
    data_by_id = {p["id"]: p for p in all_data}
    save_path = "data/save.json"
    if not os.path.exists(save_path):
        owned_ids = [1]
        with open(save_path, "w") as f:
            json.dump(owned_ids, f)
    else:
        with open(save_path, "r") as f:
            owned_ids = json.load(f)
    owned = []
    for p_id in owned_ids[:6]:
        if p_id in data_by_id:
            p = data_by_id[p_id]
            poke = Pokemon(p["name"], p["hp"], p["level"], p["attack"], p["defense"], p["type"])
            poke.id = p_id
            owned.append(poke)
    return owned

def load_all_ennemi():
    with open("data/pokemon.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)
    ennemis = []
    for p in all_data:
        poke = Pokemon(p["name"], p["hp"], p["level"], p["attack"], p["defense"], p["type"])
        poke.id = p["id"]
        ennemis.append(poke)
    return ennemis

def save_team(pokemons):
    owned_ids = [poke.id for poke in pokemons]
    with open("data/save.json", "w") as f:
        json.dump(owned_ids, f)