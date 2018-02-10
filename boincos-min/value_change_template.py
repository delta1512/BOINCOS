'''
BOINC OS Helper screen template for data changing.
A template for a basic value display and change option screen for boinc.py,
hostname.py, language.py and keyboard.py.
Authors:
  - Delta
'''

import curses

def template(val_name, value, option_msg):
    screen = curses.initscr()
    while selection != ord('q'):
        screen.keypad(1)
        screen.clear()
        screen.border(0)
        screen.addstr(1, 1, 'Current {0}: {1}'.format(val_name, value))
        screen.addstr(4, 3, '->\t ' + option_msg)
        screen.refresh()
        selection = screen.getch(4, 3)
        if selection == ord(' '):
            curses.endwin()
            return True
    curses.endwin()
    return False
