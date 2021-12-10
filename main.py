import sys
import pygame
import math
import random
from Config import *
from Invaders import Invaders
from Bunkers import Bunkers
from Spaceship import Spaceship
from GUI import LifeCounter, Score


class SpaceInvaders:
    def __init__(self):
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.player_ship = Spaceship()
        self.invaders = Invaders()
        self.bunkers = Bunkers()
        self.life_counter = LifeCounter()
        self.game_over_flag = False
        self.update_time_delay = 1
        self.draw_time_delay = 1
        self.score = Score('score')
        self.high_score = Score('high_score')

    def play(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick()
            update_count = self.get_update_count(dt)
            if update_count > 0:
                self.update(update_count * UPDATE_PERIOD_MS)
                self.update_life_count()
                self.collide()
            frame_count = self.get_frame_count(dt)
            if frame_count > 0:
                self.draw()

    def game_over(self):
        self.game_over_flag = True
        if self.score.value > self.high_score.value:
            self.high_score.value = self.score.value

    def reset(self):
        self.player_ship = Spaceship()
        self.invaders.reset()
        self.bunkers = Bunkers()
        self.life_counter = LifeCounter()
        self.game_over_flag = False
        self.score = Score('score')

    def update(self, dt):
        events = self.get_inputs()
        self.player_ship.update(dt, events)
        self.invaders.update(dt)

    def get_inputs(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    self.reset()
            events.append(event)
        return events

    def draw(self):
        self.window.fill((0, 0, 0))
        self.bunkers.draw(self.window)
        self.player_ship.draw(self.window)
        self.invaders.draw(self.window)
        self.life_counter.draw(self.window)
        self.score.draw(self.window)
        self.high_score.draw(self.window)
        pygame.display.flip()

    def update_life_count(self):
        if not self.player_ship.is_active:
            if self.life_counter.life_count > 0:
                self.life_counter.life_count -= 1
                self.player_ship.reset()
            else:
                self.game_over()

    def get_update_count(self, dt):
        self.update_time_delay += dt
        update_count = self.update_time_delay // UPDATE_PERIOD_MS
        self.update_time_delay = self.update_time_delay % UPDATE_PERIOD_MS
        return update_count

    def get_frame_count(self, dt):
        self.draw_time_delay += dt
        frame_count = self.draw_time_delay // DRAW_PERIOD_MS
        self.draw_time_delay = self.draw_time_delay % DRAW_PERIOD_MS
        return frame_count

    def collide(self):
        self.collide_missile_and_invaders()
        self.collide_spaceship_and_invaders()
        self.collide_spaceship_and_lasers()
        self.collide_missile_and_lasers()
        self.collide_missile_and_bunkers()
        self.collide_laser_and_bunkers()
        self.collide_invaders_and_bunkers()
        self.collide_missile_and_mystery_ship()

    def collide_missile_and_invaders(self):
        if not self.player_ship.missile.is_active:
            return
        missile_rect = self.player_ship.missile.rect
        for invader in self.invaders:
            if missile_rect.colliderect(invader.rect):
                invader.explode()
                self.player_ship.missile.is_active = False
                self.score.value += invader.invader_type * 10

    def collide_missile_and_mystery_ship(self):
        if not self.player_ship.missile.is_active or not self.invaders.mystery_ship.is_active:
            return
        missile_rect = self.player_ship.missile.rect
        mystery_ship_rect = self.invaders.mystery_ship.rect
        if missile_rect.colliderect(mystery_ship_rect):
            self.invaders.mystery_ship.explode()
            self.player_ship.missile.is_active = False
            self.score.value += 100

    def collide_spaceship_and_invaders(self):
        for invader in self.invaders:
            if self.player_ship.is_destroyed:
                return
            if invader.rect.colliderect(self.player_ship.rect):
                self.player_ship.destroy()

    def collide_spaceship_and_lasers(self):
        if self.player_ship.is_destroyed:
            return
        laser_rect_list = [laser.rect for laser in self.invaders.lasers]
        if self.player_ship.rect.collidelist(laser_rect_list) != - 1:
            self.player_ship.destroy()

    def collide_missile_and_lasers(self):
        if not self.player_ship.missile.is_active:
            return
        laser_rect_list = [laser.rect for laser in self.invaders.lasers]
        laser_index = self.player_ship.missile.rect.collidelist(laser_rect_list)
        if laser_index != -1:
            self.player_ship.missile.explode()
            self.invaders.lasers[laser_index].explode()

    def collide_missile_and_bunkers(self):
        if not self.player_ship.missile.is_active:
            return
        if self.collide_with_bunkers(self.player_ship.missile, MISSILE_BUNKER_EXPLOSION_RADIUS):
            self.player_ship.missile.is_active = False

    def collide_laser_and_bunkers(self):
        for laser in self.invaders.lasers:
            if self.collide_with_bunkers(laser, LASER_BUNKER_EXPLOSION_RADIUS):
                laser.explode()

    def collide_invaders_and_bunkers(self):
        for invader in self.invaders:
            self.collide_with_bunkers(invader, LASER_BUNKER_EXPLOSION_RADIUS)

    def collide_with_bunkers(self, shoot, radius):
        for bunker in self.bunkers:
            # Find a colliding pixel
            collision_point = self.find_colliding_point(shoot, bunker)
            if collision_point:
                self.apply_explosion_on_mask(collision_point, radius, bunker)
                self.build_sprite_from_mask(bunker)
                return True
        return False

    @staticmethod
    def find_colliding_point(colliding_entity, bunker):
        # получаем вектор растояния между левым верхним углом бункера и сталкивающемся объектом
        x, y = colliding_entity.rect.x, colliding_entity.rect.y
        offset = (x - bunker.rect.x, y - bunker.rect.y)

        w, h = (colliding_entity.rect.w, colliding_entity.rect.h)
        colliding_entity_mask = pygame.Mask((w, h), fill=True)
        # возвращает точку пересечения, если есть
        return bunker.mask.overlap(colliding_entity_mask, offset)

    @staticmethod
    def apply_explosion_on_mask(collision_point, radius, bunker):
        collision_x, collision_y = collision_point
        bunker.mask.set_at((collision_x, collision_y), 0)

        for x in range(collision_x - radius, collision_x + radius + 1, 1):
            for y in range(collision_y - radius, collision_y + radius + 1, 1):
                if x < 0 or x >= bunker.rect.w or y < 0 or y >= bunker.rect.h:
                    continue

                # проверяем попадает ли в круг вокруг точки столкновения
                if math.sqrt((x - collision_x) ** 2 + (y - collision_y) ** 2) > radius:
                    continue

                # с какой-то вероятностью убираем пиксели
                # попытался сделать похоже на оригинал, но ещё стоит поиграться с цифрами вероятности и радиуса
                if random.random() < BUNKER_DESTRUCTION_PROBABILITY:
                    bunker.mask.set_at((x, y), 0)

    @staticmethod
    def build_sprite_from_mask(bunker):
        # 3-мерный потому что цвет задаётся 3 значениями
        surf_array = pygame.surfarray.array3d(bunker.sprite)
        for y in range(bunker.rect.h):
            for x in range(bunker.rect.w):
                if bunker.mask.get_at((x, y)) == 0:
                    surf_array[x, y] = (0, 0, 0)
        bunker.sprite = pygame.surfarray.make_surface(surf_array)


if __name__ == "__main__":
    pygame.init()
    game = SpaceInvaders()
    game.play()
