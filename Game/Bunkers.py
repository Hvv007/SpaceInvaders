import pygame
from Game.Config import SPRITE_DIRECTORY, BUNKER_SPRITE, BUNKER_POSITIONS


class Bunker:
    def __init__(self, center):
        self.sprite = pygame.image.load(SPRITE_DIRECTORY + BUNKER_SPRITE)
        self.rect = self.sprite.get_rect(center=center)
        self.mask = pygame.mask.from_threshold(self.sprite, (0, 0, 0, 0), (1, 1, 1, 255))
        self.mask.invert()

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprite, self.rect)


class Bunkers:
    def __init__(self):
        self.bunkers_list = [Bunker(pos) for pos in BUNKER_POSITIONS]

    def draw(self, surf: pygame.Surface):
        for bunker in self.bunkers_list:
            bunker.draw(surf)

    def __iter__(self):
        return self.bunkers_list.__iter__()

    def __next__(self):
        return next(self.__iter__())
