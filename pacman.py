import curses
# import random
# import time
from objects.character import Pacman
from objects.game_box import GameBox


class PacmanGame:
    def __init__(self):
        self.init_curses_and_screen()
        self.init_map()
        # self.init_characters()
        self.start()


    def init_curses_and_screen(self):
        self.screen_obj = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        self.screen_obj.border(0)


    # def init_screen(self):
    #     self.screen = {
    #         'height': h,
    #         'width': w,
    #         'offset_y': int(h/4),
    #         'offset_x': int(w/4),
    #         'bounds': [2, h/2 - 3, 2, w/2 + 1]
    #     }

    def init_map(self):
        self.game_box = GameBox(self.screen_obj)


    # def init_characters(self):
    #     # TODO: remove
    #     s = self.screen

    #     self.pacman = Pacman(
    #         self.game_box,
    #         [s.get('height')/2, s.get('width')/2],
    #         s
    #     )


    def start(self):
        key = curses.KEY_RIGHT
        while True:
            next_key = self.game_box.map_box.getch()
            # key = key if next_key == -1 else next_key

            # if key == curses.KEY_UP:
            #     self.pacman.move('UP')

            # if key == curses.KEY_DOWN:
            #     self.pacman.move('DOWN')

            # if key == curses.KEY_LEFT:
            #     self.pacman.move('LEFT')

            # if key == curses.KEY_RIGHT:
            #     self.pacman.move('RIGHT')

            self.screen_obj.getch()


PacmanGame()
