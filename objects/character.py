import operator
import abc
import curses
import random
from .character_progression import CharProgression

HORIZONTAL_STEP_SIZE = 2
VERTICAL_STEP_SIZE = 1

STEP_SIZES = [
    VERTICAL_STEP_SIZE,
    HORIZONTAL_STEP_SIZE
]

class Character:
    def __init__(self, game_box, initial_position):
        self.game_box = game_box

        # # TODO: COLOR!
        # curses.start_color()
        # curses.use_default_colors()
        # for i in range(0, curses.COLORS):
        #     curses.init_pair(i + 1, i, i)

        self.init_directions()
        self.init_progressions()
        self.init_movements()
        self.set_position(initial_position)


    def init_directions(self):
        self.directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']


    @abc.abstractmethod
    def init_progressions(self):
        self.progressions = {}
        return


    def init_movements(self):

        self.movements = {
            'UP': {
                'operation': 'sub',
                'coord_index': 0
            },

            'DOWN': {
                'operation': 'add',
                'coord_index': 0
            },

            'LEFT': {
                'operation': 'sub',
                'coord_index': 1
            },

            'RIGHT': {
                'operation': 'add',
                'coord_index': 1
            }
        }


    def move(self, direction):
        self.set_position(self.get_new_position(direction))


    def set_position(self, coordinates):
        if hasattr(self, 'current_position'):
            self.draw_char(' ')

        self.current_position = coordinates
        self.draw_char(self.current_progression.get_char())


    def get_new_position(self, direction):
        old_coordinates = self.current_position[:]

        new_coordinates = old_coordinates[:]

        mover = self.movements.get(direction)
        index = mover.get('coord_index')
        new_coordinates[index] = getattr(operator, mover.get('operation'))(
            new_coordinates[index],
            STEP_SIZES[index]
        )

        y = new_coordinates[0]
        x = new_coordinates[1]

        if self.game_box.map_matrix[y][x] != '#':
            self.update_progression(direction)
            return new_coordinates
        else:
            return old_coordinates


    def update_progression(self, direction):
        self.current_progression = self.progressions.get(direction)
        self.current_progression.update()


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


    def draw_char(self, char):
        self.game_box.map_box.addstr(
            int(self.current_position[0]),
            int(self.current_position[1]),
            char,
            # curses.color_pair(100)
        )




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

    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__(*args, **kwargs)


    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['M']),
            'DOWN': CharProgression('DOWN', ['M']),
            'LEFT': CharProgression('LEFT', ['M']),
            'RIGHT': CharProgression('RIGHT', ['M'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    def move_in_random_direction(self):
        current_direction = self.current_progression.name
        forward_directions = self.get_all_forward_directions(current_direction)
        possible_directions = []

        for d in forward_directions:
            if self.get_new_position(d) != self.current_position:
                possible_directions.append(d)

        if possible_directions:
            self.move(random.choice(possible_directions))
        else:
            self.move(self.get_opposite_direction(current_direction))
