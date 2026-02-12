import pygame
import math

class PokemonSprite:
    def __init__(self, name_or_path, position, size=(200, 200)):
        # 1. Gestion intelligente du chemin pour éviter les doublons
        # Si name_or_path contient déjà "assets" ou ".png", on ne rajoute rien
        if "assets/" in name_or_path or name_or_path.lower().endswith(".png"):
            path = name_or_path
        else:
            # Sinon, on construit le chemin proprement
            path = f"assets/sprites/{name_or_path.lower()}.png"

        self.name = name_or_path
        
        # 2. Chargement de l'image avec sécurité
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Si l'image n'existe pas, on crée un rectangle rose de secours
            print(f"Attention : Fichier introuvable à {path}")
            self.image = pygame.Surface(size)
            self.image.fill((255, 0, 255)) 
            
        # 3. Redimensionnement et initialisation
        self.image = pygame.transform.scale(self.image, size)
        self.base_pos = position
        self.state = "idle"
        self.timer = 0

    def set_state(self, new_state):
        """Change l'état de l'animation (idle, attack, hit, ko)"""
        if self.state != new_state:
            self.state = new_state
            self.timer = 0

    def update(self):
        """Met à jour le timer pour les calculs de mouvement"""
        self.timer += 1
        
        # Retour automatique à l'état idle après une animation finie
        if self.state == "attack" and self.timer > 20:
            self.set_state("idle")
        elif self.state == "hit" and self.timer > 15:
            self.set_state("idle")

    def draw(self, screen):
        """Affiche le sprite avec l'effet correspondant à l'état"""
        if self.state == "idle":
            # Effet de flottement vertical (math.sin)
            offset = math.sin(self.timer * 0.1) * 8
            rect = self.image.get_rect(center=(self.base_pos[0], self.base_pos[1] + offset))
            screen.blit(self.image, rect)

        elif self.state == "attack":
            # Effet de secousse horizontale (shake)
            shake = [-15, 15, -10, 10, -5, 5, 0]
            offset = shake[min(self.timer // 2, len(shake) - 1)]
            rect = self.image.get_rect(center=(self.base_pos[0] + offset, self.base_pos[1]))
            screen.blit(self.image, rect)

        elif self.state == "hit":
            # Flash rouge (dégâts)
            flash = self.image.copy()
            flash.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_ADD)
            rect = flash.get_rect(center=self.base_pos)
            screen.blit(flash, rect)

        elif self.state == "ko":
            # Disparition progressive (Alpha)
            alpha = max(0, 255 - self.timer * 5)
            fade = self.image.copy()
            fade.set_alpha(alpha)
            rect = fade.get_rect(center=self.base_pos)
            screen.blit(fade, rect)