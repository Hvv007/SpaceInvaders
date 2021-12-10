import random
import pygame
from Config import *
from Mystery_ship import MysteryShip
from Laser import Laser


class Invader:
    def __init__(self, invader_type: int, top_left_pos):
        self.invader_type = invader_type
        self.sprites = [pygame.image.load(SPRITE_DIRECTORY + s) for s in INVADER_SPRITES[self.invader_type - 1]]
        self.explosion_sprite = pygame.image.load(SPRITE_DIRECTORY + INVADER_EXPLOSION_SPRITE)
        self.sprite_index = 0
        self.rect = self.sprites[self.sprite_index].get_rect(topleft=top_left_pos)
        self.last_sprite_shift_delay = 0
        self.shift_sprite_period = INVADER_SPRITE_SHIFT_PERIOD_MS
        self.move_amount = 0
        self.delay_since_explosion = 0
        self.is_exploded = False
        self.destruction_sound = pygame.mixer.Sound(SOUND_DIRECTORY + INVADER_DESTRUCTION_SOUND)

    def update(self, dt, movement):
        if self.is_exploded:
            self.delay_since_explosion += dt
        self.move(movement)
        self.sprite_shift(dt)

    def move(self, movement):
        self.rect.top += movement[1]
        self.rect.left += movement[0]

    def sprite_shift(self, dt):
        self.last_sprite_shift_delay += dt
        if self.last_sprite_shift_delay > self.shift_sprite_period:
            self.sprite_index += 1
            self.sprite_index %= len(self.sprites)
            self.last_sprite_shift_delay -= self.shift_sprite_period

    def fire(self):
        return Laser((self.rect.centerx - (LASER_RECT_DIM[0] // 2), self.rect.bottom), self.invader_type - 1)

    def draw(self, surf: pygame.Surface):
        if self.is_exploded:
            explosion_rect = self.explosion_sprite.get_rect()
            explosion_rect.center = self.rect.center
            surf.blit(self.explosion_sprite, explosion_rect)
        else:
            surf.blit(self.sprites[self.sprite_index], self.rect)

    def explode(self):
        self.is_exploded = True
        self.destruction_sound.play()


class Invaders:
    def __init__(self):
        self.invaders_list = self.make_invaders_list()
        self.mystery_ship = MysteryShip()
        self.rect = self.get_rect()
        self.lasers = []
        self.movement_direction = MovingDirection.RIGHT
        self.last_movement_sequence_delay = 0
        self.movement_speed = INVADER_SPEED_PIXEL_PER_SECOND
        self.move_amount = 0
        self.last_firing_delay = 0
        self.last_mystery_ship_appearing_delay = 0
        self.starting_invaders_count = len(self.invaders_list)
        self.speed_up_level = 0
        self.mystery_ships_count = 0
        self.move_sounds = [pygame.mixer.Sound(SOUND_DIRECTORY + sound) for sound in INVADERS_MOVE_SOUNDS]
        self.move_sounds[0].play(loops=-1)

    def __iter__(self):
        return self.invaders_list.__iter__()

    def __next__(self):
        return next(self.__iter__())

    def get_rect(self):
        if not self.invaders_list:
            return pygame.Rect((0, 0), (0, 0))
        top_left_x = min(invader.rect.left for invader in self.invaders_list)
        top_left_y = min(invader.rect.top for invader in self.invaders_list)
        bottom_right_x = max(invader.rect.right for invader in self.invaders_list)
        bottom_right_y = max(invader.rect.bottom for invader in self.invaders_list)
        rect = pygame.Rect(top_left_x, top_left_y,
                           bottom_right_x - top_left_x, bottom_right_y - top_left_y)
        return rect

    def draw(self, surf):
        for invader in self.invaders_list:
            invader.draw(surf)
        for laser in self.lasers:
            laser.draw(surf)
        self.mystery_ship.draw(surf)

    def update(self, dt):
        self.update_invaders(dt)
        self.update_lasers(dt)
        self.update_mystery_ship(dt)
        if not self.invaders_list:
            self.reset()

    def update_invaders(self, dt):
        self.fire(dt)
        self.speed_up()
        self.remove_invaders()
        self.update_invader(dt)

    def reset(self):
        self.move_sounds[self.speed_up_level].stop()
        self.invaders_list = self.make_invaders_list()
        self.rect = self.get_rect()
        self.lasers = []
        self.movement_direction = MovingDirection.RIGHT
        self.last_movement_sequence_delay = 0
        self.move_amount = 0
        self.movement_speed = INVADER_SPEED_PIXEL_PER_SECOND
        self.last_firing_delay = 0
        self.last_mystery_ship_appearing_delay = 0
        self.speed_up_level = 0
        self.mystery_ships_count = 0
        self.move_sounds[0].play(loops=-1)

    def fire(self, dt):
        self.last_firing_delay += dt
        while self.last_firing_delay > INVADER_FIRING_PERIOD_MS:
            self.last_firing_delay -= INVADER_FIRING_PERIOD_MS
            firing_invaders = self.find_firing_invaders()
            if not firing_invaders:
                return
            invader = random.choice(firing_invaders)
            self.lasers.append(invader.fire())

    def find_firing_invaders(self):
        invaders_columns = set(invader.rect.centerx for invader in self.invaders_list)
        invader_dict = {column: [] for column in invaders_columns}
        for invader in self.invaders_list:
            invader_dict[invader.rect.centerx].append(invader)

        lowest_invaders = []
        for column in invaders_columns:
            lowest_invader = None
            max_invader_y = 0
            for invader in invader_dict[column]:
                if invader.rect.bottom > max_invader_y:
                    lowest_invader = invader
                    max_invader_y = invader.rect.bottom
            if lowest_invader:
                lowest_invaders.append(lowest_invader)
        return lowest_invaders

    def speed_up(self):
        if len(self.invaders_list) <= self.starting_invaders_count // (2 ** (self.speed_up_level + 1)):
            self.move_sounds[self.speed_up_level].stop()
            self.speed_up_level += 1
            self.move_sounds[self.speed_up_level].play(loops=-1)
            self.movement_speed *= 2
            for invader in self.invaders_list:
                invader.shift_sprite_period = invader.shift_sprite_period // 2

    def remove_invaders(self):
        for invader in self.invaders_list:
            if invader.delay_since_explosion > INVADER_EXPLOSION_DURATION_MS:
                self.invaders_list.remove(invader)

    def update_invader(self, dt):
        if not self.invaders_list:
            return
        movement = self.get_invader_movement(dt)
        for invader in self.invaders_list:
            invader.update(dt, movement)

    def get_invader_movement(self, dt):
        movement_direction_values = self.movement_direction[0]
        self.move_amount += dt / 1000 * self.movement_speed
        movement = (0, 0)
        if self.move_amount > 1.:
            movement = int(self.move_amount) * movement_direction_values
            self.move_amount -= int(self.move_amount)

        self.rect = self.get_rect()
        self.rect.left += movement[0]
        self.rect.top += movement[1]
        if self.movement_direction == MovingDirection.RIGHT and self.rect.right >= GAME_SPACE[0]:
            movement = (movement[0] - (self.rect.right - GAME_SPACE[0]), movement[1] + self.invaders_list[0].rect.h)
            self.movement_direction = MovingDirection.LEFT
        if self.movement_direction == MovingDirection.LEFT and self.rect.left <= 0:
            movement = (movement[0] - self.rect.left, movement[1] + self.invaders_list[0].rect.h)
            self.movement_direction = MovingDirection.RIGHT
        return movement

    def update_lasers(self, dt):
        for laser in self.lasers:
            laser.update(dt)
            if laser.rect.bottom >= GAME_SPACE[1]:
                laser.explode()
            if laser.is_exploded and laser.time_since_explosion > INVADER_EXPLOSION_DURATION_MS:
                self.lasers.remove(laser)
                continue

    def update_mystery_ship(self, dt):
        self.last_mystery_ship_appearing_delay += dt
        if self.last_mystery_ship_appearing_delay > MYSTERY_SHIP_APPEAR_PERIOD_SECONDS * 1000 \
                and len(self.invaders_list) > 7:
            self.last_mystery_ship_appearing_delay -= MYSTERY_SHIP_APPEAR_PERIOD_SECONDS * 1000
            self.launch_mystery_ship()

        if not self.mystery_ship.is_active:
            return
        self.mystery_ship.update(dt)
        if self.mystery_ship.rect.x > GAME_SPACE[0] or self.mystery_ship.rect.right < 0:
            self.mystery_ship.set_inactive()

        if self.mystery_ship.is_exploded \
                and self.mystery_ship.time_since_explosion > self.mystery_ship.explosion_duration:
            self.mystery_ship.set_inactive()

    def launch_mystery_ship(self):
        possible_x = [0, GAME_SPACE[0] - self.mystery_ship.rect.w]
        possible_direction = [MovingDirection.RIGHT, MovingDirection.LEFT]
        index = random.choice([0, 1])
        x = possible_x[index]
        y = MYSTERY_SHIP_STARTING_POS_Y
        direction = possible_direction[index]
        self.mystery_ships_count += 1
        self.mystery_ship.launch((x, y), direction)

    @staticmethod
    def make_invaders_list():
        invaders = []
        invader_sprites = \
            [[pygame.image.load(SPRITE_DIRECTORY + sprite) for sprite in sprites] for sprites in INVADER_SPRITES]
        max_w = max([sprites[0].get_rect().w for sprites in invader_sprites])
        max_row_size = max([len(row) for row in INVADER_FORMATION])
        step = INVADER_FORMATION_WIDTH_PIXELS / max_row_size
        x0 = (-max_w) // 2 + (GAME_SPACE[0] - INVADER_FORMATION_WIDTH_PIXELS) // 2
        xs = [x0 + (step * i) for i in range(max_row_size)]
        for row_index, invader_row in enumerate(INVADER_FORMATION):
            for i, invader_index in enumerate(invader_row):
                sprites = invader_sprites[invader_index - 1]
                w, h = (sprites[0].get_rect().w, sprites[0].get_rect().h)
                center_x = xs[i]
                center_y = h + (2 * h * row_index) + INVADER_STARTING_POS_Y
                invaders.append(Invader(invader_index, (center_x - w // 2, center_y - h // 2)))
        return invaders
