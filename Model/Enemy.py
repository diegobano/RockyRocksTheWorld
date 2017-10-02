#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame as pyg
from Character import Character

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"


class Enemy(Character):
    def __init__(self, initial_x, initial_y, w_width, w_height, speed,
                 acceleration, front_image1, front_image2, back_image1, back_image2, squash_sound):
        Character.__init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration,
                           back_image1.get_size()[0])
        # Useful variables
        self.speeds = [speed, speed]
        self.speed_x = self.speed
        self.speed_y = 0
        self.pos_ini = [initial_x, initial_y]

        # Sound
        self.squash_sound = squash_sound

        # Characteristics
        self.lives = 1
        self.attack = 1
        self.last_change = 0
        self.walk_time = 250

        # Collision variables
        self.facing_forward = True
        self.on_the_floor = False
        self.bumping_left = False
        self.bumping_right = False
        self.floor_level = 0
        self.right_wall_bound = 0
        self.left_wall_bound = 0

        # Sprites
        self.current_sprite = 0
        self.front_sprites = [front_image1, front_image2]
        self.back_sprites = [back_image1, back_image2]
        # sprite being displayed
        self.sprite = self.front_sprites[0]

    def flip(self):
        if self.facing_forward:
            self.move_left()
        else:
            self.move_right()

    def check_collisions(self, level, rocky):
        self.check_in_bounds(level)
        self.check_rocky_collision(rocky)
        self.check_fireball_collisions(rocky)

    def check_fireball_collisions(self, rocky):
        for fire in rocky.fireballs:
            if (self.x <= fire.x <= self.get_bound_x() or self.x <= fire.get_bound_x() <= self.get_bound_x()) and \
                    (self.y <= fire.y <= self.get_bound_y() or self.y <= fire.get_bound_y() <= self.get_bound_y()):
                self.kill()
                fire.kill()
                rocky.get_points_bonus(self)

    def check_rocky_collision(self, rocky):
        return

    def check_in_bounds(self, level):
        squares = level.updated_squares()
        max_height = 100000000
        for square in squares:
            top_right_corner = [square[0] + square[2], square[1]]
            bottom_left_corner = [square[0], square[1] + square[3]]

            if bottom_left_corner[0] < self.x < top_right_corner[0]:
                if not bottom_left_corner[0] < self.get_bound_x() < top_right_corner[0]:
                    if self.get_bound_y() > top_right_corner[1]:
                        self.bumping_left = True
                        self.x = top_right_corner[0]
                        self.flip()
                    else:
                        self.bumping_left = False
            else:
                if bottom_left_corner[0] < self.get_bound_x() < top_right_corner[0]:
                    if self.get_bound_y() > top_right_corner[1]:
                        self.bumping_right = True
                        self.x = bottom_left_corner[0] - (self.get_bound_x() - self.x) + 1
                        self.flip()
                    else:
                        self.bumping_right = False

            if bottom_left_corner[0] < self.x < top_right_corner[0] \
                    or bottom_left_corner[0] <= self.get_bound_x() <= top_right_corner[0]:
                if top_right_corner[1] < max_height:
                    max_height = top_right_corner[1]

        self.on_the_floor = max_height <= self.get_bound_y()
        self.floor_level = max_height
        if self.get_bound_y() >= self.window_height:
            self.kill()
        # Fix floor collisions
        if self.on_the_floor and self.speed_y > 0:
            self.speed_y = 0
            self.y = self.floor_level - (self.get_bound_y() - self.get_y())

    def move_by(self, dx):
        self.x += dx

    def fix_position(self, level):
        if self.x < level.x:
            self.kill()
        if self.get_bound_x() > level.x + level.width:
            self.kill()

    def update(self, level):
        if self.x <= self.window_width:
            self.x += self.speed_x
        self.y += self.speed_y
        if not self.on_the_floor:
            self.speed_y += self.acceleration
        self.fix_position(level)
        if Character.current_time_millis() - self.last_change >= self.walk_time:
            self.change_sprite()

    def restart(self):
        self.x = self.pos_ini[0]
        self.y = self.pos_ini[1]
        self.speed_x = self.speed
        self.alive = True

    def change_sprite(self):
        self.last_change = Character.current_time_millis()
        self.current_sprite = 1 - self.current_sprite
        if self.facing_forward:
            self.sprite = self.front_sprites[self.current_sprite]
        else:
            self.sprite = self.back_sprites[self.current_sprite]

    def draw(self, bg):
        bg.blit(self.sprite, (int(self.x), int(self.y)))