import random
import curses
import time

from character import Pacman


class PacmanGame:
    def __init__(self):
        self.init_curses()
        self.init_screen()
        self.init_map()
        self.init_characters()
        self.start()


    def init_curses(self):
        self.screen_obj = curses.initscr()
        curses.curs_set(0)
        curses.noecho()


    def init_screen(self):
        s = self.screen_obj
        s.border(0)

        h, w = s.getmaxyx()

        self.screen = {
            'height': h,
            'width': w,
            'offset_y': h/4,
            'offset_x': w/4,
            'bounds': [0, h/2, 0, w/2]
        }


    def init_map(self):
        s = self.screen
        self.game_box = self.screen_obj.subwin(
            s.get('height')/2 + 3,
            s.get('width')/2 + 6,
            s.get('offset_y') - 1,
            s.get('offset_x') - 2
        )
        self.game_box.box()
        self.game_box.keypad(1)
        self.game_box.timeout(100)


    def init_characters(self):
        # TODO: remove
        s = self.screen

        self.pacman = Pacman(
            self.game_box,
            [s.get('height')/2, s.get('width')/2],
            s
        )


    def start(self):
        s = self.screen

        key = curses.KEY_RIGHT

        while True:
            next_key = self.game_box.getch()
            key = key if next_key == -1 else next_key

            if key == curses.KEY_UP:
                self.pacman.move('UP')

            if key == curses.KEY_DOWN:
                self.pacman.move('DOWN')

            if key == curses.KEY_LEFT:
                self.pacman.move('LEFT')

            if key == curses.KEY_RIGHT:
                self.pacman.move('RIGHT')

            self.screen_obj.getch()


PacmanGame()
