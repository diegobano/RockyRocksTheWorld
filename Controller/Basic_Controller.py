#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from Model.GameOverScreen import GameOverScreen
from Model.HomeScreen import HomeScreen
from Model.Level import Level
from Model.Potato import Potato
from Model.Rocky import Rocky
from Model.Spike import Spike

import pygame as pyg
import random
import sys
import time

from View.Window import Window

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"


class Controller:
    def __init__(self):
        # Level and window variables
        self.height = 500
        self.width = 600
        self.lives = 3
        self.level_size = 50
        self.easy_enemies = 20
        self.medium_enemies = 30
        self.medium_p = 0.7
        self.hard_enemies = 30
        self.hard_p = 0.3
        self.acceleration = 1
        self.total_time = 200
        self.game_song = "Resources/Music/game-song2.mp3"
        self.just_game_over = True
        self.game_mode = 0
        self.current_level = 0
        self.last_level_score = 0

        pyg.init()
        self.win = pyg.display.set_mode([self.width, self.height])
        pyg.display.set_caption('Rocky rocks the world!')

        # Rocky sprites
        self.rocky_size = 40
        # Front sprite
        self.rocky_front_image = pyg.image.load(os.path.join("Resources/Character/front.png"))
        self.rocky_front_image = pyg.transform.scale(self.rocky_front_image, (self.rocky_size, self.rocky_size))
        self.rocky_front_image.convert()
        # Back sprite
        self.rocky_back_image = pyg.image.load(os.path.join("Resources/Character/back.png"))
        self.rocky_back_image = pyg.transform.scale(self.rocky_back_image, (self.rocky_size, self.rocky_size))
        self.rocky_back_image.convert()
        # Blink sprite
        self.rocky_blink_image = pyg.image.load(os.path.join("Resources/Character/blink.png"))
        self.rocky_blink_image = pyg.transform.scale(self.rocky_blink_image, (self.rocky_size, self.rocky_size))
        self.rocky_blink_image.convert()
        # Damage sprites
        self.rocky_dmg_image1 = pyg.image.load(os.path.join("Resources/Character/dmg.png"))
        self.rocky_dmg_image1 = pyg.transform.scale(self.rocky_dmg_image1, (self.rocky_size, self.rocky_size))
        self.rocky_dmg_image1.convert()
        self.rocky_dmg_image2 = pyg.image.load(os.path.join("Resources/Character/dmg2.png"))
        self.rocky_dmg_image2 = pyg.transform.scale(self.rocky_dmg_image2, (self.rocky_size, self.rocky_size))
        self.rocky_dmg_image2.convert()
        # Ball power sprites
        self.rocky_ball_image1 = pyg.image.load(os.path.join("Resources/Character/ball.png"))
        self.rocky_ball_image1 = pyg.transform.scale(self.rocky_ball_image1, (self.rocky_size, self.rocky_size))
        self.rocky_ball_image1.convert()
        self.rocky_ball_image2 = pyg.image.load(os.path.join("Resources/Character/ball-back.png"))
        self.rocky_ball_image2 = pyg.transform.scale(self.rocky_ball_image2, (self.rocky_size, self.rocky_size))
        self.rocky_ball_image2.convert()
        # Fire power sprites
        self.rocky_fire_image1 = pyg.image.load(os.path.join("Resources/Character/fire.png"))
        self.rocky_fire_image1 = pyg.transform.scale(self.rocky_fire_image1, (self.rocky_size, self.rocky_size))
        self.rocky_fire_image1.convert()
        self.rocky_fire_image2 = pyg.image.load(os.path.join("Resources/Character/fire2.png"))
        self.rocky_fire_image2 = pyg.transform.scale(self.rocky_fire_image2, (self.rocky_size, self.rocky_size))
        self.rocky_fire_image2.convert()

        self.rocky_wink = pyg.image.load(os.path.join("Resources/Character/wink.png"))
        self.rocky_wink = pyg.transform.scale(self.rocky_wink, (self.rocky_size, self.rocky_size))
        self.rocky_wink.convert()

        # Potato sprites
        # Front sprites
        self.potato_front_image1 = pyg.image.load(os.path.join("Resources/Enemies/potato1.png"))
        self.potato_front_image1 = pyg.transform.scale(self.potato_front_image1, (self.rocky_size, self.rocky_size))
        self.potato_front_image1.convert()
        self.potato_front_image2 = pyg.image.load(os.path.join("Resources/Enemies/potato2.png"))
        self.potato_front_image2 = pyg.transform.scale(self.potato_front_image2, (self.rocky_size, self.rocky_size))
        self.potato_front_image2.convert()
        # Back sprites
        self.potato_back_image1 = pyg.image.load(os.path.join("Resources/Enemies/potato1-front.png"))
        self.potato_back_image1 = pyg.transform.scale(self.potato_back_image1, (self.rocky_size, self.rocky_size))
        self.potato_back_image1.convert()
        self.potato_back_image2 = pyg.image.load(os.path.join("Resources/Enemies/potato2-front.png"))
        self.potato_back_image2 = pyg.transform.scale(self.potato_back_image2, (self.rocky_size, self.rocky_size))
        self.potato_back_image2.convert()

        # Blob-spike sprites
        # Front sprites
        self.blob_front_image1 = pyg.image.load(os.path.join("Resources/Enemies/blob1.png"))
        self.blob_front_image1 = pyg.transform.scale(self.blob_front_image1, (self.rocky_size, self.rocky_size))
        self.blob_front_image1.convert()
        self.blob_front_image2 = pyg.image.load(os.path.join("Resources/Enemies/blob2.png"))
        self.blob_front_image2 = pyg.transform.scale(self.blob_front_image2, (self.rocky_size, self.rocky_size))
        self.blob_front_image2.convert()
        # Back sprites
        self.blob_back_image1 = pyg.image.load(os.path.join("Resources/Enemies/blob1-back.png"))
        self.blob_back_image1 = pyg.transform.scale(self.blob_back_image1, (self.rocky_size, self.rocky_size))
        self.blob_back_image1.convert()
        self.blob_back_image2 = pyg.image.load(os.path.join("Resources/Enemies/blob2-back.png"))
        self.blob_back_image2 = pyg.transform.scale(self.blob_back_image2, (self.rocky_size, self.rocky_size))
        self.blob_back_image2.convert()
        # Spike sprites
        self.spike_image1 = pyg.image.load(os.path.join("Resources/Enemies/midspiky.png"))
        self.spike_image1 = pyg.transform.scale(self.spike_image1, (self.rocky_size, self.rocky_size))
        self.spike_image1.convert()
        self.spike_image2 = pyg.image.load(os.path.join("Resources/Enemies/spiky.png"))
        self.spike_image2 = pyg.transform.scale(self.spike_image2, (self.rocky_size, self.rocky_size))
        self.spike_image2.convert()

        # Final flag
        self.flag = pyg.image.load(os.path.join("Resources/Misc/flag.png"))
        self.flag = pyg.transform.scale(self.flag, (self.rocky_size, self.rocky_size))
        self.flag.convert()

        # Sounds
        self.jump_sound = pyg.mixer.Sound("Resources/Music/jump.wav")
        # self.jump_sound.set_volume(0.2)

        self.bump_sound = pyg.mixer.Sound("Resources/Music/bump.wav")
        # self.bump_sound.set_volume(0.2)

        self.hit_sound = pyg.mixer.Sound("Resources/Music/hit.wav")
        # self.hit_sound.set_volume(0.2)

        self.squash_sound = pyg.mixer.Sound("Resources/Music/squash.wav")
        # self.squash_sound.set_volume(0.2)

        self.win_sound = pyg.mixer.Sound("Resources/Music/win.wav")
        # self.win_sound.set_volume(0.2)

        self.landing_sound = pyg.mixer.Sound("Resources/Music/floor-bump.wav")
        # self.landing_sound.set_volume(0.2)

        self.fire_sound = pyg.mixer.Sound("Resources/Music/shoot.wav")
        # self.fire_sound.set_volume(0.5)

        self.button_change = pyg.mixer.Sound("Resources/Music/button-change.wav")
        self.button_change.set_volume(0.5)

        self.button_press = pyg.mixer.Sound("Resources/Music/button-press.wav")
        self.button_change.set_volume(0.5)

        self.death_sound = "Resources/Music/death.mp3"

        # Objects for the controller
        # Numbers for counter and points
        self.numbers = []
        for i in range(10):
            number = pyg.image.load(os.path.join("Resources/Numbers/" + str(i) + ".png"))
            number = pyg.transform.scale(number, (10, 20))
            number.convert()
            self.numbers.append(number)

        # Level object
        self.level = Level(-3, self.height - 3 * self.rocky_size, self.width, self.height, self.rocky_size * 4,
                           3 * self.rocky_size / 4, self.level_size, self.flag)
        self.levels = []

        # Main character
        self.rocky_main = Rocky(self.lives, 20, self.height - 140, self.width, self.height, 3, self.acceleration,
                                self.rocky_front_image, self.rocky_back_image, self.rocky_blink_image,
                                self.rocky_dmg_image1, self.rocky_dmg_image2, self.rocky_ball_image1,
                                self.rocky_ball_image2, self.rocky_fire_image1, self.rocky_fire_image2, self.numbers,
                                self.total_time, self.jump_sound, self.landing_sound, self.bump_sound, self.win_sound,
                                self.hit_sound, self.fire_sound)

        self.rocky = self.rocky_main

        # Enemies
        self.enemies = []
        self.backup_enemies = []

        self.home_screen = HomeScreen(self.width, self.height)
        self.game_over_screen = GameOverScreen(self.width, self.height, self.rocky.points)

        # View controller
        self.window = Window(self.win, self.rocky, self.level, self.enemies, self.home_screen, self.game_over_screen)

        # Game states
        self.game_over = False
        self.home = True

    def new_easy_level(self):
        pyg.mixer.music.load(self.game_song)
        pyg.mixer.music.play(-1, 0.0)
        self.home = False
        # Main character
        self.rocky = Rocky(self.lives, 20, self.height - 140, self.width, self.height, 3, self.acceleration,
                           self.rocky_front_image, self.rocky_back_image, self.rocky_blink_image,
                           self.rocky_dmg_image1, self.rocky_dmg_image2, self.rocky_ball_image1,
                           self.rocky_ball_image2, self.rocky_fire_image1, self.rocky_fire_image2, self.numbers,
                           self.total_time, self.jump_sound, self.landing_sound, self.bump_sound, self.win_sound,
                           self.hit_sound, self.fire_sound)

        # Level object
        self.level.create_random_level(0)

        # Enemies
        self.enemies = []
        h = (self.level.width - self.rocky_size * 12 + 1 - 40) / self.easy_enemies
        for i in range(self.easy_enemies):
            self.enemies.append(Potato(self.rocky_size * 3 * 4 + h * i,
                                       self.height - self.level.height - self.rocky_size, self.width, self.height,
                                       -1, 1, self.potato_front_image1, self.potato_front_image2,
                                       self.potato_back_image1,
                                       self.potato_back_image2, self.squash_sound))
        self.backup_enemies = []
        self.backup_enemies.extend(self.enemies)

        # View controller
        self.window = Window(self.win, self.rocky, self.level, self.enemies, self.home_screen, self.game_over_screen)
        self.just_game_over = True

    def new_medium_level(self):
        pyg.mixer.music.load(self.game_song)
        pyg.mixer.music.play(-1, 0.0)
        self.home = False
        # Main character
        self.rocky = Rocky(self.lives, 20, self.height - 140, self.width, self.height, 3, self.acceleration,
                           self.rocky_front_image, self.rocky_back_image, self.rocky_blink_image,
                           self.rocky_dmg_image1, self.rocky_dmg_image2, self.rocky_ball_image1,
                           self.rocky_ball_image2, self.rocky_fire_image1, self.rocky_fire_image2, self.numbers,
                           self.total_time, self.jump_sound, self.landing_sound, self.bump_sound, self.win_sound,
                           self.hit_sound, self.fire_sound)

        # Level object
        self.level.create_random_level(1)

        # Enemies
        self.enemies = []
        h = (self.level.width - self.rocky_size * 12 + 1 - 40) / self.medium_enemies
        for i in range(self.medium_enemies):
            if random.random() < self.medium_p:
                self.enemies.append(Potato(self.rocky_size * 3 * 4 + h * i,
                                           self.height - self.level.height - self.rocky_size, self.width, self.height,
                                           -1, 1, self.potato_front_image1, self.potato_front_image2,
                                           self.potato_back_image1, self.potato_back_image2, self.squash_sound))
            else:
                self.enemies.append(Spike(self.rocky_size * 3 * 4 + h * i,
                                          self.height - self.level.height - self.rocky_size, self.width, self.height,
                                          -1, 1, self.blob_front_image1, self.blob_front_image2, self.blob_back_image1,
                                          self.blob_back_image2, self.spike_image1, self.spike_image2,
                                          self.squash_sound))

        self.backup_enemies = []
        self.backup_enemies.extend(self.enemies)
        # View controller
        self.window = Window(self.win, self.rocky, self.level, self.enemies, self.home_screen, self.game_over_screen)
        self.just_game_over = True

    def new_hard_level(self):
        pyg.mixer.music.load(self.game_song)
        pyg.mixer.music.play(-1, 0.0)
        self.home = False
        # Main character
        self.rocky = Rocky(self.lives, 20, self.height - 140, self.width, self.height, 3, self.acceleration,
                           self.rocky_front_image, self.rocky_back_image, self.rocky_blink_image,
                           self.rocky_dmg_image1, self.rocky_dmg_image2, self.rocky_ball_image1,
                           self.rocky_ball_image2, self.rocky_fire_image1, self.rocky_fire_image2, self.numbers,
                           self.total_time, self.jump_sound, self.landing_sound, self.bump_sound, self.win_sound,
                           self.hit_sound, self.fire_sound)

        # Level object
        self.level.create_random_level(2)

        # Enemies
        self.enemies = []
        h = (self.level.width - self.rocky_size * 12 + 1 - 40) / self.medium_enemies
        for i in range(self.hard_enemies):
            if random.random() < self.hard_p:
                self.enemies.append(Potato(self.rocky_size * 3 * 4 + h * i,
                                           self.height - self.level.height - self.rocky_size, self.width, self.height,
                                           -1, 1, self.potato_front_image1, self.potato_front_image2,
                                           self.potato_back_image1, self.potato_back_image2, self.squash_sound))
            else:
                self.enemies.append(Spike(self.rocky_size * 3 * 4 + h * i,
                                          self.height - self.level.height - self.rocky_size, self.width, self.height,
                                          -1, 1, self.blob_front_image1, self.blob_front_image2, self.blob_back_image1,
                                          self.blob_back_image2, self.spike_image1, self.spike_image2,
                                          self.squash_sound))

        self.backup_enemies = []
        self.backup_enemies.extend(self.enemies)

        # View controller
        self.window = Window(self.win, self.rocky, self.level, self.enemies, self.home_screen, self.game_over_screen)
        self.just_game_over = True

    def new_game(self):
        self.levels = [self.new_easy_level, self.new_medium_level, self.new_hard_level]
        self.current_level = -1
        self.next_level()

    def next_level(self):
        self.current_level += 1
        self.last_level_score = self.rocky.points.points
        if self.current_level < 3:
            self.levels[self.current_level]()
            self.rocky.points.add_points(self.last_level_score)
        else:
            self.game_mode = 0

    def restart_level(self):
        # Main character
        if self.game_mode == 0:
            self.rocky.restart()
        else:
            self.rocky.restart()
            self.rocky.points.add_points(self.last_level_score)

        # Level object
        self.level.restart_level()

        # Enemies
        self.enemies = []
        self.enemies.extend(self.backup_enemies)
        for enemy in self.enemies:
            enemy.restart()

        # View controller
        self.window = Window(self.win, self.rocky, self.level, self.enemies, self.home_screen, self.game_over_screen)

        # Game states
        self.game_over = False

    def restart_all(self):
        self.home_screen = HomeScreen(self.width, self.height)
        self.window.set_home(self.home_screen)
        self.home = True
        self.game_over = False
        self.lives = 3

    def home_update(self):
        self.window.clean()
        self.window.draw_home_screen()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.quit_game()

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    self.quit_game()

                if event.key == pyg.K_LEFT:
                    self.button_change.play()
                    self.home_screen.move_left()

                if event.key == pyg.K_RIGHT:
                    self.button_change.play()
                    self.home_screen.move_right()

                if event.key == pyg.K_SPACE:
                    self.button_press.play()
                    self.home_screen.select_button(self)

                if event.key == pyg.K_BACKSPACE:
                    self.home_screen.go_back()
        if self.home_screen.leave_home:
            self.home = False

    def winner_update(self):
        self.rocky.sprite = self.rocky_wink
        self.win_sound.play()
        self.window.clean()
        self.window.draw()
        time.sleep(1)
        if self.game_mode == 0:
            print "You won!"
            print "Your score was:", self.rocky.points.points
            self.quit_game()
        else:
            self.next_level()

    def game_update(self):
        self.window.clean()
        self.window.draw()

        if self.rocky.getting_damage:
            if Rocky.current_time_millis() - self.rocky.dmg_moment > self.rocky.dmg_time:
                self.rocky.stop_getting_damage()

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.quit_game()

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.quit_game()

            self.rocky.check_collisions(self.level)
            self.rocky.update(self.level, self.enemies)
            for enemy in self.enemies:
                enemy.check_collisions(self.level, self.rocky)
                enemy.update(self.level)

            for enemy in self.enemies:
                if not enemy.is_alive():
                    self.enemies.remove(enemy)

            if not self.rocky.is_alive():
                self.game_over = True
        elif self.rocky.transforming:
            if Rocky.current_time_millis() - self.rocky.current_power.transformation_start >= \
                    self.rocky.current_power.transformation_time:
                self.rocky.current_power.stop_transforming()

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.quit_game()

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.quit_game()

                    if event.key == pyg.K_SPACE:
                        self.rocky.current_power.stop_transforming()
                        self.rocky.to_last_power()

            self.rocky.update(self.level, self.enemies)
        else:
            for event in pyg.event.get():

                if event.type == pyg.QUIT:
                    self.quit_game()

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.quit_game()

                    pressed = pyg.key.get_pressed()

                    if pressed[pyg.K_LEFT]:
                        self.rocky.move_left()

                    if pressed[pyg.K_RIGHT]:
                        self.rocky.move_right()

                    if pressed[pyg.K_UP] and self.rocky.on_the_floor:
                        self.rocky.jump()

                    if pressed[pyg.K_SPACE]:
                        self.rocky.throw_fireball()

                if event.type == pyg.KEYUP:
                    if event.key == pyg.K_LEFT:
                        self.rocky.stop_moving_x()
                    if event.key == pyg.K_RIGHT:
                        self.rocky.stop_moving_x()

            self.rocky.check_collisions(self.level)
            self.rocky.update(self.level, self.enemies)
            for enemy in self.enemies:
                enemy.check_collisions(self.level, self.rocky)
                enemy.update(self.level)

            for enemy in self.enemies:
                if not enemy.is_alive():
                    self.enemies.remove(enemy)

            if not self.rocky.is_alive():
                self.game_over = True

    def game_over_update(self):
        if self.just_game_over:
            self.rocky.sprite = self.rocky_dmg_image1
            self.window.clean()
            self.window.draw()
            pyg.mixer.music.load(self.death_sound)
            pyg.mixer.music.play()
            time.sleep(4)
            self.just_game_over = False
            self.game_over_screen.set_points(self.rocky.points)
            pyg.mixer.music.load(self.game_over_screen.music)
            pyg.mixer.music.play(-1)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.quit_game()

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    self.quit_game()

                if event.key == pyg.K_LEFT:
                    self.button_change.play()
                    self.game_over_screen.move_left()

                if event.key == pyg.K_RIGHT:
                    self.button_change.play()
                    self.game_over_screen.move_right()

                if event.key == pyg.K_SPACE:
                    self.button_press.play()
                    self.game_over_screen.select_button(self)

        self.window.clean()
        self.window.draw_game_over_screen()

    def quit_game(self):
        pyg.quit()
        sys.exit()

    def update(self):
        if self.home:
            self.home_update()
        else:
            if not self.game_over:
                self.game_update()
                if self.rocky.end_of_the_level:
                    self.winner_update()
                if self.rocky.restart_level:
                    self.restart_level()
            else:
                self.game_over_update()
