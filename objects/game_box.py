import curses
import operator

HORIZONTAL_STEP_SIZE = 2
VERTICAL_STEP_SIZE = 1

STEP_SIZES = [
    VERTICAL_STEP_SIZE,
    HORIZONTAL_STEP_SIZE
]

class GameBox:
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors

        self.init_map_matrix()
        self.init_map_box()
        self.draw_map()
        self.init_directions()
        self.init_movements()


    def init_map_matrix(self):
        self.map_matrix = []
        self.color_matrix = []
        # with open('../maps/map.txt') as map_file:
        with open('maps/map.txt') as map_file:
            for line in map_file:
                # trim the new_line char
                self.map_matrix.append(list(line)[:-1])
                self.color_matrix.append(list(line)[:-1])

        # # TODO:
        # # Better checks to validate map files, to parse them seamlessly


    def init_map_box(self):
        screen_h, screen_w = self.screen.getmaxyx()

        m = self.map_matrix
        self.map_h, self.map_w = len(m), len(m[0])

        offset_y = int((screen_h - self.map_h)/2)
        offset_x = int((screen_w - self.map_w)/2)

        self.map_box = self.screen.subwin(
            self.map_h,
            self.map_w,
            offset_y,
            offset_x
        )

        self.map_box.keypad(1)
        self.map_box.timeout(100)

        self.border_box = self.screen.subwin(
            self.map_h + 10,
            self.map_w + 10,
            offset_y - 5,
            offset_x - 5
        )
        self.border_box.box()


        self.update_score(0)
        self.update_lives(3)


    def draw_map(self):
        color = self.colors['wall']

        line_index = 0
        for line in self.map_matrix:
            char_index = 0
            for char in line:
                if char == '#':
                    color = self.colors['wall']
                if char == ' ':
                    color = self.colors['space']
                if char == '-':
                    color = self.colors['door']
                if char == '·':
                    color = self.colors['food']
                self.map_box.addstr(
                    line_index,
                    char_index,
                    char,
                    color
                )

                self.color_matrix[line_index][char_index] = color

                char_index += 1
            line_index += 1


    def update_score(self, score):
        self.border_box.addstr(self.map_h + 10 - 1, 5, '[ Score: {0} ]'.format(score))
        self.border_box.refresh()


    def update_lives(self, lives):
        self.border_box.addstr(self.map_h + 10 - 1, 20, '[ Lives: {0} ]'.format('(<  (<  (<'))
        self.border_box.refresh()


    def init_directions(self):
        self.directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']


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


    def get_new_position(self, old_coordinates, direction):
        new_coordinates = old_coordinates[:]

        mover = self.movements.get(direction)
        index = mover.get('coord_index')
        new_coordinates[index] = getattr(operator, mover.get('operation'))(
            new_coordinates[index],
            STEP_SIZES[index]
        )

        # Wrap position:
        # horizontally
        width = len(self.map_matrix[0])
        if new_coordinates[1] < 0:
            new_coordinates[1] = width - 3
        if new_coordinates[1] >= width - 1:
            new_coordinates[1] = 1

        y = new_coordinates[0]
        x = new_coordinates[1]

        if self.map_matrix[y][x] != '#':
            return new_coordinates
        else:
            return old_coordinates


    def update_map_matrix(self, y, x, char, ):
        pass
