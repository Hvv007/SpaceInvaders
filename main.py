import sys
import pygame
import math
import random
from src.Config import *
from src.Invaders import Invaders
from src.Bunkers import Bunkers
from src.Spaceship import Spaceship
from src.GUI import LifeCounter, Score, GameOver


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
        self.game_over_screen = GameOver()
        self.game_is_muted = False
        self.cheats_flag = False
        self.cheats_on = [False]*3
        self.cheats_off = [False]*3

    def play(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick()
            if self.game_over_flag:
                self.draw_time_delay = 0
                self.game_over_screen.draw(self.window)
                pygame.display.flip()
            update_count = self.get_update_count(dt)
            if update_count > 0:
                self.update(update_count * UPDATE_PERIOD_MS)
                self.update_life_count()
                self.check_collision()
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
        self.mute_unmute()

    def update(self, dt):
        events = self.get_inputs(pygame.event.get())
        self.player_ship.update(dt, events)
        self.invaders.update(dt)

    def get_inputs(self, input_events):
        events = []
        for event in input_events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_m:
                    self.game_is_muted = not self.game_is_muted
                    self.mute_unmute()
                if self.cheats_flag is False and event.key == pygame.K_y:
                    self.cheats_on[0] = True
                if self.cheats_flag is False and event.key == pygame.K_u:
                    self.cheats_on[1] = True
                if self.cheats_flag is False and event.key == pygame.K_i:
                    self.cheats_on[2] = True
                if self.cheats_flag is True and event.key == pygame.K_h:
                    self.cheats_off[0] = True
                if self.cheats_flag is True and event.key == pygame.K_j:
                    self.cheats_off[1] = True
                if self.cheats_flag is True and event.key == pygame.K_k:
                    self.cheats_off[2] = True
                if self.cheats_flag and event.key == pygame.K_EQUALS:
                    if self.life_counter.life_count < 9:
                        self.life_counter.life_count += 1
                if self.cheats_flag and event.key == pygame.K_MINUS:
                    if self.life_counter.life_count > 0:
                        self.life_counter.life_count -= 1
                if self.cheats_flag and event.key == pygame.K_0:
                    for i in range(0, len(self.invaders.invaders_list), 2):
                        if not self.invaders.invaders_list[i].is_exploded:
                            self.invaders.invaders_list[i].explode()
                if self.cheats_flag and event.key == pygame.K_9 and not self.invaders.mystery_ship.is_active:
                    self.invaders.launch_mystery_ship()
            if len([True for i in self.cheats_on if i is True]) == 3:
                self.cheats_flag = True
                self.cheats_on = [False]*3
            if len([True for i in self.cheats_off if i is True]) == 3:
                self.cheats_flag = False
                self.cheats_off = [False]*3
            events.append(event)
        return events

    def mute_unmute(self):
        self.player_ship.sound_is_muted = self.game_is_muted
        self.invaders.sound_is_muted = self.game_is_muted
        if self.game_is_muted:
            self.invaders.move_sounds[self.invaders.speed_up_level].stop()
            self.invaders.mystery_ship.move_sound.stop()
        else:
            self.invaders.move_sounds[self.invaders.speed_up_level].play()
            if self.invaders.mystery_ship.is_active:
                self.invaders.mystery_ship.move_sound.play(loops=-1)
        for invader in self.invaders:
            invader.sound_is_muted = self.game_is_muted
        self.invaders.mystery_ship.sound_is_muted = self.game_is_muted

    def draw(self):
        self.window.fill((0, 0, 0))
        if self.cheats_flag:
            self.window.blit(self.score.digit_sprites[0], CHEATS_POS)
        self.bunkers.draw(self.window)
        self.player_ship.draw(self.window)
        self.invaders.draw(self.window)
        self.life_counter.draw(self.window)
        self.score.draw(self.window)
        self.high_score.draw(self.window)
        if any([True for invader in self.invaders if invader.rect.bottom >= WINDOW_SIZE[1]]):
            self.game_over()
        pygame.display.flip()

    def update_life_count(self):
        if self.score.value // 1500 > self.life_counter.extra_lives_count and self.life_counter.life_count < 9:
            self.life_counter.life_count += 1
            self.life_counter.extra_lives_count += 1
            if not self.game_is_muted:
                self.life_counter.extra_life_sound.play()
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

    def check_collision(self):
        self.check_missile_and_invaders_collision()
        self.check_spaceship_and_invaders_collision()
        self.check_spaceship_and_lasers_collision()
        self.check_missile_and_lasers_collision()
        self.check_missile_and_bunkers_collision()
        self.check_laser_and_bunkers_collision()
        self.check_invaders_and_bunkers_collision()
        self.check_missile_and_mystery_ship_collision()

    def check_missile_and_invaders_collision(self):
        active_missiles = [el for el in self.player_ship.minigun_missiles if el.is_active]
        if not self.player_ship.missile.is_active and not any(active_missiles):
            return
        launcher_hit = []
        if self.player_ship.missile.is_active:
            active_missiles.append(self.player_ship.missile)
        for missile in active_missiles:
            missile_rect = missile.rect
            for invader in self.invaders:
                if missile_rect.colliderect(invader.rect):
                    if missile.missile_type == 'launcher':
                        for invader_neighbour in self.invaders.invaders_list:
                            if abs(invader.rect.center[0] - invader_neighbour.rect.center[0]) < 35 and \
                                    invader.rect.center[1] == invader_neighbour.rect.center[1] or \
                                    abs(invader.rect.center[1] - invader_neighbour.rect.center[1]) < 35 and \
                                    invader.rect.center[0] == invader_neighbour.rect.center[0]:
                                launcher_hit.append(invader_neighbour)
                        for inv in launcher_hit:
                            inv.explode()
                    missile.set_inactive()
                    invader.explode()
                    self.score.value += invader.invader_type * 10
                    self.player_ship.invaders_killed += 1

    def check_missile_and_mystery_ship_collision(self):
        active_missiles = [el for el in self.player_ship.minigun_missiles if el.is_active]
        if (not self.player_ship.missile.is_active and not any(active_missiles)) \
                or not self.invaders.mystery_ship.is_active:
            return
        if self.player_ship.missile.is_active:
            active_missiles.append(self.player_ship.missile)
        for missile in active_missiles:
            missile_rect = missile.rect
            mystery_ship_rect = self.invaders.mystery_ship.rect
            if missile_rect.colliderect(mystery_ship_rect):
                if missile.missile_type == 'minigun':
                    self.invaders.mystery_ship.hp -= 1
                    missile.explode()
                    missile.draw(self.window)
                    missile.set_inactive()
                if self.invaders.mystery_ship.hp == 0 or missile.missile_type != 'minigun':
                    self.invaders.mystery_ship.explode()
                    missile.set_inactive()
                    if self.invaders.mystery_ships_count == 1 and self.player_ship.shots_count == 23 \
                            or self.invaders.mystery_ships_count > 1 and (self.player_ship.shots_count - 23) % 15 == 0:
                        self.score.value += 300
                    else:
                        self.score.value += 100

    def check_spaceship_and_invaders_collision(self):
        for invader in self.invaders:
            if self.player_ship.is_destroyed:
                return
            if invader.rect.colliderect(self.player_ship.rect):
                self.player_ship.destroy()

    def check_spaceship_and_lasers_collision(self):
        if self.player_ship.is_destroyed:
            return
        laser_rect_list = [laser.rect for laser in self.invaders.lasers]
        if self.player_ship.rect.collidelist(laser_rect_list) != - 1:
            self.player_ship.destroy()

    def check_missile_and_lasers_collision(self):
        active_missiles = [el for el in self.player_ship.minigun_missiles if el.is_active]
        if not self.player_ship.missile.is_active and not any(active_missiles):
            return
        if self.player_ship.missile.is_active:
            active_missiles.append(self.player_ship.missile)
        for missile in active_missiles:
            laser_rect_list = [laser.rect for laser in self.invaders.lasers]
            laser_index = missile.rect.collidelist(laser_rect_list)
            if laser_index != -1:
                missile.explode()
                self.invaders.lasers[laser_index].explode()

    def check_missile_and_bunkers_collision(self):
        active_missiles = [el for el in self.player_ship.minigun_missiles if el.is_active]
        if not self.player_ship.missile.is_active and not any(active_missiles):
            return
        if self.player_ship.missile.is_active:
            active_missiles.append(self.player_ship.missile)
        for missile in active_missiles:
            if self.check_collision_with_bunkers(missile, MISSILE_BUNKER_EXPLOSION_RADIUS):
                missile.set_inactive()

    def check_laser_and_bunkers_collision(self):
        for laser in self.invaders.lasers:
            if self.check_collision_with_bunkers(laser, LASER_BUNKER_EXPLOSION_RADIUS):
                laser.explode()

    def check_invaders_and_bunkers_collision(self):
        for invader in self.invaders:
            self.check_collision_with_bunkers(invader, LASER_BUNKER_EXPLOSION_RADIUS)

    def check_collision_with_bunkers(self, colliding_entity, radius):
        for bunker in self.bunkers:
            collision_point = self.find_colliding_point(colliding_entity, bunker)
            if collision_point:
                self.apply_explosion_on_mask(collision_point, radius, bunker)
                self.build_sprite_from_mask(bunker)
                return True
        return False

    @staticmethod
    def find_colliding_point(colliding_entity, bunker):
        x, y = colliding_entity.rect.x, colliding_entity.rect.y
        offset = (x - bunker.rect.x, y - bunker.rect.y)

        w, h = (colliding_entity.rect.w, colliding_entity.rect.h)
        colliding_entity_mask = pygame.Mask((w, h), fill=True)
        return bunker.mask.overlap(colliding_entity_mask, offset)

    @staticmethod
    def apply_explosion_on_mask(collision_point, radius, bunker):
        collision_x, collision_y = collision_point
        bunker.mask.set_at((collision_x, collision_y), 0)

        for x in range(collision_x - radius, collision_x + radius + 1, 1):
            for y in range(collision_y - radius, collision_y + radius + 1, 1):
                if x < 0 or x >= bunker.rect.w or y < 0 or y >= bunker.rect.h:
                    continue
                if math.sqrt((x - collision_x) ** 2 + (y - collision_y) ** 2) > radius:
                    continue
                if random.random() < BUNKER_DESTRUCTION_PROBABILITY:
                    bunker.mask.set_at((x, y), 0)

    @staticmethod
    def build_sprite_from_mask(bunker):
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
