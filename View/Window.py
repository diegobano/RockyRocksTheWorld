import pygame
__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Window:

    def __init__(self, screen, rocky, level, enemies, home, game_over):
        self.rocky = rocky
        self.level = level
        self.enemies = enemies
        self.home = home
        self.game_over = game_over
        self.win = screen
        self.color = (240,240,240)

    def clean(self):
        self.win.fill(self.color)

    def set_home(self, home):
        self.home = home

    def draw_game_over_screen(self):
        self.game_over.draw(self.win)
        pygame.display.flip()

    def draw_home_screen(self):
        self.home.draw(self.win)
        pygame.display.flip()

    def draw(self):
        self.level.draw(self.win)
        self.rocky.draw(self.win)
        for enemy in self.enemies:
            enemy.draw(self.win)
        #print self.rocky.get_x(), self.rocky.get_y()

        pygame.display.flip()