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
            return not coordinates[0] <= s.get('bounds')[0] + s.get('offset_y')

        def down_bound_condition(coordinates):
            return not coordinates[0] >= s.get('bounds')[1] + s.get('offset_y')

        def left_bound_condition(coordinates):
            return not coordinates[1] <= s.get('bounds')[2] + s.get('offset_x')

        def right_bound_condition(coordinates):
            return not coordinates[1] >= s.get('bounds')[3] + s.get('offset_x')


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


    def get_new_position(self, direction):
        coordinates = self.position[:]

        mover = self.movements.get(direction)

        if mover.get('bound_condition')(coordinates):
            self.current_progression = self.progressions.get(direction)
            self.current_progression.update()

            index = mover.get('coord_index')
            operation = mover.get('operation')

            coordinates[index] = getattr(operator, operation)(
                coordinates[index],
                STEP_SIZES[index]
            )

        return coordinates


    def set_position(self, coordinates):
        if hasattr(self, 'position'):
            self.draw_char(' ')

        self.position = coordinates

        self.draw_char(self.current_progression.get_char())


    def draw_char(self, char):
        self.game_box.addch(
            self.position[0],
            self.position[1],
            char
        )

