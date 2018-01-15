'''
BOINC OS Helper BOINC interface and information script.
Aids the user in accessing BOINC and boinctui in addition to providing some info.
Authors:
  - Delta
'''

import curses

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN
PASS_DIR = '/var/lib/boinc/gui_rpc_auth.cfg'

### START CODE ###
def boinc_help():
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
        screen.addstr(1, 1, 'BOINC Tools:')
        screen.addstr(4, 3, '->\t BOINC Manager')
        screen.addstr(6, 3, '->\t Restart BOINC')
        screen.addstr(8, 3, '->\t Change RPC password')
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
                return 1 # Return case for starting boinctui
            elif (cursor[0] == 6):
                return 2 # Return case for restarting BOINC
            elif (cursor[0] == 8):
                pass_scrn_sel = None
                cursor = [4, 3]
                screen.clear()
                screen.border(0)
                while pass_scrn_sel != ord('q'):
                    with open(PASS_DIR, 'r') as pass_file:
                        passwd = pass_file.read()
                    screen.addstr(1, 1, 'Current password: ' + passwd)
                    screen.addstr(4, 3, '->\t Change password')
                    screen.refresh()
                    pass_scrn_sel = screen.getch(cursor[0], cursor[1])
                    if pass_scrn_sel == ord(' '):
                        screen.clear()
                        screen.border(0)
                        screen.addstr(1, 1, 'New password:')
                        screen.refresh()
                        newpass = screen.getstr(1, 15)
                        with open(PASS_DIR, 'w') as pass_file:
                            pass_file.write(newpass)
                        screen.clear()
                        screen.border(0)
