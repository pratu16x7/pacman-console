
### Making a Box - Editor

```python
import curses

class PacmanGame():
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

        # New here
        screen_h, screen_w = self.screen.getmaxyx()

        self.map_box = self.screen.subwin(
            int(screen_h/2), int(screen_w/2),
            int(screen_h/4), int(screen_w/4)
        )

        self.map_box.box()

        # Wait for key press
        self.map_box.getch()

PacmanGame()

```
[editor] (Make a box)

