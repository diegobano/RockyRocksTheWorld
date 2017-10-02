import os
import pygame


class PlayerPoints:
    def __init__(self, numbers):
        self.points = 0
        self.numbers = numbers
        self.text = pygame.image.load(os.path.join("Resources/Numbers/points.png"))
        self.text = pygame.transform.scale(self.text, (self.numbers[0].get_size()[0] * 6, self.numbers[0].get_size()[1]))
        self.text.convert()
        self.x = 5
        self.y = 5

    def get_bound_x(self):
        return self.x + self.numbers[0].get_size()[0]

    def add_points(self, points):
        self.points += points

    def lose_points(self, points):
        self.points -= points

    def digit_at(self, pos):
        return (self.points / 10**(pos - 1)) % 10

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def restart(self):
        self.points = 0

    def draw(self, bg):
        bg.blit(self.text, (int(self.x), int(self.y)))
        for i in range(3):
            bg.blit(self.numbers[self.digit_at(3 - i)], (int(self.text.get_size()[0] + 10 + self.x + (self.get_bound_x() + 3) * i), int(self.y)))
