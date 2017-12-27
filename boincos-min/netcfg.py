'''
BOINC OS Helper networking script.
Aids the user in accessing networking functionality and configuration.
Authors:
  - Delta
'''

import curses
from os import popen

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN

def net_config():
    selection = None
    cursor = [4, 3]
    screen = curses.initscr()
    while selection != ord('q'):
        screen.keypad(1)
        screen.clear()
        screen.border(0)
        screen.addstr(1, 1, 'Network Configuration:')
        screen.addstr(4, 3, '—>\t Ethernet: Reset connection state ')
        screen.addstr(6, 3, '—>\t Wi-Fi: Setup Wi-Fi network')
        screen.refresh()
        selection = screen.getch(cursor[0], cursor[1])
        if (selection == UP) and (4 < cursor[0] <= 6):
            cursor[0] -= 2
        elif (selection == DN) and (4 <= cursor[0] < 6):
            cursor[0] += 2
        elif (selection == ord(' ')):
            if (cursor[0] == 4):
                popen('sudo netctl restart eth')
            elif (cursor[0] == 6):
                curses.endwin()
                popen('sudo wifi-menu')
