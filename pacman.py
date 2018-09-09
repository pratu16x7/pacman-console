# coding: utf-8

import curses
import time
from objects.character import Pacman, Ghost
from objects.game_box import GameBox
from objects.color import Color

COLOR = Color(curses)


# The only things configurable are the map (walls + food) and object postions
DATA = {
    'map_file': 'maps/map.txt',
    'map_chars': {
        'wall': '█',
        'door': '-',
        'space': ' ',
        'food': '·'
    },
    'character_positions': {
        'pacman': [18, 29],
        'ghosts': [[12, 25], [12, 29], [12, 33], [11, 29]]
    },
}


LIVES = 3
FOOD_SCORE = 10


class PacmanGame():
    def __init__(self):
        self.screen_obj = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

        self.init_map()
        self.show_start_screen()


    def init_map(self):
        self.game_box = GameBox(
            self.screen_obj,
            DATA['map_file'],
            DATA['map_chars'],
            {
                'wall': COLOR.blue,
                'door': COLOR.blue,
                'space': COLOR.black,
                'food': COLOR.yellow
            }
        )


    def init_characters(self):
        positions = DATA['character_positions']
        ghost_pos = positions['ghosts']

        self.pacman = Pacman(
            self.game_box,
            COLOR.yellow,
            positions['pacman']
        )

        self.ghosts = {
            'Blinky': Ghost(
                self.game_box,
                COLOR.red,
                ghost_pos[0]
            ),

            'Pinky': Ghost(
                self.game_box,
                COLOR.pink,
                ghost_pos[1]
            ),

            'Inky': Ghost(
                self.game_box,
                COLOR.cyan,
                ghost_pos[2]
            ),

            'Clyde': Ghost(
                self.game_box,
                COLOR.orange,
                ghost_pos[3]
            )
        }


    def start_new_game(self):
        self.lives = LIVES
        self.score = 0

        self.game_box.set_map_matrix()
        self.game_box.draw_map()
        self.game_box.update_score(self.score)
        self.game_box.update_lives(self.lives)

        self.food_count = self.game_box.food_count
        self.food_count -= 1    # Initial position over food

        self.init_characters()
        self.run_game_loop()


    def restart(self):
        self.reset_positions()
        self.standby()
        self.run_game_loop()


    def standby(self):
        time.sleep(1)

        self.pacman.respawn()
        for ghost in self.ghosts.values():
            ghost.respawn()

        self.blink_characters()


    def win(self):
        self.show_win_screen()


    def end(self):
        self.show_game_over_screen()


    def run_game_loop(self):
        game_loop_running = True
        key = curses.KEY_RIGHT

        while game_loop_running:
            next_key = self.game_box.map_box.getch()
            key = key if next_key == -1 else next_key
            self.prev_position = self.pacman.current_position

            # Ghosts move
            for ghost in self.ghosts.values():
                ghost.move_in_random_direction()

            # Check state
            if not self.pacman.stopped:
                if self.food_eaten():
                    self.food_count -= 1
                    self.increment_score('food')

                    if self.food_count <= 0:
                        game_loop_running = False
                        time.sleep(1)
                        self.win()

            if self.ghost_touched():
                game_loop_running = False
                for ghost in self.ghosts.values():
                    ghost.vanish()

                self.die()

                self.game_box.map_box.refresh()

                if self.lives >= 0:
                    self.restart()
                else:
                    self.end()

            # Pacman moves
            if key == curses.KEY_UP:
                self.pacman.move('UP')

            if key == curses.KEY_DOWN:
                self.pacman.move('DOWN')

            if key == curses.KEY_LEFT:
                self.pacman.move('LEFT')

            if key == curses.KEY_RIGHT:
                self.pacman.move('RIGHT')



    def die(self):
        self.lives -= 1
        self.game_box.update_lives(self.lives)
        self.pacman.die()


    def increment_score(self, score_type):
        score_values = {
            'food': FOOD_SCORE
        }
        self.score += score_values[score_type]
        self.game_box.update_score(self.score)


    def reset_positions(self):
        positions = DATA['character_positions']
        ghost_pos = positions['ghosts']

        self.pacman.set_position(positions['pacman'])

        for idx, ghost in enumerate(self.ghosts.values()):
            ghost.set_position(ghost_pos[idx])


    def blink_characters(self):
        show = False
        for i in range(4):
            time.sleep(0.5)
            self.pacman.toggle(show)
            for ghost in self.ghosts.values():
                ghost.toggle(show)
            self.game_box.map_box.refresh()
            
            show = not show


    def food_eaten(self):
        y, x = self.pacman.current_position
        return self.game_box.map_matrix[y][x] == DATA['map_chars']['food']


    def ghost_touched(self):
        for ghost in self.ghosts.values():
            if ghost.current_position in (self.pacman.current_position,
                                          self.prev_position):
                return True
        return False


    def show_start_screen(self):
        blink_line_index = 0
        mesg_line = '|                 Press any key to START                  |'
        blank_line = '|                                                         |'

        with open('screens/start.txt') as screen:
            line_index = 0
            for line in screen:
                if 'Press' in line:
                    blink_line_index = line_index
                self.game_box.map_box.addstr(
                    line_index,
                    0,
                    line,
                    COLOR.blue if '█' in line else COLOR.yellow
                )
                line_index += 1

        self.game_box.border_box.refresh()

        start_screen_running = True
        show_msg = False

        while start_screen_running:
            next_key = self.game_box.map_box.getch()
            self.game_box.map_box.addstr(
                blink_line_index,
                0,
                mesg_line if show_msg else blank_line,
                COLOR.yellow
            )
            show_msg = not show_msg
            if next_key != -1:
                start_screen_running = False
                self.start_new_game()
            time.sleep(0.5)


    def show_win_screen(self):
        self.show_end_screen('screens/win.txt', COLOR.yellow)


    def show_game_over_screen(self):
        self.show_end_screen('screens/game_over.txt', COLOR.orange)


    def show_end_screen(self, filename, color):
        with open(filename) as screen:
            line_index = 7
            for line in screen:
                if 'SCORE: 0000' in line:
                    line = line.replace('SCORE: 0000', 'SCORE: ' + str(self.score).zfill(4))
                self.game_box.map_box.addstr(line_index, 0, line, color)
                line_index += 1

        self.game_box.border_box.refresh()
        game_over_screen_running = True

        while game_over_screen_running:
            next_key = self.game_box.map_box.getch()
            if next_key != -1:
                game_over_screen_running = False

                if next_key == 27:
                    curses.endwin()
                    exit()
                else:
                    self.start_new_game()


PacmanGame()
