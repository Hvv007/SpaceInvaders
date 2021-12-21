import os
import random
import pygame
import pytest
from src.Config import *
from main import SpaceInvaders
from src.Spaceship import Spaceship

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ['SDL_AUDIODRIVER'] = 'dummy'
pygame.init()
pygame.mixer.init()


@pytest.fixture
def game():
    return SpaceInvaders()


@pytest.fixture
def spaceship():
    return Spaceship()


def test_starting_positions(game):
    game.draw()
    assert [bunker.rect.center for bunker in game.bunkers] == BUNKER_POSITIONS
    assert game.player_ship.rect.center == SPACESHIP_STARTING_POSITION
    game.invaders.launch_mystery_ship()
    assert game.invaders.mystery_ship.rect.topleft in \
           [(0, MYSTERY_SHIP_STARTING_POS_Y),
            (GAME_SPACE[0] - game.invaders.mystery_ship.rect.w, MYSTERY_SHIP_STARTING_POS_Y)]
    game.game_over_screen.draw(game.window)
    assert game.game_over_screen.rect.center == (GAME_SPACE[0] // 2, GAME_SPACE[1] // 2)


def test_game_inputs(game):
    game.life_counter.life_count = -1
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)])
    assert game.life_counter.life_count == STARTING_LIFE_COUNT
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
    assert game.game_is_muted is True
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m),
                     pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
    assert game.game_is_muted is True
    assert game.player_ship.sound_is_muted is True
    assert game.invaders.sound_is_muted is True
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
    assert game.game_is_muted is False
    assert game.player_ship.sound_is_muted is False
    assert game.invaders.sound_is_muted is False


def test_game_over_score_and_flag(game):
    test_number = random.randint(1, 9999)
    game.score.value = test_number
    game.game_over()
    assert game.high_score.value == test_number
    assert game.game_over_flag is True
    game.reset()
    game.score.value = test_number - 1
    game.game_over()
    assert game.high_score.value == test_number
    assert game.game_over_flag is True


def test_reset(game):
    test_number = random.randint(1, 1000)
    game.score.value = test_number
    game.life_counter.life_count -= 2
    test_invader_number = random.randint(0, 54)
    test_invader = game.invaders.invaders_list[test_invader_number]
    test_invader.explode()
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)])
    game.game_over()
    game.reset()
    assert game.game_over_flag is False
    assert game.life_counter.life_count == STARTING_LIFE_COUNT
    assert game.score.value == 0
    assert game.high_score.value == test_number
    assert test_invader.is_exploded != game.invaders.invaders_list[test_invader_number].is_exploded
    assert game.game_is_muted is True


def test_spaceship_inputs(spaceship):
    shots_before_input = spaceship.shots_count
    spaceship.update(11, [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE),
                          pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)])
    assert spaceship.missile.is_active is True
    assert spaceship.missile.move_amount == 0
    assert spaceship.missile.moving_direction == MovingDirection.UP
    assert spaceship.shots_count == shots_before_input + 1


def test_cheats_on_off(game):
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_y),
                     pygame.event.Event(pygame.KEYDOWN, key=pygame.K_u),
                     pygame.event.Event(pygame.KEYDOWN, key=pygame.K_i)])
    assert game.cheats_flag is True
    game.get_inputs([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h),
                     pygame.event.Event(pygame.KEYDOWN, key=pygame.K_j),
                     pygame.event.Event(pygame.KEYDOWN, key=pygame.K_k)])
    assert game.cheats_flag is False

