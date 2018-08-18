import random
import curses
import time

s = curses.initscr()
curses.curs_set(0)

s.border(0)

sh, sw = s.getmaxyx()
w = s.subwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

corners = [
    [0, 0],
    [0, sw/2],
    [sh/2, 0],
    [sh/2, sw/2]
]

offset_y = sh/4
offset_x = sw/4


box1 = s.subwin(sh/2, sw/2, offset_y, offset_x)
box1.box()


for corner in corners:
    s.addch(
        corner[0] + offset_y,
        corner[1] + offset_x,
        curses.ACS_PI
    )

while True:
    s.getch()
