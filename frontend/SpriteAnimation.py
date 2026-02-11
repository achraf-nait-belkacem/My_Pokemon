import pygame
import math

class SpriteAnimation:
    def __init__(self, image_path, position):
        self.sprite = pygame.image.load(image_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (120, 120))

        self.x, self.y = position
        self.state = "idle"
        self.timer = 0


    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.timer = 0

    def draw_idle(self, screen):
        offset = math.sin(self.timer * 0.1) * 4
        rect = self.sprite.get_rect(
            center=(self.x, self.y + offset)
        )
        screen.blit(self.sprite, rect)

    def draw_attack(self, screen):
        shake = [-10, 10, -6, 6, -3, 3, 0]
        offset = shake[min(self.timer, len(shake) - 1)]
        rect = self.sprite.get_rect(
            center=(self.x + offset, self.y)
        )
        screen.blit(self.sprite, rect)

    def draw_hit(self, screen):
        flash = self.sprite.copy()
        flash.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_ADD)
        rect = flash.get_rect(center=(self.x, self.y))
        screen.blit(flash, rect)

    def draw_ko(self, screen):
        alpha = max(0, 255 - self.timer * 8)
        fade = self.sprite.copy()
        fade.set_alpha(alpha)
        rect = fade.get_rect(center=(self.x, self.y))
        screen.blit(fade, rect)

    def update(self, screen):
        self.timer += 1

        if self.state == "idle":
            self.draw_idle(screen)

        elif self.state == "attack":
            self.draw_attack(screen)
            if self.timer > 20:
                self.set_state("idle")

        elif self.state == "hit":
            self.draw_hit(screen)
            if self.timer > 15:
                self.set_state("idle")

        elif self.state == "ko":
            self.draw_ko(screen)
