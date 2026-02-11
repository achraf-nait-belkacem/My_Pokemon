import math

class Pokemon:
    def __init__(self, name, hp, level, attack, defense, type  ):
        self.name = name
        self.lvl = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.type = type
        self.sprite_path = f"assets/sprites/{self.name.lower()}.png"
        self.defeated_ennemi_ids = []


    def take_damage (self, amount):
        amount = amount - (self.defense / 10)
        amount = math.ceil(amount)
        if amount < 1:
            amount = 1
        self.hp -= amount
        if self.hp < 0 :
            self.hp = 0
        return self.hp

    def evolve(self, evolution_data):
        if not evolution_data:
            return
        if self.lvl >= evolution_data["level"]:
            print(f"{self.name} evolve in {evolution_data['next_form']} !")
            self.name = evolution_data["next_form"]
            self.sprite_path = f"../assets/sprites/{self.name.lower()}.png"
            self.hp += evolution_data["hp_bonus"]
            self.attack += evolution_data["attack_bonus"]
            self.hp = math.ceil(self.hp)
            self.attack = math.ceil(self.attack)
        

    def new_level(self):
        self.lvl += 1

    def is_alive(self):
        if self.hp <= 0:
            print(f"{self.name} is KO choose an other pokemon")
        return self.hp > 0
        

    def __str__(self):
        return f"{self.name} ({self.type}) - LVL {self.lvl} [HP : {self.hp}]"
