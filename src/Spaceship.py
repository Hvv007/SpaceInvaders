import pygame
import os
from src.Config import *
from src.Missile import Missile


class Spaceship:
    def __init__(self):
        self.sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, SPACESHIP_SPRITE))
        self.rect = self.sprite.get_rect(center=SPACESHIP_STARTING_POSITION)
        self.destruction_sprite = pygame.image.load(os.path.join(SPRITE_DIRECTORY, SPACESHIP_EXPLOSION_SPRITE))
        self.moving_direction = MovingDirection.IDLE
        self.move_amount = 0
        self.is_active = True
        self.is_destroyed = False
        self.delay_since_explosion = 0
        self.is_firing = False
        self.missile = Missile()
        self.shots_count = 0
        self.invaders_killed = 0
        self.shoot_sound = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, SPACESHIP_SHOOT_SOUND))
        self.destruction_sound = pygame.mixer.Sound(os.path.join(SOUND_DIRECTORY, SPACESHIP_DESTRUCTION_SOUND))
        self.sound_is_muted = False
        self.missile_firing = False
        self.minigun_firing = False
        self.launcher_firing = False
        self.acc = 0

    def reset(self):
        self.rect = self.sprite.get_rect(center=SPACESHIP_STARTING_POSITION)
        self.moving_direction = MovingDirection.IDLE
        self.move_amount = 0
        self.is_active = True
        self.is_destroyed = False
        self.delay_since_explosion = 0
        self.is_firing = False

    def update(self, dt, events):
        self.handle_input(events)
        if not self.is_destroyed:
            self.move(dt)
            self.update_missile(dt)
            self.fire()
        else:
            self.delay_since_explosion += dt
            if self.is_destroyed and self.delay_since_explosion > SPACESHIP_EXPLOSION_DURATION_MS:
                self.is_active = False

    def draw(self, surf: pygame.Surface):
        if self.is_active:
            if self.is_destroyed:
                self.destruction_sprite = pygame.transform.flip(self.destruction_sprite, True, False)
                surf.blit(self.destruction_sprite, self.rect)
            else:
                surf.blit(self.sprite, self.rect)
        if self.missile.is_active:
            self.missile.draw(surf)

    def handle_input(self, events):
        accel_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            accel_x -= 0.1
        if keys[pygame.K_d]:
            accel_x += 0.1
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            accel_x = 0
        self.acc += accel_x
        if abs(self.acc) >= SPACESHIP_MAX_SPEED:
            self.acc = self.acc / abs(self.acc) * SPACESHIP_MAX_SPEED
        if accel_x == 0:
            if self.acc > 0:
                self.acc *= 0.99
            else:
                self.acc *= 0.97
            if 0 > self.acc > -.1 or 0 < self.acc < .1:
                self.acc = 0
        if keys[pygame.K_SPACE]:
            self.is_firing = True
            self.missile_firing = True
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_firing = True
                    self.missile_firing = True
                if event.key == pygame.K_RALT:
                    self.is_firing = True
                    self.launcher_firing = True
                if event.key == pygame.K_RCTRL:
                    self.is_firing = True
                    self.minigun_firing = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.is_firing = False
                    self.missile_firing = False
                if event.key == pygame.K_RALT:
                    self.is_firing = False
                    self.launcher_firing = False
                if event.key == pygame.K_RCTRL:
                    self.is_firing = False
                    self.minigun_firing = False

    def move(self, dt):
        self.move_amount += dt / 1000 * SPACESHIP_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            self.rect.x += int(self.move_amount) * self.acc
            self.move_amount -= int(self.move_amount)

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right >= GAME_SPACE[0]:
                self.rect.right = GAME_SPACE[0] - 1

    def update_missile(self, dt):
        if not self.missile.is_active:
            return
        self.missile.update(dt, self.acc)
        if self.missile.time_since_explosion > INVADER_EXPLOSION_DURATION_MS:
            self.missile.set_inactive()

    def fire(self):
        if not self.is_firing or self.missile.is_active:
            return
        self.shots_count += 1
        if self.missile_firing:
            self.launch_missile()
        if self.launcher_firing:
            self.launch_launcher()
        if self.minigun_firing:
            self.launch_minigun()
        if not self.sound_is_muted:
            self.shoot_sound.play()

    def destroy(self):
        self.is_destroyed = True
        if not self.sound_is_muted:
            self.destruction_sound.play()

    def launch_missile(self):
        missile_rect = pygame.Rect(self.rect.centerx - (MISSILE_RECT_DIM[0] // 2),
                                   self.rect.top - MISSILE_RECT_DIM[1],
                                   MISSILE_RECT_DIM[0],
                                   MISSILE_RECT_DIM[1])
        self.missile.missile_type = 'default'
        self.missile.launch(missile_rect)

    def launch_launcher(self):
        missile_rect = pygame.Rect(self.rect.centerx - (MISSILE_RECT_DIM[0] // 2),
                                   self.rect.top - MISSILE_RECT_DIM[1],
                                   MISSILE_RECT_DIM[0]*3,
                                   MISSILE_RECT_DIM[1]*3)
        self.missile.missile_type = 'launcher'
        self.missile.launch(missile_rect)

    def launch_minigun(self):
        missile_rect = pygame.Rect(self.rect.centerx - (MISSILE_RECT_DIM[0] // 2),
                                   self.rect.top - MISSILE_RECT_DIM[1],
                                   MISSILE_RECT_DIM[0],
                                   MISSILE_RECT_DIM[1])
        self.missile.missile_type = 'minigun'
        self.missile.launch(missile_rect)

