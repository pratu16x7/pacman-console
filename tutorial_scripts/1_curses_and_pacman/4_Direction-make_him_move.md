### Make him move - Editor

- Concept of Direction, programatically
- Multiple inheritance in Python
- Pacman doesn't understand direction, just knows to update it's position

```python
import curses

class PacmanGame():
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

        self.init_screen()
        self.init_pacman()

        self.start()

        # Wait for key press
        # self.map_box.getch()
        # curses.endwin()


    def init_screen(self):
        screen_h, screen_w = self.screen.getmaxyx()

        self.map_box = self.screen.subwin(
            int(screen_h/2),
            int(screen_w/2),
            int(screen_h/4),
            int(screen_w/4)
        )

        self.map_box.box()

        # self.map_box.addstr(
        #     int(self.position[0]),
        #     int(self.position[1]),
        #     char
        # )

    def init_pacman(self):
        h, w = self.map_box.getmaxyx()
        position = [h/2, w/2]
        self.position = position
        self.pacman = Pacman(self.map_box, position)
        self.pacman.appear()


    def start(self):
        self.map_box.keypad(1)
        self.map_box.timeout(100)

        while True:
            key = self.map_box.getch()
            # print('foo')
            # print('foo', chr(self.map_box.inch(int(self.position[0]), int(self.position[1]))))

            if key == curses.KEY_UP:
                self.pacman.move(UP)

            if key == curses.KEY_DOWN:
                self.pacman.move(DOWN)

            if key == curses.KEY_LEFT:
                self.pacman.move(LEFT)

            if key == curses.KEY_RIGHT:
                self.pacman.move(RIGHT)


UP_PROG = ['v', 'V', '|', '|', 'V', 'v']
DOWN_PROG = ['^']
LEFT_PROG = ['}', ')', '>', '-', '-', '>', ')', '}']
RIGHT_PROG = ['{', '(', '<', '-', '-', '<', '(', '{']

class Pacman():
    def __init__(self, map_box, position):
        self.map_box = map_box
        self.char = '{'
        self.position = position

    def appear(self):
        self.draw_char(self.char)

    def disappear(self):
        self.draw_char(' ')

    def move(self, direction):
        self.disappear()
        self.position = direction(self.position)
        self.appear()

    def draw_char(self, char):
        self.map_box.addstr(
            int(self.position[0]),
            int(self.position[1]),
            char
        )

import operator

X_STEP_SIZE = 2
Y_STEP_SIZE = 1

def get_next_position(position, operator, coord_index, step_size):
    new_position = position[:]
    i, step, op = coord_index, step_size, operator
    new_position[i] = op(position[i], step)
    return new_position

INCR = operator.add
DECR = operator.sub

Y = {'coord_index': 0, 'step_size': Y_STEP_SIZE}
X = {'coord_index': 1, 'step_size': X_STEP_SIZE}

# You give it the position, and decrement it according to the Y rules
def UP(position): return get_next_position(position, DECR, **Y)
def DOWN(position): return get_next_position(position, INCR, **Y)
def LEFT(position): return get_next_position(position, DECR, **X)
def RIGHT(position): return get_next_position(position, INCR, **X)


class Progression():
    def __init__(self, progression_cycle):
        self.cycle = progression_cycle
        self.index = 0

    @property
    def char(self):
        # forward default
        self.update()
        return self.cycle[self.index]

    def update(self):
        self.update_forward()

    def update_forward(self):
        self.index += 1
        if self.index >= len(self.cycle):
            self.index = 0


PacmanGame()


```
[editor] (Make pacman move)
