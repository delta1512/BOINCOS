'''
BOINC OS Helper firewall configuration script.
Provides and interface to modifying the firewall within the system.
Authors:
  - Delta
'''

from os import popen
import curses

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN

### START CODE ###
def fw_config():
    # Initiate screen variables
    selection = None
    cursor = [4, 3]
    screen = curses.initscr()
    # Move into main loop
    while selection != ord('q'):
        screen.keypad(1)
        screen.clear()
        screen.border(0)
        # Add all components to display
        # Navigation labels and buttons
        screen.addstr(1, 1, 'Firewall Configuration:')
        screen.addstr(4, 3, '—>\t Current firewall state')
        screen.addstr(6, 3, '—>\t Add firewall rules')
        screen.addstr(8, 3, '—>\t Revert to defaults')
        screen.refresh()
        # Fetch and handle user selection
        selection = screen.getch(cursor[0], cursor[1])
        if (selection == UP) and (4 < cursor[0] <= 8):
            cursor[0] -= 2
        elif (selection == DN) and (4 <= cursor[0] < 8):
            cursor[0] += 2
        elif (selection == ord(' ')):
            curses.endwin()
            if (cursor[0] == 4):
                pass # Placeholder for checking the current firewall state
            elif (cursor[0] == 6):
                pass # Placeholder for adding firewall rules
            elif (cursor[0] == 8):
                pass # Placeholder for reverting firewall rules to defaults
