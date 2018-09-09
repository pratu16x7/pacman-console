import abc
import random
import time
from .character_progression import CharProgression


class Character():
    def __init__(self, game_box, color, initial_position=None):
        self.game_box = game_box
        self.color = color

        self.pass_over = False
        self.stopped = False

        self.init_progressions()

        if initial_position:
            self.set_position(initial_position)


    @abc.abstractmethod
    def init_progressions(self):
        self.progressions = {}
        return


    def appear(self):
        self.draw_char(self.current_progression.get_char(), False)


    def vanish(self):
        self.draw_char(' ', False)


    def toggle(self, show=True):
        if show:
            self.appear()
        else:
            self.vanish()


    def move(self, direction):
        new_position = self.game_box.get_new_position(self.current_position, direction)

        if new_position != self.current_position:
            self.stopped = False
            self.update_progression(direction)
            self.set_position(new_position)
        else:
            self.stopped = True


    def set_position(self, coordinates):
        if hasattr(self, 'current_position'):
            if not self.pass_over:
                self.draw_char(' ')
            else:
                self.draw_char(' ', True, True)

        self.current_position = coordinates
        self.draw_char(self.current_progression.get_char(), False)


    def update_progression(self, direction):
        self.current_progression = self.progressions.get(direction)
        self.current_progression.update()


    def draw_char(self, char, update=True, redraw=False):
        y, x = self.current_position

        color = self.color

        if redraw:
            char = self.game_box.map_matrix[y][x]
            color = self.game_box.color_matrix[y][x]

        self.game_box.map_box.addstr(
            y,
            x,
            char,
            color
        )

        if update:
            self.game_box.map_matrix[y][x] = char




class Pacman(Character):
    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['v', 'V', '|', '|', 'V', 'v']),
            'DOWN': CharProgression('DOWN', ['^']),
            'LEFT': CharProgression('LEFT', ['}', ')', '>', '-', '-', '>', ')', '}']),
            'RIGHT': CharProgression('RIGHT', ['{', '(', '<', '-', '-', '<', '(', '{'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    def die(self):
        self.appear()
        for char in ['O', 'o', '.', "'", '*', ' ']:
            time.sleep(0.2)
            self.draw_char(char, False)
            self.game_box.map_box.refresh()
        self.vanish()


    def respawn(self):
        self.appear()




class Ghost(Character):
    SPEED_DAMPER_LEVEL = 1

    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__(*args, **kwargs)
        self.pass_over = True
        self.wait_flag = 0


    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['M']),
            'DOWN': CharProgression('DOWN', ['M']),
            'LEFT': CharProgression('LEFT', ['M']),
            'RIGHT': CharProgression('RIGHT', ['M'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    def move_in_random_direction(self, bias=None):
        if self.wait_flag < self.SPEED_DAMPER_LEVEL:
            self.wait_flag += 1
            return

        self.wait_flag = 0

        box = self.game_box

        current_direction = self.current_progression.name
        forward_directions = box.get_all_forward_directions(current_direction)
        possible_directions = []

        for d in forward_directions:
            if box.get_new_position(self.current_position, d) != self.current_position:
                possible_directions.append(d)

        if possible_directions:
            self.move(random.choice(possible_directions))
        else:
            self.move(box.get_opposite_direction(current_direction))


    def respawn(self):
        self.appear()
