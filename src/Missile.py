import pygame
import os
import random
from src.Config import *


class Missile:
    def __init__(self):
        self.ship_direction = MovingDirection.IDLE
        self.rect = None
        self.explosion_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, MISSILE_EXPLOSION_SPRITE))
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0
        self.time_since_explosion = 0
        self.is_exploded = False
        self.is_active = False
        self.missile_type = 'default'

    def launch(self, rect, ship_direction):
        self.rect = rect
        self.moving_direction = MovingDirection.UP
        self.move_amount = 0
        self.is_exploded = False
        self.time_since_explosion = 0
        self.is_active = True
        self.ship_direction = ship_direction

    def update(self, dt, ship_move_amount):
        if not self.is_active:
            return
        if self.is_exploded:
            self.time_since_explosion += dt
        else:
            self.move(dt, ship_move_amount)

    def move(self, dt, ship_move_amount):
        if self.moving_direction == MovingDirection.IDLE:
            return
        missile_speed = MISSILE_SPEED[self.missile_type]
        self.move_amount += dt / 1000 * missile_speed
        if self.move_amount > 1.:
            direction_x = 0
            if self.ship_direction == MovingDirection.LEFT:
                direction_x = -1
            elif self.ship_direction == MovingDirection.RIGHT:
                direction_x = 1
            self.rect.y += int(self.move_amount) * -1
            if self.missile_type == 'minigun':
                self.rect.x += ship_move_amount * random.randint(-10, 10)
            else:
                self.rect.x += direction_x * ship_move_amount
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
        self.is_exploded = True

    def set_inactive(self):
        self.is_active = False
