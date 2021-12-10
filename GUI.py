import pygame
from Config import *


class LifeCounter:
    def __init__(self):
        self.life_count = STARTING_LIFE_COUNT
        self.life_sprite = pygame.image.load(SPRITE_DIRECTORY + SPACESHIP_SPRITE)
        self.digit_sprites = [pygame.image.load(SPRITE_DIRECTORY + str(i) + ".png") for i in range(10)]

    def draw(self, surf: pygame.Surface):
        surf.blit(self.digit_sprites[self.life_count], pygame.Rect(LIFE_COUNT_POS, (0, 0)))
        rect = self.life_sprite.get_rect()
        rect.left, rect.top = LIFE_POS
        for life in range(self.life_count):
            surf.blit(self.life_sprite, rect)
            rect.left, rect.top = (rect.left + LIFE_POS_SHIFT[0] + rect.w, rect.top + LIFE_POS_SHIFT[1])
