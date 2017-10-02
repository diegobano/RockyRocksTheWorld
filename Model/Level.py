#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random

import pygame as pyg
from LevelBlock import LevelBlock

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"


class Level:
    def __init__(self, initial_x, initial_y, w_width, w_height, square_width, square_height, level_length, flag):
        self.sprite = None
        self.window_width = w_width
        self.window_height = w_height
        self.x = initial_x
        self.y = self.window_height - initial_y
        self.width = level_length * square_width
        self.height = square_height * 3
        self.level_length = level_length
        self.squares = []
        self.square_width = square_width
        self.square_height = square_height
        self.flag = flag
        self.flag_x = self.width - self.square_width / 2 - self.flag.get_size()[0] / 2
        self.flag_y = self.window_height - self.flag.get_size()[1]
        self.level_creators = [self.create_easy_level, self.create_medium_level, self.create_hard_level]

        # Level sprites
        # Low level floor
        self.low_level = pyg.image.load(os.path.join("Resources/Landscapes/low_level.png"))
        self.low_level = pyg.transform.scale(self.low_level, (self.square_width, self.square_height))
        self.low_level.convert()
        # Middle level floor
        self.mid_level = pyg.image.load(os.path.join("Resources/Landscapes/mid_level.png"))
        self.mid_level = pyg.transform.scale(self.mid_level, (self.square_width, self.square_height * 2))
        self.mid_level.convert()
        # High level floor
        self.high_level = pyg.image.load(os.path.join("Resources/Landscapes/high_level.png"))
        self.high_level = pyg.transform.scale(self.high_level, (self.square_width, self.square_height * 3))
        self.high_level.convert()

        self.background = pyg.image.load(os.path.join("Resources/Landscapes/background2.png"))
        self.background = pyg.transform.scale(self.background, (self.window_width, self.window_height))
        self.background.convert()

    def updated_squares(self):
        updated_corners = []
        for square in self.squares:
            updated_corners.append([square.get_x(), square.get_y(), square.get_width(),
                                    square.get_height()])
        return updated_corners

    def create_random_level(self, difficulty):
        self.restart_level()
        self.squares = []
        self.level_creators[difficulty]()

    def create_easy_level(self):
        previous = 1
        previous_x = self.x - self.square_width
        for i in range(self.level_length):
            previous_x += self.square_width
            sig = random.randint(1, 2)
            if previous == 1:
                if sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                else:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
            elif previous == 2:
                if sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                else:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
            if i == self.level_length - 1:
                self.flag_y = self.squares[i].get_y() - self.flag.get_size()[1]

    def create_medium_level(self):
        previous = 0
        previous_x = self.x - self.square_width
        for i in range(self.level_length):
            previous_x += self.square_width
            if previous == 0:
                self.squares.append(self.new_low_square(previous_x))
                previous = 1
            elif previous == 1:
                sig = random.randint(1, 2)
                if sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                else:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
            elif previous == 2:
                sig = random.randint(1, 3)
                if sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                elif sig == 2:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
                else:
                    self.squares.append(self.new_high_square(previous_x))
                    previous = 3
            else:
                sig = random.randint(1, 3)
                if sig == 1:
                    if i == self.level_length - 1 or i < 7:
                        self.squares.append(self.new_low_square(previous_x))
                        previous = 1
                    else:
                        self.squares.append(self.new_empty_square(previous_x))
                        previous = 0
                elif sig == 2:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
                else:
                    self.squares.append(self.new_high_square(previous_x))
                    previous = 3
            if i == self.level_length - 1:
                self.flag_y = self.squares[i].get_y() - self.flag.get_size()[1]

    def create_hard_level(self):
        previous = 0
        previous_x = self.x - self.square_width
        for i in range(self.level_length):
            previous_x += self.square_width
            if previous == 0:
                self.squares.append(self.new_low_square(previous_x))
                previous = 1
            elif previous == 1:
                sig = random.randint(0, 2)
                if sig == 0:
                    if i == self.level_length - 1 or i < 7:
                        self.squares.append(self.new_low_square(previous_x))
                        previous = 1
                    else:
                        self.squares.append(self.new_empty_square(previous_x))
                        previous = 0
                elif sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                else:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
            elif previous == 2:
                sig = random.randint(0, 3)
                if sig == 0:
                    if i == self.level_length - 1 or i < 7:
                        self.squares.append(self.new_low_square(previous_x))
                        previous = 1
                    else:
                        self.squares.append(self.new_empty_square(previous_x))
                        previous = 0
                elif sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                elif sig == 2:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
                else:
                    self.squares.append(self.new_high_square(previous_x))
                    previous = 3
            else:
                sig = random.randint(0, 3)
                if sig == 0:
                    if i == self.level_length - 1 or i < 7:
                        self.squares.append(self.new_low_square(previous_x))
                        previous = 1
                    else:
                        self.squares.append(self.new_empty_square(previous_x))
                        previous = 0
                elif sig == 1:
                    self.squares.append(self.new_low_square(previous_x))
                    previous = 1
                elif sig == 2:
                    self.squares.append(self.new_mid_square(previous_x))
                    previous = 2
                else:
                    self.squares.append(self.new_high_square(previous_x))
                    previous = 3
            if i == self.level_length - 1:
                self.flag_y = self.squares[i].get_y() - self.flag.get_size()[1]

    def new_empty_square(self, x):
        return LevelBlock(x, self.window_height, self.square_width, 0, self.low_level)

    def new_low_square(self, x):
        return LevelBlock(x, self.window_height - self.square_height, self.square_width, self.square_height,
                          self.low_level)

    def new_mid_square(self, x):
        return LevelBlock(x, self.window_height - 2 * self.square_height, self.square_width, self.square_height * 2,
                          self.mid_level)

    def new_high_square(self, x):
        return LevelBlock(x, self.window_height - 3 * self.square_height, self.square_width, self.square_height * 3,
                          self.high_level)

    def restart_level(self):
        for square in self.squares:
            square.x -= self.x
        self.flag_x -= self.x
        self.x = 0

    def get_flag_bound_x(self):
        return self.flag_x + self.flag.get_size()[0]

    def get_flag_bound_y(self):
        return self.flag_y + self.flag.get_size()[0]

    def move_level(self, speed, enemies):
        self.x += speed
        for square in self.squares:
            square.move(speed)
        for enemy in enemies:
            enemy.move_by(speed)
        self.flag_x += speed

    def draw(self, bg):
        bg.blit(self.background, (0, 0))
        bg.blit(self.flag, (int(self.flag_x), int(self.flag_y)))
        for square in self.squares:
            square.draw(bg)














