import math
import os
import unicodedata

class Pokemon:
    def __init__(self, name, hp, level, attack, defense, pokemon_type, current_hp=None):
        self.name = name.strip()
        self.lvl = level
        self.xp = 0
        self.type = pokemon_type
        self.base_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.max_hp = 0
        self.attack = 0
        self.defense = 0
        self.recalc_stats()
        
        if current_hp is not None:
            self.hp = float(current_hp)
        else:
            self.hp = float(self.max_hp)
        
        self.sprite_path = "assets/sprites/default.png"
        self.update_sprite()
        self.id = None 
        self.processed = False 
        self.can_evolve = True

    def update_sprite(self):
        name_clean = "".join(
            c for c in unicodedata.normalize('NFD', self.name)
            if unicodedata.category(c) != 'Mn'
        )
        filename = name_clean.lower().strip().replace(" ", "")
        rel_path = f"assets/sprites/{filename}.png"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        abs_path = os.path.join(base_dir, "assets", "sprites", f"{filename}.png")
        
        if os.path.exists(abs_path):
            self.sprite_path = abs_path
        elif os.path.exists(rel_path):
            self.sprite_path = rel_path
        else:
            self.sprite_path = "assets/sprites/default.png"

    def recalc_stats(self):
        self.max_hp = math.ceil(self.base_hp + (self.lvl * 2))
        self.attack = math.ceil(self.base_attack + (self.lvl * 1.5))
        self.defense = math.ceil(self.base_defense + (self.lvl * 1.2))
        if hasattr(self, 'hp') and self.hp > self.max_hp:
            self.hp = self.max_hp

    def gain_xp(self, amount):
        self.xp += amount
        leveled_up = False
        while self.xp >= 100:
            self.lvl += 1
            self.xp -= 100
            leveled_up = True
            old_max = self.max_hp
            self.recalc_stats()
            gain_hp = self.max_hp - old_max
            if self.hp > 0:
                self.hp += gain_hp
        return leveled_up

    def evolve(self, evolution_data):
        if not evolution_data or not self.can_evolve:
            return False
        nom_actuel = self.name.strip().lower()
        nom_evolution = evolution_data["next_form"].strip().lower()
        niveau_requis = evolution_data.get("level", 16)
        if nom_actuel == nom_evolution:
            return False
        if self.lvl >= niveau_requis:
            self.name = evolution_data["next_form"].strip()
            self.update_sprite()
            self.base_hp += evolution_data.get("hp_bonus", 0)
            self.base_attack += evolution_data.get("attack_bonus", 0)
            self.recalc_stats()
            self.hp = self.max_hp 
            return True
        return False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        return self.hp

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"{self.name} (Nv. {self.lvl}) - HP: {int(self.hp)}/{self.max_hp}"