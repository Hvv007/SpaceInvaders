import pygame
from Config import *


class MysteryShip:
    def __init__(self):
        self.sprite = pygame.image.load(SPRITE_DIRECTORY + MYSTERY_SHIP_SPRITE_NAME)
        self.explosion_sprite = pygame.image.load(SPRITE_DIRECTORY + MYSTERY_SHIP_EXPLOSION_SPRITE_NAME)
        self.rect = self.sprite.get_rect()
        self.moving_direction = None
        self.move_amount = 0
        self.is_active = False
        self.is_exploded = False
        self.time_since_explosion = 0
        self.explosion_duration = MYSTERY_SHIP_EXPLOSION_DURATION_MS

    def launch(self, top_left_pos, direction: MovingDirection):
        self.rect = self.sprite.get_rect(topleft=top_left_pos)
        self.moving_direction = direction
        self.is_active = True
        self.is_exploded = False
        self.time_since_explosion = 0

    def update(self, dt):
        if self.is_exploded:
            self.time_since_explosion += dt
        self.move(dt)

    def move(self, dt):
        if self.is_exploded:
            return
        self.move_amount += dt / 1000 * MYSTERY_SHIP_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.x += int(self.move_amount) * self.moving_direction[0][0]
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        if not self.is_active:
            return
        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.rect)
        else:
            surf.blit(self.sprite, self.rect)

    def explode(self):
        self.is_exploded = True

    def set_inactive(self):
        self.is_active = False
