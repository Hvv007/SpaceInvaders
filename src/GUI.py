import pygame
import os
from src.Config import *


class LifeCounter:
    def __init__(self):
        self.life_count = STARTING_LIFE_COUNT
        self.life_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, SPACESHIP_SPRITE))
        self.digit_sprites = [pygame.image.load(SPRITE_DIRECTORY + str(i) + ".png") for i in range(10)]
        self.extra_lives_count = 0
        self.extra_life_sound = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, EXTRA_LIFE_SOUND))

    def draw(self, surf: pygame.Surface):
        surf.blit(self.digit_sprites[self.life_count], pygame.Rect(LIFE_COUNT_POS, (0, 0)))
        rect = self.life_sprite.get_rect()
        rect.left, rect.top = LIFE_POS
        for life in range(self.life_count):
            surf.blit(self.life_sprite, rect)
            rect.left, rect.top = (rect.left + LIFE_POS_SHIFT[0] + rect.w, rect.top + LIFE_POS_SHIFT[1])


class Score:
    def __init__(self, score_type):
        self.value = 0
        self.digit_sprites = [pygame.image.load(SPRITE_DIRECTORY + str(i) + ".png") for i in range(10)]
        if score_type == 'score':
            self.score_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, SCORE_SPRITE))
            self.score_position = SCORE_POS
        else:
            self.score_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, HIGH_SCORE_SPRITE))
            self.score_position = HIGH_SCORE_POS

    def draw(self, surf: pygame.Surface):
        score_string = str(self.value)
        while len(score_string) < SCORE_DIGIT_COUNT:
            score_string = '0' + score_string
        score_x, score_y = self.score_position
        offset = SCORE_BETWEEN_DIGIT_SPACE_PIXELS
        digit_rect = self.digit_sprites[0].get_rect()
        digit_rect.x, digit_rect.y = score_x, score_y - (digit_rect.h * 2)
        surf.blit(self.score_sprite, digit_rect)
        for digit in score_string:
            digit_rect.x, digit_rect.y = score_x, score_y
            surf.blit(self.digit_sprites[int(digit)], digit_rect)
            score_x += digit_rect.w + offset


class GameOver:
    def __init__(self):
        self.game_over_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, GAME_OVER_SPRITE))
        self.rect = pygame.rect

    def draw(self, surf: pygame.Surface):
        w, h = GAME_SPACE
        center = (w // 2, h // 2)
        self.rect = self.game_over_sprite.get_rect(center=center)
        surf.blit(self.game_over_sprite, self.rect)
