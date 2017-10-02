#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Enemy import Enemy
from Character import Character

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"


class Spike(Enemy):
    def __init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration, front_image1, front_image2,
                 back_image1, back_image2, spike_image1, spike_image2, squash_sound):
        Enemy.__init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration, front_image1, front_image2,
                       back_image1, back_image2, squash_sound)
        self.is_spike = False
        self.spike_sprites = [spike_image1, spike_image2]
        self.last_spike = 0
        self.spike_duration = 1500
        self.spike_rest = 2000
        self.spike_distance = 80
        self.transforming = False
        self.transforming_time = 200
        self.transformation_start = 0
        self.last_transformation = 0
        self.current_state = 0
        self.previous_sprite = self.sprite

    def check_rocky_collision(self, rocky):
        if (self.x < rocky.get_bound_x() < self.get_bound_x() or self.x < rocky.x < self.get_bound_x()) \
                and not rocky.getting_damage:
            if (self.get_bound_y() >= rocky.get_bound_y() >= self.y or self.get_bound_y() >= rocky.y >= self.y) \
                    and rocky.speed_y <= 0:
                rocky.get_hit()
            elif (self.get_bound_y() >= rocky.get_bound_y() >= self.y or self.get_bound_y() >= rocky.y >= self.y) \
                    and rocky.speed_y > 0 and not self.is_spike:
                self.squash_sound.play()
                self.kill()
                rocky.get_spike_bonus()
            elif (self.get_bound_y() >= rocky.get_bound_y() >= self.y or self.get_bound_y() >= rocky.y >= self.y) \
                    and rocky.speed_y > 0 and self.is_spike:
                rocky.get_hit()

    def check_rocky_approach(self, rocky):
        if abs(rocky.get_center_x() - self.get_center_x()) < self.spike_distance \
                and Character.current_time_millis() - self.last_spike >= self.spike_rest and not self.is_spike:
            self.turn_into_spike()

    def turn_into_spike(self):
        self.transforming = True
        self.transformation_start = Character.current_time_millis()
        self.is_spike = True
        self.previous_sprite = self.sprite

    def back_to_normal(self):
        self.transforming = False
        self.is_spike = False
        self.current_state = 0
        self.last_spike = Character.current_time_millis()

    def update(self, level):
        if not self.is_spike:
            if self.x <= self.window_width:
                self.x += self.speed_x
            self.y += self.speed_y
            if not self.on_the_floor:
                self.speed_y += self.acceleration
            self.fix_position(level)
            if Character.current_time_millis() - self.last_change >= self.walk_time:
                self.change_sprite()
        else:
            self.y += self.speed_y
            if not self.on_the_floor:
                self.speed_y += self.acceleration
            self.fix_position(level)
            if Character.current_time_millis() - self.transformation_start <= self.spike_duration:
                if Character.current_time_millis() - self.last_transformation >= self.transforming_time \
                        and self.current_state < 2:
                    self.last_transformation = Character.current_time_millis()
                    self.change_into_spike(self.current_state + 1)
            else:
                if Character.current_time_millis() - self.last_transformation >= self.transforming_time:
                    self.last_transformation = Character.current_time_millis()
                    self.change_back_to_blob(self.current_state - 1)

    def change_into_spike(self, new_state):
        self.current_state = new_state
        self.sprite = self.spike_sprites[self.current_state - 1]

    def change_back_to_blob(self, new_state):
        self.current_state = new_state
        if self.current_state == 0:
            self.back_to_normal()
            self.is_spike = False
            self.sprite = self.previous_sprite
        else:
            self.sprite = self.spike_sprites[self.current_state]

    def check_collisions(self, level, rocky):
        self.check_in_bounds(level)
        self.check_rocky_collision(rocky)
        self.check_fireball_collisions(rocky)
        self.check_rocky_approach(rocky)

    def get_points(self):
        return 10