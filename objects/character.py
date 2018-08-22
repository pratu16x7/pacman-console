import operator
from character_progression import CharProgression

HORIZONTAL_STEP_SIZE = 2
VERTICAL_STEP_SIZE = 1

STEP_SIZES = [
    VERTICAL_STEP_SIZE,
    HORIZONTAL_STEP_SIZE
]

class Pacman:
    def __init__(self, game_box, initial_position, screen):
        self.game_box = game_box

        # TODO: remove
        self.screen = screen

        self.init_progressions()
        self.init_movements()
        self.set_position(initial_position)


    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['v', 'V', '|', '|', 'V']),
            'DOWN': CharProgression('DOWN', ['^']),
            'LEFT': CharProgression('LEFT', ['}', ')', '>', '-', '-', '>', ')', '}']),
            'RIGHT': CharProgression('RIGHT', ['{', '(', '<', '-', '-', '<', '(', '{'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    def init_movements(self):

        # TODO: remove
        s = self.screen

        def up_bound_condition(coordinates):
            return not coordinates[0] <= s.get('bounds')[0]

        def down_bound_condition(coordinates):
            return not coordinates[0] >= s.get('bounds')[1]

        def left_bound_condition(coordinates):
            return not coordinates[1] <= s.get('bounds')[2]

        def right_bound_condition(coordinates):
            return not coordinates[1] >= s.get('bounds')[3]

        self.movements = {
            'UP': {
                'bound_condition': up_bound_condition,
                'operation': 'sub',
                'coord_index': 0
            },

            'DOWN': {
                'bound_condition': down_bound_condition,
                'operation': 'add',
                'coord_index': 0
            },

            'LEFT': {
                'bound_condition': left_bound_condition,
                'operation': 'sub',
                'coord_index': 1
            },

            'RIGHT': {
                'bound_condition': right_bound_condition,
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
        coordinates = self.current_position[:]

        mover = self.movements.get(direction)

        if mover.get('bound_condition')(coordinates):
            self.update_progression(direction)

            index = mover.get('coord_index')

            coordinates[index] = getattr(operator, mover.get('operation'))(
                coordinates[index],
                STEP_SIZES[index]
            )

        return coordinates


    def update_progression(self, direction):
        self.current_progression = self.progressions.get(direction)
        self.current_progression.update()


    def draw_char(self, char):
        self.game_box.addch(
            self.current_position[0],
            self.current_position[1],
            char
        )

