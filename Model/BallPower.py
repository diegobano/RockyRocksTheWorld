from Power import Power


class BallPower(Power):
    def __init__(self, rocky, state_number):
        Power.__init__(self, rocky, state_number)
        self.speed = self.rocky.speed * 2
        self.jump_speed = -15

    def back_to_normal(self):
        self.rocky.is_ball = False

    def is_ball(self):
        return True