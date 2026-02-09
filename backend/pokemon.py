import json

class Pokemon:
    def __init__(self, name, hp, level, attack, defense, p_type  ):
        self.name = name
        self.lvl = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.type = p_type
        self.sprite_path = f"../assets/sprites/{self.name.lower()}.png"


    def take_damage (self, amount):
        amount = amount - (self.defense / 10)
        if amount < 1:
            amount = 1
        self.hp -= amount
        if self.hp < 0 :
            self.hp = 0
        return self.hp

    def evolve(self, new_name, new_attack, new_hp, new_sprite_path):
        if self.lvl >= 32:
            self.name = new_name
            self.attack = new_attack * 1.5
            self.hp = new_hp * 1.5
            self.sprite_path = new_sprite_path
        elif self.lvl >= 16:
            self.name = new_name
            self.attack = new_attack
            self.hp = new_hp
            self.sprite_path = new_sprite_path
        

    def new_level(self):
        self.lvl += 1

    def is_alive(self):
        if self.hp <= 0:
            print(f"{self.name} is KO choose an other pokemon")
        return self.hp > 0
        

    def __str__(self):
        return f"{self.name} ({self.type}) - LVL {self.lvl} [HP : {self.hp}]"
        
