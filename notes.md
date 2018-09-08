Take care of the order of y and x (not x and y) coordinates. I messed up a lot.


no need to do these after initscr() I guess,
    curses.curs_set(0)
    curses.noecho()
    self.screen_obj.border(0)



# for corner in [ [0, 0], [0, sw/2], [sh/2, 0], [sh/2, sw/2] ]:
#     s.addch(
#         corner[0] + offset_y,
#         corner[1] + offset_x,
#         curses.ACS_PI
#     )

