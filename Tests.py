import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import unittest
import pygame
import random
from main import SpaceInvaders
from Config import *

pygame.init()
pygame.mixer.init()
game = SpaceInvaders()


class MyTestCase(unittest.TestCase):
    def test_starting_positions(self):
        game.draw()
        self.assertEqual([bunker.rect.center for bunker in game.bunkers], BUNKER_POSITIONS)
        self.assertEqual(game.player_ship.rect.center, SPACESHIP_STARTING_POSITION)
        game.invaders.launch_mystery_ship()
        self.assertIn(game.invaders.mystery_ship.rect.topleft,
                      [(0, MYSTERY_SHIP_STARTING_POS_Y),
                       (GAME_SPACE[0] - game.invaders.mystery_ship.rect.w, MYSTERY_SHIP_STARTING_POS_Y)])
        game.game_over_screen.draw(game.window)
        self.assertEqual(game.game_over_screen.rect.center, (GAME_SPACE[0] // 2, GAME_SPACE[1] // 2))
        game.reset()

    def test_inputs(self):
        game.life_counter.life_count = -1
        game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)])
        self.assertEqual(game.life_counter.life_count, STARTING_LIFE_COUNT)
        game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
        self.assertEqual(game.game_is_muted, True)
        game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m),
                         pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
        self.assertEqual(game.game_is_muted, True)
        self.assertEqual(game.player_ship.sound_is_muted, True)
        self.assertEqual(game.invaders.sound_is_muted, True)
        game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
        self.assertEqual(game.game_is_muted, False)
        self.assertEqual(game.player_ship.sound_is_muted, False)
        self.assertEqual(game.invaders.sound_is_muted, False)
        game.reset()

    def test_game_over_score_and_flag(self):
        test_number = random.randint(1, 9999)
        game.score.value = test_number
        game.game_over()
        self.assertEqual(game.high_score.value, test_number)
        self.assertEqual(game.game_over_flag, True)
        game.reset()
        game.score.value = test_number - 1
        game.game_over()
        self.assertEqual(game.high_score.value, test_number)
        self.assertEqual(game.game_over_flag, True)
        game.high_score.value = 0
        game.reset()

    def test_reset(self):
        test_number = random.randint(1, 1000)
        game.score.value = test_number
        game.life_counter.life_count -= 2
        test_invader_number = random.randint(0, 54)
        test_invader = game.invaders.invaders_list[test_invader_number]
        test_invader.explode()
        game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
        game.game_over()
        game.reset()
        self.assertEqual(game.game_over_flag, False)
        self.assertEqual(game.life_counter.life_count, STARTING_LIFE_COUNT)
        self.assertEqual(game.score.value, 0)
        self.assertEqual(game.high_score.value, test_number)
        self.assertNotEqual(test_invader.is_exploded, game.invaders.invaders_list[test_invader_number].is_exploded)
        self.assertEqual(game.game_is_muted, True)

