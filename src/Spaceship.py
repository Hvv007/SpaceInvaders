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
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving_direction = MovingDirection.LEFT
                if event.key == pygame.K_RIGHT:
                    self.moving_direction = MovingDirection.RIGHT
                if event.key == pygame.K_SPACE:
                    self.is_firing = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.moving_direction == MovingDirection.LEFT:
                    self.moving_direction = MovingDirection.IDLE
                if event.key == pygame.K_RIGHT and self.moving_direction == MovingDirection.RIGHT:
                    self.moving_direction = MovingDirection.IDLE
                if event.key == pygame.K_SPACE:
                    self.is_firing = False

    def move(self, dt):
        if self.moving_direction == MovingDirection.IDLE:
            return
        self.move_amount += dt / 1000 * SPACESHIP_SPEED_PIXEL_PER_SECOND
        if self.move_amount > 1.:
            direction = -1 if self.moving_direction == MovingDirection.LEFT else 1
            self.rect.x += int(self.move_amount) * direction
            self.move_amount -= int(self.move_amount)

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right >= GAME_SPACE[0]:
                self.rect.right = GAME_SPACE[0] - 1

    def update_missile(self, dt):
        if not self.missile.is_active:
            return
        self.missile.update(dt)
        if self.missile.rect.top < 0:
            self.missile.rect.top = 0
            self.missile.explode()

        if self.missile.time_since_explosion > INVADER_EXPLOSION_DURATION_MS:
            self.missile.set_inactive()

    def fire(self):
        if not self.is_firing or self.missile.is_active:
            return
        self.shots_count += 1
        self.launch_missile()
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
        self.missile.launch(missile_rect)
