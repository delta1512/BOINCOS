'''
BOINC OS Helper hostname handling script.
Allows the user to see current hostname and change it if neccessary.
Authors:
  - Delta
'''

from value_change_template import template
import curses

### DEFINITIONS ###
NAME_FILE = '/etc/hostname'

def host_change():
    selection = True
    # Enter the main loop
    while selection:
        with open(NAME_FILE, 'r') as hostnamef: # Fetch the current hostname
            hname = hostnamef.read().replace('\n', '')
        selection = template('hostname', hname, 'Change hostname')
        if selection:
            pass # Code for changing hostname goes here
