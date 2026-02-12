import math

class Pokemon:
    def __init__(self, name, hp, level, attack, defense, pokemon_type):
        self.name = name
        self.lvl = level
        self.xp = 0
        self.type = pokemon_type
        
        # --- STATS DE BASE ---
        # On sauvegarde ces valeurs pour les calculs de croissance
        self.base_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        
        # --- STATS ACTUELLES ---
        self.max_hp = 0
        self.attack = 0
        self.defense = 0
        
        # Calcul initial des stats selon le niveau
        self.recalc_stats()
        
        # Initialisation des PV au maximum au départ
        self.hp = self.max_hp
        
        self.sprite_path = f"assets/sprites/{self.name.lower()}.png"
        self.id = None # Sera défini par le DataManager
        self.processed = False # Flag pour la logique de victoire

    def recalc_stats(self):
        """
        Recalcule les statistiques réelles.
        C'est ici que la barre de vie puise son information 'Max'.
        """
        # Formule de croissance : Base + (Niveau * Coefficient)
        self.max_hp = math.ceil(self.base_hp + (self.lvl * 2))
        self.attack = math.ceil(self.base_attack + (self.lvl * 1.5))
        self.defense = math.ceil(self.base_defense + (self.lvl * 1.2))

    def gain_xp(self, amount):
        """Ajoute de l'XP et gère la montée de niveau multiple."""
        self.xp += amount
        leveled_up = False
        
        while self.xp >= 100:
            self.lvl += 1
            self.xp -= 100
            leveled_up = True
            
            # Mise à jour du plafond de PV
            self.recalc_stats()
            
            # SYNCHRONISATION PV : On remet les PV au nouveau Max
            # Cela évite que la barre de vie reste bloquée sur l'ancien ratio
            self.hp = self.max_hp 
            
            print(f"🆙 {self.name} est monté au Niveau {self.lvl} ! (PV: {self.hp}/{self.max_hp})")
        
        return leveled_up

    def evolve(self, evolution_data):
        """Transforme le Pokémon si les conditions sont remplies."""
        if not evolution_data:
            return False
            
        if self.lvl >= evolution_data["level"]:
            print(f"🌟 QUOI ? {self.name} évolue !")
            
            # Changement d'identité
            self.name = evolution_data["next_form"]
            self.sprite_path = f"assets/sprites/{self.name.lower()}.png"
            
            # Application des bonus permanents aux bases
            self.base_hp += evolution_data.get("hp_bonus", 0)
            self.base_attack += evolution_data.get("attack_bonus", 0)
            
            # Recalcul global pour que max_hp intègre les nouveaux bonus
            self.recalc_stats()
            
            # Soin complet après évolution pour l'UI
            self.hp = self.max_hp
            return True
            
        return False

    def take_damage(self, amount):
        """Réduit les PV actuels sans descendre sous 0."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def is_alive(self):
        """Retourne True si le Pokémon a encore des PV."""
        return self.hp > 0

    def __str__(self):
        return f"{self.name} ({self.type}) - Nv. {self.lvl} [{int(self.hp)}/{self.max_hp} PV]"