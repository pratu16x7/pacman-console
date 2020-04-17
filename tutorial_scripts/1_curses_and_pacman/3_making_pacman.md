### Making Pacman, static - Editor
- abstraction, knows how to do things, if it has the map
- appear, disappear
- moving relative to box not screen
- getch after everything
- clear screen after all done

```python
# import curses

# class PacmanGame():
#     def __init__(self):
#         self.screen = curses.initscr()
#         curses.curs_set(0)
#         curses.noecho()

        self.init_screen()
        self.init_pacman()

        # Wait for key press
        self.map_box.getch()
        curses.endwin()


    # def init_screen(self):
    #     screen_h, screen_w = self.screen.getmaxyx()

    #     self.map_box = self.screen.subwin(
    #         int(screen_h/2),
    #         int(screen_w/2),
    #         int(screen_h/4),
    #         int(screen_w/4)
    #     )

    #     self.map_box.box()

    def init_pacman(self):
        h, w = self.map_box.getmaxyx()
        position = [h/2, w/2]
        self.pacman = Pacman(self.map_box, position)
        self.pacman.appear()


class Pacman():
    def __init__(self, map_box, position):
        self.map_box = map_box
        self.position = position

    def appear(self):
        self.draw_char('{')

    def disappear(self):
        self.draw_char(' ')

    def move(self, direction):
        pass

    def draw_char(self, char):
        self.map_box.addstr(
            self.position[0],
            self.position[1],
            char
        )


PacmanGame()

```
[editor] (Make pacman)
