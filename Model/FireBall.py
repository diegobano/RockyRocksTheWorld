from Character import Character

import os
import pygame as pyg


class FireBall:
    def __init__(self, initial_x, initial_y, rocky):
        self.rocky = rocky
        self.x = initial_x
        self.y = initial_y
        self.alive = True
        self.current_sprite = 0
        self.last_change = 0
        self.change_rate = 300

        self.fire_sprite_front1 = pyg.image.load(os.path.join("Resources/Attack/fire.png"))
        self.fire_sprite_front1 = pyg.transform.scale(self.fire_sprite_front1, (self.rocky.size / 2, self.rocky.size / 2))
        self.fire_sprite_front1.convert()
        self.fire_sprite_front2 = pyg.image.load(os.path.join("Resources/Attack/fire2.png"))
        self.fire_sprite_front2 = pyg.transform.scale(self.fire_sprite_front2, (self.rocky.size / 2, self.rocky.size / 2))
        self.fire_sprite_front2.convert()

        self.fire_sprite_back1 = pyg.image.load(os.path.join("Resources/Attack/fire-back.png"))
        self.fire_sprite_back1 = pyg.transform.scale(self.fire_sprite_back1, (self.rocky.size / 2, self.rocky.size / 2))
        self.fire_sprite_back1.convert()
        self.fire_sprite_back2 = pyg.image.load(os.path.join("Resources/Attack/fire2-back.png"))
        self.fire_sprite_back2 = pyg.transform.scale(self.fire_sprite_back2, (self.rocky.size / 2, self.rocky.size / 2))
        self.fire_sprite_back2.convert()
        if self.rocky.facing_forward:
            self.sprites = [self.fire_sprite_front1, self.fire_sprite_front2]
            self.speed = self.rocky.speed * 2
        else:
            self.sprites = [self.fire_sprite_back1, self.fire_sprite_back2]
            self.speed = - self.rocky.speed * 2
        self.sprite = self.sprites[0]

    def check_in_bounds(self, level):
        squares = level.updated_squares()
        for square in squares:
            top_right_corner = [square[0] + square[2], square[1]]
            bottom_left_corner = [square[0], square[1] + square[3]]

            if top_right_corner[0] - 10 < self.x < top_right_corner[0]:
                if not bottom_left_corner[0] < self.get_bound_x() < bottom_left_corner[0] + 10:
                    if self.get_bound_y() > top_right_corner[1]:
                        self.x = top_right_corner[0] + 1
                        self.kill()
            else:
                if bottom_left_corner[0] < self.get_bound_x() < bottom_left_corner[0] + 10:
                    if self.get_bound_y() > top_right_corner[1]:
                        self.x = bottom_left_corner[0] - (self.get_bound_x() - self.x) - 1
                        self.kill()

    def kill(self):
        self.alive = False

    def get_bound_x(self):
        return self.x + self.sprite.get_size()[0]

    def get_bound_y(self):
        return self.y + self.sprite.get_size()[1]

    def is_alive(self):
        return self.alive

    def move(self, speed):
        self.x += speed

    def update(self, level):
        if Character.current_time_millis() - self.last_change >= self.change_rate:
            self.last_change = Character.current_time_millis()
            self.current_sprite = 1 - self.current_sprite
            self.sprite = self.sprites[self.current_sprite]
        self.x += self.speed
        self.check_in_bounds(level)

    def draw(self, bg):
        bg.blit(self.sprite, (self.x, self.y))