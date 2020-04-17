<!-- META
1.  Problem: Talk naturally, with normal pitch and breath
    Plausible solution: Talk loudly along with videos for hours, to get the modulation down
2.  Problem: Transitioning to next topic, and being natural about it
    Plausible solutions:
    First define a logical succession, the introducs the new one, avoid "Now ...", rather say, "Wait, but what if I want to ..."
    Just copy someone else's and go with it, hint, HELLO INTERNET
-->


Hi everyone, I'll talking about how to make a console pacman game in Python. Let's just jump right in.

------------

Right, Let's make a main.py,

and import curses

have our PacmanGame class, where I begin __init__iliazing.

Now I'll tell curses to make a screen for us.

and tell it to print a string at position 10, 25 'Hello world'

Let's instantiate it PacmanGame()

[Terminal]

and see how that looks

Well I didn't see it because the program ended right away

Let's tell it to wait for a keypress ... (getch())

There we go. Hello world at y=10, x=25

A good time to introduce the game loop concept here, I invoke an infinite loop that keeps waiting for the next key. LEt's try that out.

See? now I get to press as many keys as I want. useful for playing the game later on

couple of things to notice here, are the cursor and the the character echo when I pressed a key. See that there? the 'h'? Let's turn those off.

[sample]
```py
import curses

class PacmanGame():
    def __init__(self):
        self.screen = curses.initscr()

        curses.curs_set(0)
        # curses.noecho()

        self.screen.addstr(10, 25, 'Hello World!')

        while True:
            self.screen.getch()

PacmanGame()
```




-------------------

Let's make a box

To do that, I need the screen parameters width and height so that I can make a box, or subwindow with relative measures.

I tell it to give it half the height and width, and start making it at point at the quarter of the screen

and box it

```py
    screen_h, screen_w = self.screen.getmaxyx()

    self.map_box = self.screen.subwin(
        int(screen_h/2), int(screen_w/2),
        int(screen_h/4), int(screen_w/4)
    )

    self.map_box.box()
```

-------------------

Now for the exciting part, lets make PACMAN himself!

For that, I'll just go ahead and separate out the screen initialization

and let's initialize pacman (init_pacman())

Now all I do now will be wrt to the box I just made

so to put him in the center of the box, I'll just get the box params

(the subwin object is just a tiny version of the screen itself, so it has all the screen utilities)

and print our pacman as a curly brace

```py
def init_pacman(self):
    h, w = self.map_box.getmaxyx()
    position = [h/2, w/2]
    self.map_box.addstr(position[0], position[2], '{')
```

Yay!

but hold on, that's no pacman, it has no character.

he should know how to do things, and be aware of his surroundings

Like, instead of this, imagine if you were able to do this: Give it his surroundings, and his position, and tell him to appear ... !

```py
    self.pacman = Pacman(self.map_box, position)
    self.pacman.appear()
```

"Turns out, the joys of Objcet oriented programming mean that I _can_ give it character"

Let's make a real Pacman

At first he simply knows where he's dumped

And he knows how to appear

to dissappear

and to move ...

well appearing and disappearing is easy, I draw his character, or I erase it (draw_char())

and I already know how to do that (def draw_char, addstr)

```py
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
```

Let's try that ... great

But moving, is trickier.

--------------------------

The trouble is, he has no sense of direction yet. For our purposes, what I mean is,
he should be able to do this,


                                        [3, 7]
                                           |
                                           |
                                           | .move('UP')
                                           |
                                           |
                                           |
                       .move('LEFT')              .move('RIGHT')
             [4, 6]   <-------------   { [4, 7]   ------------->    [4, 8]

                                           |
                                           |
                                           | .move('DOWN')
                                           |
                                           |

                                         [5, 7]



Starting from my initial example position: [4, 7]
Let's jot down rules:

Now what I know is that, in computer graphics, the coord system looks like this:

thinngs to note here are:



                           THE CG CO_ORDINATE SYSTEM
                          """""""""""""""""""""""""""

                    |
                 -2 |
                    |
                 -1 |
    -3   -2   -1    |    1    2    3    4    5    6    7    8    9   10   11
    ----------------+-----------------------------------------------------------  X
                    | 0
                  1 |
                    |      This is the CG co-ord system
                  2 |
                    |
                  3 |      As it mimics the way things are printed
                    |      on a screen,
                  4 |
                    |      Y direction is POSITIVE DOWNWARDS
                  5 |
                    |
                  6 |      Also, as points are described as [which_ROW, which_COL]
                    |
                  7 |      coordinates are noted as [Y, X], NOT [X, Y]
                    |
                  8 |
                    |
                  9 |      UP:     (-)   Y                  |   (-)    (+)
                    |                                   ----+----------------
                 10 |      DOWN:   (+)   Y                  |
                    |                                    Y  |    UP    DOWN
                 11 |      LEFT:   (-)   X                  |
                    |                                    X  |   LEFT   RIGHT
                 12 |      RIGHT:  (+)   X                  |
                    |
                    |

                    Y


So borrowing from here, let's imagine directions to look something like this,
what will convert

[4, 7]          to           [3, 7]

if it is of the type UP

```py
# You give it the position, and decrement it according to the Y rules
def UP(position): return get_next_position(position, DECR, **Y)
def DOWN(position): return get_next_position(position, INCR, **Y)

def LEFT(position): return get_next_position(position, DECR, **X)
def RIGHT(position): return get_next_position(position, INCR, **X)

```


I know what increassing or decreasing mean

```py
INCR = operator.add
DECR = operator.sub
```

I also know the Y rules

```py
Y = {'coord_index': 0, 'step_size': Y_STEP_SIZE}
X = {'coord_index': 1, 'step_size': X_STEP_SIZE}
```


Now I'll make a get_next_position, that gives a new position very like the old one
_except_ it has it's Y or X coordinate added or subtracted

```py
def get_next_position(position, operator, coord_index, step_size):
    new_position = position[:]
    i, step, op = coord_index, step_size, operator
    new_position[i] = op(position[i], step)

    return new_position

```


Wooh! Now Pacman can finally know what direction is! and move!
Just by disappearing, updating its position with the direction and appear again !

```py

def move(self, direction):
        self.disappear()
        self.position = direction(self.position)
        self.appear()
```

I WANNA SEE THAT IN ACTION

keypad: arrow key presses register as defined constants, eg  KEY_UP

```py
def start(self):
    self.map_box.keypad(1)
    self.map_box.timeout(100)

    while True:
        key = self.map_box.getch()

        if key == curses.KEY_UP:
            self.pacman.move(UP)

        if key == curses.KEY_DOWN:
            self.pacman.move(DOWN)

        if key == curses.KEY_LEFT:
            self.pacman.move(LEFT)

        if key == curses.KEY_RIGHT:
            self.pacman.move(RIGHT)


    self.start()


```




But of course he doesn't look like he's moving right, according to where he faces

The culprit is right here, this fixed char.
Can we do something better?

-----------------------


Now we could do this, a char for every direction, but why settle for this when you can,

ANIMATE!

is just drawing on one picture on instant and drawing a slightly different picture in the next instant

And it's quite easy to make

Let's say we have a circular list like so, loops over and repeats, that always gives the next character.

Well, you have that right here.

```py
class Progression():
    def __init__(self, progression_cycle):
        self.cycle = progression_cycle
        self.index = 0

    @property
    def char(self):
        # automatically update everytime you get a character
        self.update()
        return self.cycle[self.index]

    def update(self):
        self.update_forward()

    def update_forward(self):
        self.index += 1
        if self.index >= len(self.cycle):
            self.index = 0
```

If I run it, giving it the cycle, ['Do', 'Re', 'Mi', 'Fa', 'Sol'], it will keep giving me the next one indefinitly

A minor detail, you can also incorporate reverse, but we don't need it; pacman always move forward.


Let me jot down the frames I discussed for all the directions,


```py

UP_PROG = ['v', 'V', '|', '|', 'V', 'v']
DOWN_PROG = ['^']
LEFT_PROG = ['}', ')', '>', '-', '-', '>', ')', '}']
RIGHT_PROG = ['{', '(', '<', '-', '-', '<', '(', '{']

```

So I'll make something usable for pacman,
_a character progression_,
which defines (initializes) _four_ progressions for each of the directions

and gets the next char for a given direction by asking the progression to update
(remember, when we fetch the char of a progression, it automagically updates)

```py
class CharacterProgression():
    def __init__(self, progressions):
        self.progressions = {
            'UP': Progression(progressions[0]),
            'DOWN': Progression(progressions[1]),
            'LEFT': Progression(progressions[2]),
            'RIGHT': Progression(progressions[3])
        }

    def get_char(self, direction):
        return self.progressions.get(direction).char # self updating!
```

Now pacman is good to go to use this:

```py

    self.char = '{'
    self.progression = CharacterProgression([
        UP_PROG, DOWN_PROG, LEFT_PROG, RIGHT_PROG
    ])

    # ...

    self.char = self.progression.get_char(direction.__name__)

```


And let's see that ... WOOOHOOOOO! AWESOME


-----------------------------

Make him aware of surroundings

Dividing control over the game and the character



Now we were passing an entire map to him

But that may not be what you're looking for, especially if your map is pretty big

what I'll instead do is just pass him his vicinity, and update it everytime he moves

That means, this little bunch of points, we saw earlier:



            #############
            . . . . . { #
                        #
                        #



                   # [3, 7]


        . [4, 6]    { [4, 7]    # [4, 8]


                    [5, 7]



How do I pass it? This seems good enough

```py
vicinity = {
    'UP': {
        'position': [3, 7],
        'map_block': '#'
    }
}
```


So here's what the method for that will look like:

```py
    def get_vicinity(self, position):
        # knows what the map is
        vicinity = {}
        for direction in [UP, DOWN, LEFT, RIGHT]:
            dir_name = direction.__name__
            new_position = direction(position)
            vicinity[dir_name] = {
                'position': new_position,
                'map_block': chr(self.map_box.inch(*new_position))
            }
        return vicinity
```


Update it

```py
        vicinity = self.get_vicinity(position)

        self.pacman = Pacman(self.map_box, vicinity, position)

        # ...

        self.update_pacmans_vicinity()


    def update_pacmans_vicinity(self):
        self.pacman.vicinity = self.get_vicinity(self.pacman.position)


    # ...


    def __init__(self, map_box, vicinity, position):
        self.map_box = map_box
        self.vicinity = vicinity



```


Now I'll actually have to forgo the concept of movement,


We're precalculating all posible positions here


that means, movement is simply getting the position via the vicinity key


```py
    # self.position = direction(self.position)
    self.position = self.vicinity[direction.__name__]['position']
```

And it still works.

-------

Now we get to reacting to those surroundings

```py

WALL = '#'

# ...

    def move(self, direction):
        ahead = self.vicinity[direction.__name__]
        whats_ahead = ahead['map_block']

        if whats_ahead == WALL:
            return
```

Now I have to take care of the food


First off all, you guess it, declare what's food
I'm gonna use an interpunct not a full stop, because it is at the exact center of a pixel

```py

FOOD = '·'  # NOT '.'

```


Let me tell it to eat if something foodlike comes along

```py

        self.ate_food = 0

        # ...

            self.get_ready_to_eat()

            self.position = ahead['position']
            self.char = self.progression.get_char(direction.__name__)

            if whats_ahead == FOOD_PELLET:
                self.eat()

            self.appear()

        def get_ready_to_eat(self):
            self.ate_food = False

        def eat(self):
            self.ate_food = True

```


I'll check if he ate food and increase the score

```py

FOOD_PELLET_SCORE = 10

# ...

        self.score = 0

    # ...

        self.map_box.addstr(position[0]+4, position[1]-10, '. . . . . . . . . . . . . . .')

    # ...

            if self.pacman.ate_food:
                self.score += FOOD_PELLET_SCORE
                self.pacman.ate_food = 0

            self.refresh_score()

            self.update_pacmans_vicinity()


    def refresh_score(self):
        self.map_box.addstr(0, 10, '[ Score: {0} ]'.format(self.score))
        self.map_box.refresh()

```


YAY!

