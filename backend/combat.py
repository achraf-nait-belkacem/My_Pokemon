import random
import json
import os

class Combat:
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.turn = 1
        self.type_chart = self.load_type_chart()

    def load_type_chart(self):
        """Charge la table des types pour calculer l'efficacité des attaques."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(base_path)
        path = os.path.join(root_path, "data", "types.json")
        
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data
            except Exception as e:
                print(f"❌ Erreur lecture JSON : {e}")
        return {}

    def get_multiplier(self, attacker, defender):
        """Récupère le multiplicateur de dégâts (ex: x2.0 pour l'eau sur le feu)."""
        # On s'assure de récupérer le type en string proprement formaté
        atk_type = str(getattr(attacker, 'type', attacker)).strip().capitalize()
        def_type = str(getattr(defender, 'type', defender)).strip().capitalize()
        
        return self.type_chart.get(atk_type, {}).get(def_type, 1.0)

    def calculate_damage(self, attacker, defender):
        """Calcule les dégâts en fonction de l'attaque, la défense et les types."""
        multiplier = self.get_multiplier(attacker, defender)
        
        # Ratio Atk / Def (évite la division par zéro si la def est nulle)
        ratio = attacker.attack / max(1, defender.defense)
        
        # Puissance de base
        base_power = 15 
        
        # Calcul final : Ratio * Puissance * Multiplicateur de type
        damage = (ratio * base_power) * multiplier
        
        # On ajoute un petit bonus fixe (+2) pour éviter les dégâts à 0
        final_damage = int(damage) + 2
        
        # Message d'efficacité pour le feedback
        if multiplier > 1: print("✨ C'est super efficace !")
        elif multiplier < 1: print("🛡️ Ce n'est pas très efficace...")
        
        return max(1, final_damage)

    def attack(self, attacker, defender):
        """Exécute une attaque : gère l'esquive et inflige les dégâts."""
        # 5% de chance de rater
        if random.random() < 0.05:
            print(f"💨 {attacker.name} a raté son coup !")
            return 0

        damage = self.calculate_damage(attacker, defender)
        defender.take_damage(damage)
        
        print(f"⚔️ {attacker.name} inflige {damage} dégâts à {defender.name}")
        return damage

    def gain_xp(self, winner, loser):
        """Calcule l'XP et vérifie l'évolution après le gain de niveau."""
        xp_amount = loser.lvl * 15
        print(f"📈 {winner.name} gagne {xp_amount} XP")
        
        old_lvl = winner.lvl
        winner.gain_xp(xp_amount) # On suppose que cette méthode gère le passage de niveau
        
        # --- LOGIQUE D'ÉVOLUTION ---
        self.check_evolution(winner)
        
        return winner.lvl > old_lvl

    def check_evolution(self, pokemon):
        """Vérifie dans pokemon.json si le pokemon doit évoluer."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(base_path)
        path = os.path.join(root_path, "data", "pokemon.json")

        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            all_pokemon_data = json.load(f)

        # On cherche les données du Pokémon actuel par son ID
        for p_data in all_pokemon_data:
            if p_data["id"] == pokemon.id:
                evo_info = p_data.get("evolution")
                
                # Si une évolution existe et que le niveau est suffisant
                if evo_info and pokemon.lvl >= evo_info["level"]:
                    print(f"🌟 INCROYABLE ! {pokemon.name} évolue en {evo_info['next_form']} !")
                    
                    # On change l'identité du Pokémon
                    pokemon.name = evo_info["next_form"]
                    
                    # On applique les bonus d'évolution
                    pokemon.max_hp += evo_info.get("hp_bonus", 0)
                    pokemon.hp = pokemon.max_hp # Soins complets lors de l'évolution
                    pokemon.base_attack += evo_info.get("attack_bonus", 0)
                    
                    # On met à jour le sprite pour le prochain combat
                    pokemon.sprite_path = f"assets/sprites/{pokemon.name.lower()}.png"
                    
                    # Si tu as une méthode de recalcul des stats, on l'appelle
                    if hasattr(pokemon, 'recalc_stats'):
                        pokemon.recalc_stats()

    def switch_turn(self):
        """Alterne entre le tour du joueur (1) et de l'ennemi (-1)."""
        self.turn *= -1

    def win_check(self):
        """Vérifie si l'un des deux combattants est K.O."""
        return self.player_pokemon.hp <= 0 or self.enemy_pokemon.hp <= 0