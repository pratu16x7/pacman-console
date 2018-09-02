import curses
from objects.character import Pacman, Ghost
from objects.game_box import GameBox


class PacmanGame:
    def __init__(self):
        self.init_curses_and_screen()
        self.init_color()
        self.init_map()
        self.init_characters()
        self.start()


    def init_curses_and_screen(self):
        self.screen_obj = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        self.screen_obj.border(0)


    def init_color(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1 + 300, i, i)


    def init_map(self):
        black = 233
        blue = 22

        blue_fill = 278

        self.game_box = GameBox(self.screen_obj, {
            'wall': curses.color_pair(blue_fill),
            'door': curses.color_pair(blue),
            'space': curses.color_pair(black)
        })


    def init_characters(self):
        self.pacman = Pacman(
            self.game_box,
            [18, 29],
            curses.color_pair(12)
        )

        self.ghosts = {
            'Blinky': Ghost(
                self.game_box,
                [12, 25],
                curses.color_pair(2)
            ),

            'Pinky': Ghost(
                self.game_box,
                [12, 29],
                curses.color_pair(14)
            ),

            'Inky': Ghost(
                self.game_box,
                [12, 33],
                curses.color_pair(15)
            ),

            'Clyde': Ghost(
                self.game_box,
                [11, 29],
                curses.color_pair(209)
            )
        }


    def start(self):
        key = curses.KEY_RIGHT
        while True:
            next_key = self.game_box.map_box.getch()
            key = key if next_key == -1 else next_key

            if key == curses.KEY_UP:
                self.pacman.move('UP')

            if key == curses.KEY_DOWN:
                self.pacman.move('DOWN')

            if key == curses.KEY_LEFT:
                self.pacman.move('LEFT')

            if key == curses.KEY_RIGHT:
                self.pacman.move('RIGHT')

            # TODO: find a way to wait
            # self.screen_obj.getch()

            self.ghosts['Blinky'].move_in_random_direction()
            self.ghosts['Pinky'].move_in_random_direction()
            self.ghosts['Inky'].move_in_random_direction()
            self.ghosts['Clyde'].move_in_random_direction()


PacmanGame()
