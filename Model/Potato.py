#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Enemy import Enemy

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"


class Potato(Enemy):
    def __init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration, front_image1, front_image2,
                 back_image1, back_image2, squash_sound):
        Enemy.__init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration, front_image1, front_image2,
                       back_image1, back_image2, squash_sound)

    def check_rocky_collision(self, rocky):
        if (self.x < rocky.get_bound_x() < self.get_bound_x() or self.x < rocky.x < self.get_bound_x()) \
                and not rocky.getting_damage:
            if (self.get_bound_y() >= rocky.get_bound_y() >= self.y or self.get_bound_y() >= rocky.y >= self.y) \
                    and rocky.speed_y <= 0:
                rocky.get_hit()
            elif (self.get_bound_y() >= rocky.get_bound_y() >= self.y or self.get_bound_y() >= rocky.y >= self.y) \
                    and rocky.speed_y > 0:
                self.squash_sound.play()
                self.kill()
                rocky.get_potato_bonus()

    def get_points(self):
        return 5
