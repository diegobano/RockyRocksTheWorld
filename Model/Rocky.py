#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BallPower import BallPower
from Character import Character
from Counter import Counter
from FirePower import FirePower
from NullPower import NullPower
from PlayerPoints import PlayerPoints
import os
import pygame as pyg

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"


class Rocky(Character):
    def __init__(self, lives, initial_x, initial_y, w_width, w_height, speed, acceleration, front_image, back_image,
                 blink_image, dmg_image1, dmg_image2, ball_image1, ball_image2, fire_image1, fire_image2, numbers,
                 counter, jump_sound, landing_sound, bump_sound, win_sound, hit_sound, fire_sound):
        Character.__init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration,
                           front_image.get_size()[0])
        # Useful variables
        self.points = PlayerPoints(numbers)
        self.last_blink = 0
        self.restart_level = False
        self.end_of_the_level = False
        self.counter = Counter(self.window_width - 50, counter, numbers)
        self.heart_pos = [self.window_width / 2 - front_image.get_size()[0] * 2, 5]
        self.jump_speed = -13
        self.pos_ini = [initial_x, initial_y]

        # Sounds
        self.jump_sound = jump_sound
        self.landing_sound = landing_sound
        self.bump_sound = bump_sound
        self.win_sound = win_sound
        self.hit_sound = hit_sound
        self.fire_sound = fire_sound

        # Different power states
        self.transforming = False
        self.null_power = NullPower(self, 0)
        self.ball_power = BallPower(self, 1)
        self.fire_power = FirePower(self, 2)
        self.current_power = self.null_power
        self.last_power = self.current_power
        self.current_state = 0
        self.fireballs = []
        self.checked = False

        # Characteristics
        self.lives = lives
        self.attack = 1

        # Collision variables
        self.jumping = False
        self.facing_forward = True
        self.on_the_floor = False
        self.getting_damage = False
        self.dmg_moment = 0
        self.dmg_time = 800
        self.last_change = 0
        self.current_dmg_sprite = 0
        self.floor_level = 0
        self.right_wall_bound = 0
        self.left_wall_bound = 0

        # Sprites
        self.heart = pyg.image.load(os.path.join("Resources/Misc/life.png"))
        self.heart = pyg.transform.scale(self.heart,
                                         ((self.get_bound_x() - self.x) / 2, (self.get_bound_x() - self.x) / 2))
        self.heart.convert()
        self.front_sprites = [front_image, ball_image1, fire_image1]
        self.back_sprites = [back_image, ball_image2, fire_image2]
        self.blink = blink_image
        self.dmg_sprites = [dmg_image1, dmg_image2]
        # sprite being displayed
        self.sprite = self.front_sprites[0]
        self.last_state = self.sprite

    def jump(self):
        self.speed_y = self.current_power.jump_speed
        self.jumping = True
        self.on_the_floor = False
        self.jump_sound.play()

    def set_player_points(self, numbers):
        self.points = PlayerPoints(numbers)

    def check_collisions(self, level):
        self.check_in_bounds(level)

    def fix_position(self):
        # Fix wall collisions
        if self.x < 0:
            self.x = 0

        if self.get_bound_x() > self.window_width:
            self.x = self.window_width - (self.get_bound_x() - self.x)

        if self.get_bound_y() >= self.window_height and self.floor_level >= self.window_height:
            self.sprite = self.dmg_sprites[0]
            self.fall_down()

        # Fix floor collisions
        if self.get_bound_y() > self.floor_level and self.speed_y > 0:
            self.y = self.floor_level - (self.get_bound_y() - self.get_y())
            self.speed_y = 0

    def get_hit(self):
        if self.current_power.is_null_power() and not self.checked:
            self.checked = True
            self.restart_level = True
        self.last_state = self.sprite
        self.sprite = self.dmg_sprites[0]
        self.getting_damage = True
        self.back_to_normal()
        self.jump()
        self.dmg_moment = self.current_time_millis()
        self.last_change = self.dmg_moment
        if self.speed_x >= 0:
            self.move_left()
        else:
            self.move_right()
        if self.is_alive():
            self.hit_sound.play()

    def fall_down(self):
        self.restart_level = True

    def back_to_normal(self):
        self.current_state = 0
        self.current_power.back_to_normal()
        self.current_power = self.null_power

    def has_power(self):
        return not self.current_power.is_null_power()

    def set_power(self, power):
        self.current_power = power

    def throw_fireball(self):
        if self.current_power.is_fire():
            if Character.current_time_millis() - self.current_power.last_fire >= self.current_power.fire_rest:
                self.fire_sound.play()
                self.current_power.shoot_fire()

    def stop_getting_damage(self):
        self.sprite = self.last_state
        self.getting_damage = False
        self.speed_x = 0
        self.current_dmg_sprite = 0
        self.back_to_normal()

    def get_potato_bonus(self):
        self.points.add_points(5)
        self.last_power = self.current_power
        self.ball_power.get_power()

    def get_spike_bonus(self):
        self.points.add_points(10)
        self.last_power = self.current_power
        self.fire_power.get_power()

    def get_points_bonus(self, enemy):
        self.points.add_points(enemy.get_points())

    def to_last_power(self):
        self.current_power = self.last_power
        self.current_state = self.current_power.rocky_state

    def change_damage_sprite(self):
        self.current_dmg_sprite = 1 - self.current_dmg_sprite
        self.sprite = self.dmg_sprites[self.current_dmg_sprite]
        self.last_change = self.current_time_millis()

    def check_in_bounds(self, level):
        squares = level.updated_squares()
        max_height = 100000000
        for square in squares:
            top_right_corner = [square[0] + square[2], square[1]]
            bottom_left_corner = [square[0], square[1] + square[3]]

            if top_right_corner[0] - 10 < self.x < top_right_corner[0]:
                if not bottom_left_corner[0] < self.get_bound_x() < bottom_left_corner[0] + 10:
                    if self.get_bound_y() > top_right_corner[1]:
                        self.x = top_right_corner[0] + 1
                        self.speed_x = 0
                        self.bump_sound.play()
            else:
                if bottom_left_corner[0] < self.get_bound_x() < bottom_left_corner[0] + 10:
                    if self.get_bound_y() > top_right_corner[1]:
                        self.x = bottom_left_corner[0] - (self.get_bound_x() - self.x) - 1
                        self.speed_x = 0
                        self.bump_sound.play()

            if bottom_left_corner[0] < self.x < top_right_corner[0] or bottom_left_corner[0] <= self.get_bound_x() <= \
                    top_right_corner[0]:
                if top_right_corner[1] < max_height:
                    max_height = top_right_corner[1]

        prev = self.on_the_floor
        self.on_the_floor = max_height <= self.get_bound_y()
        self.floor_level = max_height
        if (prev != self.on_the_floor) and self.on_the_floor and not self.jumping:
            self.landing_sound.play()
        # Fix floor collisions
        if self.on_the_floor and self.speed_y > 0:
            self.speed_y = 0
            self.y = self.floor_level - (self.get_bound_y() - self.get_y())

        if (level.flag_x <= self.x <= level.get_flag_bound_x()
            or level.flag_x <= self.get_bound_x() <= level.get_flag_bound_x()) and \
                (level.flag_y <= self.y <= level.get_flag_bound_y()
                 or level.flag_y <= self.y <= level.get_flag_bound_y()):
            self.end_of_the_level = True
            self.points.add_points(self.counter.remaining)

    def update(self, level, enemies):
        self.counter.update()
        if self.counter.remaining <= 0:
            self.get_hit()
        if not self.getting_damage:
            if self.transforming:
                self.current_power.check_transformation()
            else:
                self.checked = False
                # Move horizontally if inside the window
                if self.window_width >= self.get_bound_x() and self.x >= 0:
                    # if in the middle, move level
                    if ((self.get_bound_x() >= self.window_width / 2 + 30 and self.speed_x > 0) or
                            (self.x <= self.window_width / 2 - 30 and self.speed_x < 0)) and \
                            not (-1 < level.x and self.speed_x < 0) and not \
                            (self.speed_x > 0 and level.x < - (level.width - level.window_width) + 1):
                        level.move_level(-self.speed_x, enemies)
                        for fire in self.fireballs:
                            fire.move(-self.speed_x)
                    # Else move rocky
                    else:
                        self.x += self.speed_x
                # Move vertically
                self.y += self.speed_y

                # Add acceleration in y if in the air
                if not self.on_the_floor and self.speed_y < -self.jump_speed:
                    self.speed_y += self.acceleration

                # If no more lives, kill rocky
                if self.lives == 0:
                    self.kill()

                # Change current sprite according to the situation
                if self.facing_forward:
                    self.sprite = self.front_sprites[self.current_state]
                else:
                    self.sprite = self.back_sprites[self.current_state]

                # Update or remove fireballs
                for fire in self.fireballs:
                    fire.update(level)
                    if not fire.is_alive():
                        self.fireballs.remove(fire)
        # While suffering damage
        else:
            # Move horizontally if inside window
            if self.window_width >= self.get_bound_x() and self.x >= 0:
                # if in the middle, move level
                if self.window_width / 2 + 20 >= (self.x + self.get_bound_x()) / 2 >= self.window_width / 2 - 20 and \
                        not (-1 < level.x and self.speed_x < 0) and \
                        not (self.speed_x > 0 and level.x < -(level.width - level.window_width) + 1):
                    level.move_level(-self.speed_x, enemies)
                # Else move rocky
                else:
                    self.x += self.speed_x
            # Update damage sprite
            if self.current_time_millis() - self.last_change >= 50:
                self.change_damage_sprite()

            # Update vertical movement
            self.y += self.speed_y
            if not self.on_the_floor:
                self.speed_y += self.acceleration

            # If no more lives, kill rocky
            if self.lives == 0:
                self.kill()
        self.fix_position()

    def restart(self):
        self.lives -= 1
        self.x = self.pos_ini[0]
        self.y = self.pos_ini[1]
        self.speed_x = 0
        self.speed_y = 0
        self.counter.restart()

        # Useful variables
        self.points.restart()
        self.last_blink = 0
        self.restart_level = False
        self.end_of_the_level = False

        # Different power states
        self.transforming = False
        self.current_power = self.null_power
        self.current_state = 0
        self.fireballs = []
        self.checked = False

        # Collision variables
        self.jumping = False
        self.facing_forward = True
        self.on_the_floor = False
        self.getting_damage = False
        self.dmg_moment = 0
        self.dmg_time = 800
        self.last_change = 0
        self.current_dmg_sprite = 0
        self.floor_level = 0
        self.right_wall_bound = 0
        self.left_wall_bound = 0

        # Sprite being displayed
        self.sprite = self.front_sprites[0]
        self.last_state = self.sprite

    def draw(self, bg):
        for fire in self.fireballs:
            fire.draw(bg)
        bg.blit(self.sprite, (int(self.x), int(self.y)))
        for i in range(self.lives):
            bg.blit(self.heart, (self.heart_pos[0] + i * (self.heart.get_size()[0] + 2), self.heart_pos[1]))
        self.points.draw(bg)
        self.counter.draw(bg)
