import time
import pygame as pyg
import os


class Counter:
    def __init__(self, x, total, numbers):
        self.total = total
        self.initial_time = time.time()
        self.remaining = int(self.total - (time.time() - self.initial_time))
        self.numbers = numbers
        self.time = pyg.image.load(os.path.join("Resources/Numbers/time.png"))
        self.time = pyg.transform.scale(self.time, (self.numbers[0].get_size()[0] * 4 +
                                                              self.numbers[0].get_size()[0] / 3,
                                                              self.numbers[0].get_size()[1]))
        self.time.convert()
        self.x = x
        self.y = 5

    def update(self):
        self.remaining = int(self.total - (time.time() - self.initial_time))

    def restart(self):
        self.initial_time = time.time()

    def digit_at(self, pos):
        return (self.remaining / 10**(pos - 1)) % 10

    def draw(self, bg):
        bg.blit(self.time, (int(self.x - self.time.get_size()[0] - 10), int(self.y)))
        for i in range(3):
            bg.blit(self.numbers[self.digit_at(3 - i)], (int(self.x + (self.numbers[0].get_size()[0] + 3)* i), int(self.y)))
