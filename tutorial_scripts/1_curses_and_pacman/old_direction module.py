
import operator

X_STEP_SIZE = 2
Y_STEP_SIZE = 1

class Direction(object):
    def get_position(self, position):
        new_position = position[:]
        i, step, op = self.coord_index, self.step_size, self.operator
        new_position[i] = op(position[i], step)
        return new_position


class Y(Direction):
    def __init__(self):
        super(Y, self).__init__()
        self.coord_index = 0
        self.step_size = Y_STEP_SIZE

class X(Direction):
    def __init__(self):
        super(X, self).__init__()
        self.coord_index = 1
        self.step_size = X_STEP_SIZE


class Increasing(Direction):
    def __init__(self):
        self.operator = operator.add

class Decreasing(Direction):
    def __init__(self):
        self.operator = operator.sub


class Up(Y, Decreasing): pass
class Down(Y, Increasing): pass
class Left(X, Decreasing): pass
class Right(X, Increasing): pass



"""
So borrowing from here, let's imagine directions to look something like this,

```py
class Up(Y, Decreasing): pass

class Down(Y, Increasing): pass

class Left(X, Decreasing): pass

class Right(X, Increasing): pass
```

I know what being Y means

```py

class Y(Direction):
    def __init__():                                      #[4, 7]
        self.coord_index = 0


class X(Direction):
    def __init__():
        self.coord_index = 1
```


I also know what increassing or decreasing mean

```py
import operator

class Increasing(Direction):
    def __init__():
        # def add(a,b): return a + b;

        self.operator = operator.add

class Decreasing(Direction):
    def __init__():
        # def add(a,b): return a + b;

        self.operator = operator.sub
```

[!!!!] Now in addition I'll need to call the init method of direction by using super in the child instance [!!?????]

```py
class Y(Direction):
    def __init__():                                      #[4, 7]
        super(Y, self).__init__()
        self.coord_index = 0
```


Now I am ready to define what Direction is:
what will convert

[4, 7]          to           [4, 8]

if it is of the type RIGHT

I'll give it a get_next_position, that gives a new position very like the old one
_except_ it has it's Y or X coordinate added or subtracted

```py
class Direction(object):
    def get_next_position(self, position):
        new_position = position[:]
        i, op = self.coord_index, self.operator
        new_position[i] = op(position[i], 1)

```
"""
