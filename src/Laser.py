import pygame
import os
from src.Config import *


class Laser:
    def __init__(self, top_left_pos, type_index: int, invader_direction, acceleration):
        self.invader_direction = invader_direction
        self.explosion_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, LASER_EXPLOSION_SPRITE))
        self.moving_direction = MovingDirection.DOWN
        self.move_amount = 0
        self.sprites = [pygame.image.load(SPRITE_DIRECTORY + s) for s in LASER_SPRITES[type_index]]
        self.sprite_index = 0
        self.rect = pygame.Rect(top_left_pos, self.sprites[self.sprite_index].get_rect().size)
        self.is_exploded = False
        self.time_since_explosion = 0
        self.acceleration = acceleration

    def update(self, dt):
        if self.is_exploded:
            self.time_since_explosion += dt
        self.move(dt)

    def move(self, dt):
        if self.is_exploded:
            return
        self.move_amount += dt / 1000 * LASER_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            direction_x = 0
            if self.invader_direction == MovingDirection.LEFT:
                direction_x = -1
            elif self.invader_direction == MovingDirection.RIGHT:
                direction_x = 1
            self.rect.y += int(self.move_amount)
            self.rect.x += direction_x * (self.rect.right - self.rect.left)/6 * self.acceleration
            if self.rect.left <= 0 or self.rect.right >= GAME_SPACE[0]:
                self.explode()
            self.move_amount -= int(self.move_amount)

    def draw(self, surf: pygame.Surface):
        if self.is_exploded:
            surf.blit(self.explosion_sprite, self.explosion_sprite.get_rect(center=self.rect.center))
        else:
            sprite = self.sprites[self.sprite_index]
            surf.blit(sprite, sprite.get_rect(center=self.rect.center))
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

    def explode(self):
        self.is_exploded = True
