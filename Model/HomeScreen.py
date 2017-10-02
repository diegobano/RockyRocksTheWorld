import os
import pygame as pyg


class HomeScreen:
    def __init__(self, w_width, w_height):
        # Parameters
        self.window_width = w_width
        self.window_height = w_height
        self.current_button = 0
        self.current_stage = 0
        self.leave_home = False
        
        # Background image
        self.background = pyg.image.load(os.path.join("Resources/Misc/title-screen.jpg"))
        self.background = pyg.transform.scale(self.background, (self.window_width, self.window_height))
        self.background.convert()
        
        # First screen
        # New game box
        self.new_game = pyg.image.load(os.path.join("Resources/Misc/new-game.png"))
        self.new_game = pyg.transform.scale(self.new_game, (self.window_width / 4, self.window_height / 10))
        self.new_game.convert()
        # New game square
        self.new_game_square = pyg.image.load(os.path.join("Resources/Misc/new-game-square.png"))
        self.new_game_square = pyg.transform.scale(self.new_game_square, (self.window_width / 4 + 20, self.window_height / 10 + 20))
        self.new_game_square.convert()
        
        # Story mode box
        self.story_mode = pyg.image.load(os.path.join("Resources/Misc/story-mode.png"))
        self.story_mode = pyg.transform.scale(self.story_mode, (self.window_width / 4, self.window_height / 10))
        self.story_mode.convert()
        
        # Story mode square
        self.story_mode_square = pyg.image.load(os.path.join("Resources/Misc/story-mode-square.png"))
        self.story_mode_square = pyg.transform.scale(self.story_mode_square, (self.window_width / 4 + 20, self.window_height / 10 + 20))
        self.story_mode_square.convert()

        # Second screen
        # Easy box
        self.easy = pyg.image.load(os.path.join("Resources/Misc/easy.png"))
        self.easy = pyg.transform.scale(self.easy, (self.window_width / 5, self.window_height / 10))
        self.easy.convert()
        # Easy square
        self.easy_square = pyg.image.load(os.path.join("Resources/Misc/easy-square.png"))
        self.easy_square = pyg.transform.scale(self.easy_square, (self.window_width / 5 + 20, self.window_height / 10 + 20))
        self.easy_square.convert()
        
        # Medium box
        self.medium = pyg.image.load(os.path.join("Resources/Misc/medium.png"))
        self.medium = pyg.transform.scale(self.medium, (self.window_width / 5, self.window_height / 10))
        self.medium.convert()
        # Medium square
        self.medium_square = pyg.image.load(os.path.join("Resources/Misc/medium-square.png"))
        self.medium_square = pyg.transform.scale(self.medium_square, (self.window_width / 5 + 20, self.window_height / 10 + 20))
        self.medium_square.convert()

        # Hard box
        self.hard = pyg.image.load(os.path.join("Resources/Misc/hard.png"))
        self.hard = pyg.transform.scale(self.hard, (self.window_width / 5, self.window_height / 10))
        self.hard.convert()
        # Hard square
        self.hard_square = pyg.image.load(os.path.join("Resources/Misc/hard-square.png"))
        self.hard_square = pyg.transform.scale(self.hard_square, (self.window_width / 5 + 20, self.window_height / 10 + 20))
        self.hard_square.convert()

        self.buttons = [
            [[self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.new_game],
             [3 * self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.story_mode]],
            [[self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.easy],
             [2 * self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.medium],
             [3 * self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.hard]]
        ]

        self.squares = [
            [[self.buttons[0][0][0] - 10,  self.buttons[0][0][1] - 10, self.new_game_square],
             [self.buttons[0][1][0] - 10,  self.buttons[0][1][1] - 10, self.story_mode_square]],
            [[self.buttons[1][0][0] - 10,  self.buttons[1][0][1] - 10, self.easy_square],
             [self.buttons[1][1][0] - 10,  self.buttons[1][1][1] - 10, self.medium_square],
             [self.buttons[1][2][0] - 10,  self.buttons[1][2][1] - 10, self.hard_square]]
        ]

        # Music!
        pyg.mixer.music.load("Resources/Music/intro-song.mp3")
        pyg.mixer.music.play(-1, 0.0)

    def move_right(self):
        self.current_button = (self.current_button + 1) % len(self.buttons[self.current_stage])

    def move_left(self):
        self.current_button = (self.current_button + len(self.buttons[self.current_stage]) - 1) \
                              % len(self.buttons[self.current_stage])

    def select_button(self, controller):
        if self.current_stage == 0:
            if self.current_button == 1:
                controller.new_game()
                controller.game_mode = 1
            else:
                self.current_stage += 1
                self.current_button = 0
        else:
            if self.current_button == 0:
                controller.new_easy_level()
            elif self.current_button == 1:
                controller.new_medium_level()
            else:
                controller.new_hard_level()

    def go_back(self):
        self.current_stage = 0
        self.current_button = 0

    def draw(self, bg):
        bg.blit(self.background, (0, 0))
        bg.blit(self.squares[self.current_stage][self.current_button][2],
                (self.squares[self.current_stage][self.current_button][0],
                 self.squares[self.current_stage][self.current_button][1]))
        for button in self.buttons[self.current_stage]:
            bg.blit(button[2], (button[0], button[1]))
