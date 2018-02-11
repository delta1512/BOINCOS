'''
BOINC OS Helper hostname handling script.
Allows the user to see current hostname and change it if necessary.
Authors:
  - Delta
'''

from value_change_template import template
from subprocess import call
import string as s
import curses

### DEFINITIONS ###
NAME_FILE = '/etc/hostname'
BANNED_CHARS = [sym for sym in s.punctuation if not sym in ['-', '_']]

def host_change():
    selection = True
    # Enter the main loop
    while selection:
        with open(NAME_FILE, 'r') as hostnamef: # Fetch the current hostname
            hname = hostnamef.read().replace('\n', '')
        selection = template('hostname', hname, 'Change hostname')
        if selection:
            screen.keypad(1)
            screen.clear()
            screen.border(0)
            screen.addstr(1, 1, 'New hostname:')
            screen.refresh()
            newhname = ''.join(char for char in screen.getstr(1, 15) if not char in BANNED_CHARS)
            call('sudo hostnamectl set-hostname ' + newhname, shell=True)
