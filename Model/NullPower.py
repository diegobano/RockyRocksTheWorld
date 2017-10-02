from Power import Power


class NullPower(Power):
    def __init__(self, rocky, state_number):
        Power.__init__(self, rocky, state_number)
        self.rocky = rocky
        self.rocky_state = state_number
        self.speed = self.rocky.speed
        self.jump_speed = self.rocky.jump_speed

    def is_null_power(self):
        return True

    def back_to_normal(self):
        return

    def check_transformation(self):
        return