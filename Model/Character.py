import time


class Character:
    def __init__(self, initial_x, initial_y, w_width, w_height, speed, acceleration, size):
        # Useful variables
        self.x = initial_x
        self.y = initial_y
        self.window_width = w_width
        self.window_height = w_height
        self.acceleration = acceleration
        self.speed_x = 0
        self.speed_y = 0
        self.alive = True
        self.speed = speed
        self.current_state = 0
        self.size = size
        self.facing_forward = True
        self.speeds = [self.speed, self.speed]
        self.lives = 3
        self.current_power = None

    @staticmethod
    def current_time_millis():
        return int(round(time.time() * 1000))

    def move_right(self):
        self.facing_forward = True
        if self.current_power is None:
            self.speed_x = self.speed
        else:
            self.speed_x = self.current_power.speed


    def move_left(self):
        self.facing_forward = False
        if self.current_power is None:
            self.speed_x = -self.speed
        else:
            self.speed_x = -self.current_power.speed

    def stop_moving_x(self):
        self.speed_x = 0

    def stop_moving_y(self):
        self.speed_y = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_bound_x(self):
        return self.size + self.x

    def get_bound_y(self):
        return self.size + self.y

    def is_alive(self):
        return self.alive

    def get_center_x(self):
        return (self.get_bound_x() + self.get_x()) / 2

    def get_center_y(self):
        return (self.get_bound_y() + self.get_y()) / 2

    def kill(self):
        self.lives = 0
        self.alive = False
