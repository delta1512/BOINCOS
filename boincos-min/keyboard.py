'''
BOINC OS Helper keyboard layout handling script.
Allows the user to see current keyboard layout and change it if neccessary.
Authors:
  - Delta
'''

from value_change_template import template
import curses

### DEFINITIONS ###
KEY_CONF = '/etc/vconsole.conf'

def key_change():
    selection = True
    # Enter main loop
    while selection:
        with open(KEY_CONF, 'r') as vconsole:
            key_layout = vconsole.read().replace('\n', '').replace('KEYMAP=', '')
