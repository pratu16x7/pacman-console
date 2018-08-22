class GameBox:
    def __init__(self, screen, y, x, height, width):
        self.subwin = screen.subwin(
            height,
            width,
            y,
            x
        )
        pass

