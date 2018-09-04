import operator
import abc
import curses
import random
from .character_progression import CharProgression


class Character:
    def __init__(self, game_box, initial_position, color):
        self.game_box = game_box
        self.color = color

        self.score = 0

        self.pass_over = False

        self.init_directions()
        self.init_progressions()
        self.set_position(initial_position)


    def init_directions(self):
        self.directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']


    @abc.abstractmethod
    def init_progressions(self):
        self.progressions = {}
        return


    def move(self, direction):
        new_position = self.game_box.get_new_position(self.current_position, direction)

        if new_position != self.current_position:
            self.update_progression(direction)
            self.set_position(new_position)


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
        y = int(self.current_position[0])
        x = int(self.current_position[1])

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
            if not self.pass_over:
                if self.game_box.map_matrix[y][x] == '·':
                    self.score += 1
                    self.game_box.update_score(self.score)

            self.game_box.map_matrix[y][x] = char


    def get_opposite_direction(self, direction):
        opposite_direction = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }

        return opposite_direction[direction]


    def get_all_forward_directions(self, current_direction):
        directions = self.directions[:]
        directions.remove(self.get_opposite_direction(current_direction))
        return directions




class Pacman(Character):
    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['v', 'V', '|', '|', 'V']),
            'DOWN': CharProgression('DOWN', ['^']),
            'LEFT': CharProgression('LEFT', ['}', ')', '>', '-', '-', '>', ')', '}']),
            'RIGHT': CharProgression('RIGHT', ['{', '(', '<', '-', '-', '<', '(', '{'])
        }

        self.current_progression = self.progressions.get('RIGHT')




class Ghost(Character):
    SPEED_DAMPER_LEVEL = 1

    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__(*args, **kwargs)
        self.wait_flag = 0
        self.pass_over = True


    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['M']),
            'DOWN': CharProgression('DOWN', ['M']),
            'LEFT': CharProgression('LEFT', ['M']),
            'RIGHT': CharProgression('RIGHT', ['M'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    def move_in_random_direction(self):
        if self.wait_flag < self.SPEED_DAMPER_LEVEL:
            self.wait_flag += 1
            return

        self.wait_flag = 0

        current_direction = self.current_progression.name
        forward_directions = self.get_all_forward_directions(current_direction)
        possible_directions = []

        for d in forward_directions:
            if self.game_box.get_new_position(self.current_position, d) != self.current_position:
                possible_directions.append(d)

        if possible_directions:
            self.move(random.choice(possible_directions))
        else:
            self.move(self.get_opposite_direction(current_direction))
