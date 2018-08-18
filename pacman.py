import random
import curses
import time

class CharProgression:
    def __init__(self, name, progression_cycle):
        self.name = name
        self.cycle = progression_cycle
        self.current_index = 0

    def get_char(self):
        return self.cycle[self.current_index]

    def update(self, reverse=False):
        if not reverse:
            self.current_index += 1
            if self.current_index >= len(self.cycle):
                self.current_index = 0
        else:
            self.current_index -= 1
            if self.current_index <= 0:
                self.current_index = len(self.cycle) - 1

# SETUP
s = curses.initscr()
curses.curs_set(0)

s.border(0)

sh, sw = s.getmaxyx()
w = s.subwin(sh, sw, 0, 0)
curses.noecho()
w.keypad(1)
w.timeout(100)

offset_y = sh/4
offset_x = sw/4


box1 = s.subwin(sh/2 + 3, sw/2 + 6, offset_y - 1, offset_x - 2)
box1.box()


# for corner in [ [0, 0], [0, sw/2], [sh/2, 0], [sh/2, sw/2] ]:
#     s.addch(
#         corner[0] + offset_y,
#         corner[1] + offset_x,
#         curses.ACS_PI
#     )

map1 = []

bounds = [0, sh/2, 0, sw/2]


# CHAR PROGRESSIONS
right_progression = CharProgression('right', ['{', '(', '<', '-', '-', '<', '(', '{'])
left_progression = CharProgression('left', ['}', ')', '>', '-', '-', '>', ')', '}'])
up_progression = CharProgression('up', ['v', 'V', '|', '|', 'V'])
down_progression = CharProgression('down', ['^'])

# INIT
new_pos = [sh/2, sw/2]
current_progression = right_progression

key = curses.KEY_RIGHT

while True:

    next_key = w.getch()

    key = key if next_key == -1 else next_key

    old_pos = new_pos[:]

    if key == curses.KEY_UP and not new_pos[0] <= bounds[0] + offset_y:
        current_progression = up_progression
        new_pos[0] -= 1

    if key == curses.KEY_DOWN and not new_pos[0] >= bounds[1] + offset_y:
        current_progression = down_progression
        new_pos[0] += 1

    if key == curses.KEY_LEFT and not new_pos[1] <= bounds[2] + offset_x:
        current_progression = left_progression
        new_pos[1] -= 2

    if key == curses.KEY_RIGHT and not new_pos[1] >= bounds[3] + offset_x:
        current_progression = right_progression
        new_pos[1] += 2

    current_progression.update()

    s.addch(
        old_pos[0],
        old_pos[1],
        ' '
    )

    s.addch(
        new_pos[0],
        new_pos[1],
        current_progression.get_char()
    )

    s.getch()

