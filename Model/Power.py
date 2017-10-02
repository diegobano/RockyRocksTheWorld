from Character import Character


class Power:
    def __init__(self, rocky, state_number):
        self.rocky = rocky
        self.rocky_state = state_number
        self.transformation_start = 0
        self.transformation_time = 500
        self.transformation_rate = 50
        self.last_transformation_change = 0
        self.last_sprite = 0

    def stop_transforming(self):
        self.rocky.transforming = False

    def get_power(self):
        if self.rocky.current_state != self.rocky_state:
            self.rocky.current_power = self
            self.rocky.speed_x = 0
            self.rocky.current_state = self.rocky_state
            self.rocky.transforming = True
            self.transformation_start = Character.current_time_millis()
            self.rocky.set_power(self)

    def change_transformation_sprite(self):
        self.last_transformation_change = Character.current_time_millis()
        self.last_sprite = self.rocky.current_state - self.last_sprite
        if self.rocky.facing_forward:
            self.rocky.sprite = self.rocky.front_sprites[self.last_sprite]
        else:
            self.rocky.sprite = self.rocky.back_sprites[self.last_sprite]

    def check_transformation(self):
        if Character.current_time_millis() - self.last_transformation_change >= self.transformation_rate:
            self.change_transformation_sprite()

    def is_fire(self):
        return False

    def is_ball(self):
        return False

    def is_null_power(self):
        return False
