### Begin coding - Editor

```python

import curses

```

[editor](main.py) and start of by importing curses

















### ASIDE: Curses documentation
- TODO later

[browser](page-curses) we'll do an overview on what curses actually is, but first just let's get stuff on the screen for starters.

















### Start curses screen - Editor
- PacmanGame Object

```python

import curses

class PacmanGame():
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

```
[editor] We'll go ahead and make a PacmanGame class, and initialize all the variables. screen ... echo ...
















### Addstr to show what that does - Editor
- Coord system

```python

import curses

class PacmanGame():
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

        self.screen.addstr(10, 25, 'Hello World')

        self.screen.getch()

PacmanGame()

```
[editor] You know what, let's run pacmangame, and check it out!














### First Tryout  - Split Screen
```bash
$ python main.py
```
[terminal] Let's just quickly see what that does (blank screen for 3 seconds). So there we have the terminal screen cleared for us to play. That's actually a curses screen object. Right now we're using sleep to see it, but while playing we'll make wait for keystrokes
