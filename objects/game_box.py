class GameBox:
    def __init__(self, screen):
        self.screen = screen
        self.init_map_matrix()
        self.init_map_box()
        self.draw_map()


    def init_map_matrix(self):
        self.map_matrix = []
        # with open('../maps/map.txt') as map_file:
        with open('maps/map.txt') as map_file:
            for line in map_file:
                # trim the new_line char
                self.map_matrix.append(list(line)[:-1])

        # # TODO:
        # # Better checks to validate map files, to parse them seamlessly


    def init_map_box(self):
        screen_h, screen_w = self.screen.getmaxyx()

        m = self.map_matrix
        map_h, map_w = len(m), len(m[0])

        offset_y = int((screen_h - map_h)/2)
        offset_x = int((screen_w - map_w)/2)

        self.map_box = self.screen.subwin(
            map_h,
            map_w,
            offset_y,
            offset_x
        )

        self.map_box.keypad(1)
        self.map_box.timeout(100)


    def draw_map(self):
        line_index = 0
        for line in self.map_matrix:
            char_index = 0
            for char in line:
                self.map_box.addch(
                    line_index,
                    char_index,
                    char
                )
                char_index += 1
            line_index += 1

