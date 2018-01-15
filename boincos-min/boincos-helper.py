'''
BOINC OS Helper main script.
Launches on login unless set otherwise and directs the user to other functionality.
Authors:
  - Delta
'''

from boinc import boinc_help
from monitoring import  monitoring_tools
from firewall import fw_config
from netcfg import net_config
from sys import exit
import curses

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN
LT = curses.KEY_LEFT
RT = curses.KEY_RIGHT
# Fast function definitions to check user selection
BOINC_SEL = lambda cursor: cursor == [4, 3]
MONITOR_SEL = lambda cursor: cursor == [6, 3]
FIREW_SEL = lambda cursor: cursor == [8, 3]
NET_SEL = lambda cursor: cursor == [10, 3]
YES_SEL = lambda cursor: cursor == [9, 43]
NO_SEL = lambda cursor: cursor == [9, 56]
OPT_DIR = '/home/boincuser/.helper.opt'
selection = None
cursor = [4, 3] # y, x
radio_stateY = 'X'
radio_stateN = 'o'
start_at_login = False

### FUNCTIONS ###
def write_opts(user_sel):
    with open(OPT_DIR, 'w') as options:
        options.write(user_sel)

### START CODE ###
# Check the options file to see if BOINC OS Helper should be run at login
try:
    with open(OPT_DIR, 'r') as options:
        if options.read() == 'no':
            start_at_login = False
        else:
            start_at_login = True
except:
    start_at_login = True

screen = curses.initscr() # Initialise curses
# Enter the main loop
while selection != ord('q'):
    screen.keypad(1)
    screen.clear()
    screen.border(0)
    # Add all components to display
    # Navigation labels and buttons
    screen.addstr(1, 1, 'Welcome to BOINC OS Helper. Use arrow keys and spacebar to navigate, press q to quit.')
    screen.addstr(4, 3, '->\t BOINC')
    screen.addstr(6, 3, '->\t Monitoring tools')
    screen.addstr(8, 3, '->\t Firewall configuration')
    screen.addstr(10, 3, '->\t Network configuration')
    # Radio button labels
    screen.addstr(4, 40, 'Start BOINC OS Helper')
    screen.addstr(5, 45, 'at login:')
    screen.addstr(7, 43, 'Y' + (' ' * 12) + 'N')
    # Radio Buttons
    screen.addstr(8, 42, '.-.' + (' ' * 10) + '.-.')
    # Determine the states of the options
    if start_at_login:
        radio_stateY = 'X'
        radio_stateN = 'o'
    else:
        radio_stateY = 'o'
        radio_stateN = 'X'
    screen.addstr(9, 42, '|' + radio_stateY + '|' + (' ' * 10) + '|' + radio_stateN + '|')
    screen.addstr(10, 42, '\'-\'' + (' ' * 10) + '\'-\'')
    screen.refresh() # Display components
    # Handle user selection/navigation
    selection = screen.getch(cursor[0], cursor[1])
    if (selection == UP) and (4 < cursor[0] <= 10) and (cursor[1] == 3):
        cursor[0] -= 2
    elif (selection == DN) and (4 <= cursor[0] < 10) and (cursor[1] == 3):
        cursor[0] += 2
    elif (selection == LT):
        if (cursor[1] == 56): # Move from 'no' to 'yes'
            cursor[1] = 43
        elif (cursor[1] == 43): # Move from radio buttons to navigation
            cursor = [4, 3]
    elif (selection == RT):
        if (cursor[1] == 3): # Move from navigation to radio buttons
            cursor = [9, 43]
        elif (cursor[1] == 43): # Move from 'yes' to 'no'
            cursor[1] = 56
    elif (selection == ord(' ')): # Handle selection
        if BOINC_SEL(cursor):
            curses.endwin()
            exit(boinc_help())
        elif MONITOR_SEL(cursor):
            curses.endwin()
            exit(monitoring_tools())
        elif FIREW_SEL(cursor):
            curses.endwin()
            fw_config()
        elif NET_SEL(cursor):
            curses.endwin()
            exit(net_config())
        elif YES_SEL(cursor):
            start_at_login = True
            radio_stateY = 'X'
            radio_stateN = 'o'
            write_opts('yes')
        elif NO_SEL(cursor):
            start_at_login = False
            radio_stateY = 'o'
            radio_stateN = 'X'
            write_opts('no')

curses.endwin() # Close curses gracefully
exit(0) # Return a quit signal to the bash script
