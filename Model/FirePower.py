from Character import Character
from FireBall import FireBall
from Power import Power


class FirePower(Power):
    def __init__(self, rocky, state_number):
        Power.__init__(self, rocky, state_number)
        self.speed = int(self.rocky.speed * 1.5)
        self.jump_speed = -15
        self.last_fire = 0
        self.fire_rest = 1500

    def shoot_fire(self):
        self.last_fire = Character.current_time_millis()
        self.rocky.fireballs.append(FireBall(self.rocky.get_center_x(), self.rocky.get_center_y() - 8, self.rocky))

    def back_to_normal(self):
        self.rocky.is_fire = False

    def is_fire(self):
        return True