class CharProgression:
    def __init__(self, name, progression_cycle):
        self.name = name
        self.cycle = progression_cycle
        self.current_index = 0

    def get_char(self):
        return self.cycle[self.current_index]

    def update(self, reverse=False):
        if not reverse:
            self.update_forward()
        else:
            self.update_reverse()

    def update_forward(self):
        self.current_index += 1
        if self.current_index >= len(self.cycle):
            self.current_index = 0

    def update_reverse(self):
        self.current_index -= 1
        if self.current_index <= 0:
            self.current_index = len(self.cycle) - 1
