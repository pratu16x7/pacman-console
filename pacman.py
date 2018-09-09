import curses
from objects.character import Pacman, Ghost
from objects.game_box import GameBox
from objects.color import Color

COLOR = Color(curses)

# The only things configurable are the map (walls + food) and object postions
DATA = {
    'map_file': 'maps/map.txt',
    'character_positions': {
        'pacman': [18, 29],
        'ghosts': [[12, 25], [12, 29], [12, 33], [11, 29]]
    }
}

class PacmanGame():
    def __init__(self):
        self.screen_obj = curses.initscr()
        self.init_map()
        self.init_characters()

        self.lives = 3
        self.score = 0

        self.start()


    def init_map(self):
        self.game_box = GameBox(
            self.screen_obj,
            DATA['map_file'],
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


    def start(self):
        self.run_game_loop()


    def restart(self):
        self.reset_positions()
        self.run_game_loop()


    def standby(self):
        return


    def end(self):
        return


    def run_game_loop(self):
        game_loop_running = True
        key = curses.KEY_RIGHT

        while game_loop_running:
            next_key = self.game_box.map_box.getch()
            key = key if next_key == -1 else next_key

            # Pacman moves
            if key == curses.KEY_UP:
                self.pacman.move('UP')

            if key == curses.KEY_DOWN:
                self.pacman.move('DOWN')

            if key == curses.KEY_LEFT:
                self.pacman.move('LEFT')

            if key == curses.KEY_RIGHT:
                self.pacman.move('RIGHT')

            # Ghosts move
            for ghost in self.ghosts.values():
                ghost.move_in_random_direction()

            if not self.pacman.stopped:
                if self.food_eaten():
                    self.increment_score('food')

            if self.ghost_touched():
                game_loop_running = False
                self.kill_pacman()

                # if self.lives > 0:
                #     self.restart()
                # else:
                #     self.end()

    def food_eaten(self):
        y, x = self.pacman.current_position
        return self.game_box.map_matrix[y][x] == '·'


    def ghost_touched(self):
        for ghost in self.ghosts.values():
            if self.pacman.current_position == ghost.current_position:
                return True
        return False


    def increment_score(self, score_type):
        score_values = {
            'food': 10
        }
        self.score += score_values[score_type]
        self.game_box.update_score(self.score)


    def reset_positions(self):
        return


    def kill_pacman(self):
        self.lives -= 1
        self.pacman.die()
        for ghost in self.ghosts.values():
            ghost.vanish()
        # self.pacman


PacmanGame()
