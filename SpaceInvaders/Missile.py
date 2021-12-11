import pygame
from SpaceInvaders.Config import *


class Missile:
    def __init__(self):
        self.rect = None
        self.explosion_sprite = pygame.image.load(SPRITE_DIRECTORY + MISSILE_EXPLOSION_SPRITE)
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0
        self.time_since_explosion = 0
        self.is_exploded = False
        self.is_active = False

    def launch(self, rect):
        self.rect = rect
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0
        self.is_exploded = False
        self.time_since_explosion = 0
        self.is_active = True

    def update(self, dt):
        if not self.is_active:
            return
        if self.is_exploded:
            self.time_since_explosion += dt
        else:
            self.move(dt)

    def move(self, dt):
        if self.moving_direction == MovingDirection.IDLE:
            return
        self.move_amount += dt / 1000 * MISSILE_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            direction = -1 if self.moving_direction == MovingDirection.UP else 1
            self.rect.y += int(self.move_amount) * direction
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        if not self.is_active:
            return

        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.explosion_sprite.get_rect(center=self.rect.center))
        else:
            pygame.draw.rect(surf, MISSILE_RECT_COLOR, self.rect)

    def explode(self):
        self.is_exploded = True

    def set_inactive(self):
        self.is_active = False
