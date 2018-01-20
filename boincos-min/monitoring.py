'''
BOINC OS Helper monitoring tools screen.
Allows the user to access tools to monitor system performance and generate system reports.
Authors:
  - Delta
'''

from sys import exit
import subprocess
import curses
import pickle

### DEFINITIONS ###
UP = curses.KEY_UP
DN = curses.KEY_DOWN

### START CODE ###
def monitoring_tools():
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
        screen.addstr(4, 3, '->\t HTOP: CPU/Memory usage and processes')
        screen.addstr(6, 3, '->\t BMON: Network usage')
        screen.addstr(8, 3, '->\t Generate session report')
        screen.refresh()
        # Fetch and handle user selection
        selection = screen.getch(cursor[0], cursor[1])
        if (selection == UP) and (4 < cursor[0] <= 8):
            cursor[0] -= 2
        elif (selection == DN) and (4 <= cursor[0] < 8):
            cursor[0] += 2
        elif (selection == ord(' ')):
            if (cursor[0] == 4):
                curses.endwin()
                return 3 # Return case for htop
            elif (cursor[0] == 6):
                curses.endwin()
                return 4 # Return case for bmon
            elif (cursor[0] == 8):
                screen.clear()
                try:
                    exit_code = subprocess.call('exec /opt/helper/reporterd.py --dump', shell=True)
                    if exit_code != 0:
                        raise Exception('Failed to dump stats')
                    data_file = pickle.load(open('/tmp/report.pkl', 'rb'))
                except:
                    return 99
                screen.addstr(0, 0, 'AVG CPU Usage: ' + data_file['avg_cpu'])
                screen.addstr(2, 0, 'Net Usage: UP: {0} DOWN: {1}'.format(
                            data_file['net_total_up'], data_file['net_total_down']))
                screen.addstr(4, 0, '% of Disk Used: ' + data_file['disk_perct_used'])
                screen.addstr(5, 0, 'Space free: ' + data_file['disk_free'])
                screen.addstr(7, 0, data_file['temperature'])
                screen.addstr(0, 40, '% BOINC uptime: ' + data_file['boinc_percent'])
                screen.addstr(2, 40, 'Network: ' + data_file['net_connect'])
                screen.addstr(4, 40, 'Active BOINC tasks: ' + str(data_file['task_count']))
                screen.addstr(4, 40, 'Users and teams:')
                for uoffset, user in enumerate(data_file['users']):
                    screen.addstr(6, 40+uoffset, user)
                uoffset += 1
                for toffset, team in enumerate(data_file['teams']):
                    screen.addstr(6, 40+uoffset+toffset, team)
