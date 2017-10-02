
class LevelBlock:
    def __init__(self, initial_x, initial_y, width, height, sprite):
        self.x = initial_x
        self.y = initial_y
        self.width = width
        self.height = height
        self.sprite = sprite

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_bound_x(self):
        return self.x + self.sprite.get_size()[0]

    def get_bound_y(self):
        return self.y + self.sprite.get_size()[1]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def move(self, speed):
        self.x += speed

    def draw(self, bg):
        bg.blit(self.sprite, (int(self.x), int(self.y)))