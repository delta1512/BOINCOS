'''
BOINC OS Helper networking script.
Aids the user in accessing networking functionality and configuration.
Authors:
  - Delta
'''

import curses

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN

### START CODE ###
def net_config():
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
        screen.addstr(1, 1, 'Network Configuration:')
        screen.addstr(4, 3, '—>\t Ethernet: Reset connection state ')
        screen.addstr(6, 3, '—>\t Wi-Fi: Setup Wi-Fi network')
        screen.refresh()
        # Fetch and handle user selection
        selection = screen.getch(cursor[0], cursor[1])
        if (selection == UP) and (4 < cursor[0] <= 6):
            cursor[0] -= 2
        elif (selection == DN) and (4 <= cursor[0] < 6):
            cursor[0] += 2
        elif (selection == ord(' ')):
            curses.endwin()
            if (cursor[0] == 4):
                return 5 # Return case for ethernet restart
            elif (cursor[0] == 6):
                return 6 # Return case for Wi-Fi configuration
