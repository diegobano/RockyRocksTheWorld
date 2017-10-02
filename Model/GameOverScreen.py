import os
import pygame as pyg


class GameOverScreen:
    def __init__(self, w_width, w_height, points):
        # Parameters
        self.window_width = w_width
        self.window_height = w_height
        self.current_button = 0
        self.leave_home = False
        self.points = points
        self.points.set_coords(self.window_width / 2 - (self.points.get_bound_x() * 9) / 2, 50)

        # Background image
        self.background = pyg.image.load(os.path.join("Resources/Misc/game-over.jpg"))
        self.background = pyg.transform.scale(self.background, (self.window_width, self.window_height))
        self.background.convert()

        # First screen
        # New game box
        self.play_again = pyg.image.load(os.path.join("Resources/Misc/new-game.png"))
        self.play_again = pyg.transform.scale(self.play_again, (self.window_width / 4, self.window_height / 10))
        self.play_again.convert()
        # New game square
        self.play_again_square = pyg.image.load(os.path.join("Resources/Misc/new-game-square.png"))
        self.play_again_square = pyg.transform.scale(self.play_again_square,
                                                   (self.window_width / 4 + 20, self.window_height / 10 + 20))
        self.play_again_square.convert()

        self.exit = pyg.image.load(os.path.join("Resources/Misc/exit.png"))
        self.exit = pyg.transform.scale(self.exit, (self.window_width / 4, self.window_height / 10))
        self.exit.convert()
        # New game square
        self.exit_square = pyg.image.load(os.path.join("Resources/Misc/exit-square.png"))
        self.exit_square = pyg.transform.scale(self.exit_square,
                                                     (self.window_width / 4 + 20, self.window_height / 10 + 20))
        self.exit_square.convert()

        self.buttons = [[self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.play_again],
                        [3 * self.window_width / 4 - self.window_width / 8, 3 * self.window_height / 4, self.exit]
                        ]

        self.squares = [[self.buttons[0][0] - 10, self.buttons[0][1] - 10, self.play_again_square],
                        [self.buttons[1][0] - 10, self.buttons[1][1] - 10, self.exit_square]]

        # Music!
        self.music = "Resources/Music/game-over.mp3"

    def move_right(self):
        self.current_button = (self.current_button + 1) % len(self.buttons)

    def move_left(self):
        self.current_button = (self.current_button + len(self.buttons) - 1) \
                              % len(self.buttons)

    def select_button(self, controller):
        if self.current_button == 1:
            controller.quit_game()
        else:
            controller.restart_all()

    def set_points(self, points):
        self.points = points
        self.points.set_coords(self.window_width / 2 - (self.points.get_bound_x() * 9) / 2, 50)

    def draw(self, bg):
        bg.blit(self.background, (0, 0))
        bg.blit(self.squares[self.current_button][2],
                (self.squares[self.current_button][0],
                 self.squares[self.current_button][1]))
        for button in self.buttons:
            bg.blit(button[2], (button[0], button[1]))
        self.points.draw(bg)