import pygame
import os
import random
from src.Config import *


class Missile:
    def __init__(self):
        self.rect = None
        self.explosion_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, MISSILE_EXPLOSION_SPRITE))
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0
        self.time_since_explosion = 0
        self.is_exploded = False
        self.is_active = False
        self.missile_type = 'default'
        self.ship_acc = 0

    def launch(self, rect):
        self.rect = rect
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0
        self.is_exploded = False
        self.time_since_explosion = 0
        self.is_active = True

    def update(self, dt, accel):
        if not self.is_active:
            return
        if self.ship_acc == 0:
            self.ship_acc = accel
        if self.is_exploded:
            self.time_since_explosion += dt
        else:
            self.move(dt)

    def move(self, dt):
        if self.moving_direction == MovingDirection.IDLE:
            return
        missile_speed = MISSILE_SPEED[self.missile_type]
        self.move_amount += dt / 1000 * missile_speed
        if self.move_amount > 1.:
            self.rect.y += int(self.move_amount) * -1
            if self.missile_type == 'minigun':
                self.rect.x += max(self.ship_acc, 1) * random.randint(-15, 15)
            else:
                self.rect.x += int(self.move_amount) * self.ship_acc / 3
            self.move_amount -= int(self.move_amount)

        if self.rect.top < 0:
            self.rect.top = 0
            self.explode()
        elif self.rect.x < 0:
            self.rect.x = 0
            self.explode()
        elif self.rect.x > GAME_SPACE[0]:
            self.rect.x = GAME_SPACE[0]-2
            self.explode()

    def draw(self, surf: pygame.Surface):
        if not self.is_active:
            return

        if self.is_exploded:
            surf.blit(self.explosion_sprite,
                      self.explosion_sprite.get_rect(center=self.rect.center))
        else:
            pygame.draw.rect(surf, MISSILE_RECT_COLOR, self.rect)

    def explode(self):
        self.ship_acc = 0
        self.is_exploded = True

    def set_inactive(self):
        self.ship_acc = 0
        self.is_active = False
