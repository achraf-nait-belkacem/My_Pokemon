from imports import *
class PokemonSprite:
    def __init__(self, path_to_sprite, position, size=(200, 200)):
        self.base_pos = position
        self.size = size
        self.state = "idle"
        self.timer = 0
        self.image = self._load_sprite(path_to_sprite)
        self.image = pygame.transform.scale(self.image, size)
    def _load_sprite(self, path):
        try:
            if not path:
                raise FileNotFoundError
            return pygame.image.load(str(path)).convert_alpha()
        except (pygame.error, FileNotFoundError):
            default_path = "assets/sprites/default.png"
            if os.path.exists(default_path):
                return pygame.image.load(default_path).convert_alpha()
            else:
                surface = pygame.Surface((100, 100), pygame.SRCALPHA)
                surface.fill((255, 0, 255))
                return surface
    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.timer = 0
    def update(self):
        self.timer += 1
        if self.state == "attack" and self.timer > 20:
            self.set_state("idle")
        elif self.state == "hit" and self.timer > 15:
            self.set_state("idle")
    def draw(self, screen):
        if self.state == "idle":
            offset_y = math.sin(self.timer * 0.1) * 8
            rect = self.image.get_rect(center=(self.base_pos[0], self.base_pos[1] + offset_y))
            screen.blit(self.image, rect)
        elif self.state == "attack":
            shake_offsets = [-20, 20, -15, 15, -10, 10, -5, 5, 0]
            idx = min(self.timer // 2, len(shake_offsets) - 1)
            offset_x = shake_offsets[idx]
            rect = self.image.get_rect(center=(self.base_pos[0] + offset_x, self.base_pos[1]))
            screen.blit(self.image, rect)
        elif self.state == "hit":
            flash_surf = self.image.copy()
            flash_surf.fill((255, 0, 0, 150), special_flags=pygame.BLEND_RGBA_MULT)
            rect = flash_surf.get_rect(center=self.base_pos)
            screen.blit(flash_surf, rect)
        elif self.state == "ko":
            alpha = max(0, 255 - self.timer * 8)
            fade_surf = self.image.copy()
            fade_surf.set_alpha(alpha)
            pos_y = self.base_pos[1] + (self.timer * 2)
            rect = fade_surf.get_rect(center=(self.base_pos[0], pos_y))
            screen.blit(fade_surf, rect)