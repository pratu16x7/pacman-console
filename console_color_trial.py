import curses

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1 + 300, i, i)

    try:
        for i in range(0, 555):
            stdscr.addstr(str(i), curses.color_pair(i))
            stdscr.addstr(' ', curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass

    stdscr.getch()

curses.wrapper(main)
