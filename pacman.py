import random
import curses
import time

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

bounds = [0, sh/2, 0, sw/2]

new_pos = [sh/2, sw/2]

key = curses.KEY_UP

while True:

    next_key = w.getch()

    key = key if next_key == -1 else next_key

    old_pos = new_pos[:]

    if key == curses.KEY_UP and not new_pos[0] <= bounds[0] + offset_y:
        new_pos[0] -= 1
    if key == curses.KEY_DOWN and not new_pos[0] >= bounds[1] + offset_y:
        new_pos[0] += 1
    if key == curses.KEY_LEFT and not new_pos[1] <= bounds[2] + offset_x:
        new_pos[1] -= 2
    if key == curses.KEY_RIGHT and not new_pos[1] >= bounds[3] + offset_x:
        new_pos[1] += 2

    s.addch(
        old_pos[0],
        old_pos[1],
        ' '
    )

    s.addch(
        new_pos[0],
        new_pos[1],
        curses.ACS_LARROW
    )

    s.getch()

