'''
BOINC OS Helper monitoring tools screen.
Allows the user to access tools to monitor system performance and generate system reports.
Authors:
  - Delta
'''

import curses

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN

### START CODE ###
def monitoring():
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
        screen.addstr(1, 1, 'Monitoring tools:')
        screen.addstr(4, 3, '—>\t HTOP: CPU/Memory usage and processes')
        screen.addstr(6, 3, '—>\t BMON: Network usage')
        screen.addstr(8, 3, '—>\t Generate session report')
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
                return 3 # Return case for htop
            elif (cursor[0] == 6):
                return 4 # Return case for bmon
            elif (cursor[0] == 8):
                pass # Placeholder for system session reporter
