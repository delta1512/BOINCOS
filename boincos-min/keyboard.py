'''
BOINC OS Helper keyboard layout handling script.
Allows the user to see current keyboard layout and change it if neccessary.
Authors:
  - Delta
'''

from value_change_template import template
import subprocess as sp
import curses

### DEFINITIONS ###
KEY_CONF = '/etc/vconsole.conf'
KEYMAPS = sp.check_output('localectl list-keymaps').decode().split()

def key_change():
    selection = True
    # Enter main loop
    while selection:
        with open(KEY_CONF, 'r') as vconsole:
            key_layout = vconsole.read().replace('\n', '').replace('KEYMAP=', '')
        selection = template('keyboard layout', key_layout, 'Change keyboard layout')
        if selection:
            screen.keypad(1)
            screen.clear()
            screen.border(0)
            screen.addstr(1, 1, 'New keymap:')
            screen.refresh()
            keymap = screen.getstr(1, 15)
            if keymap in KEYMAPS:
                sp.call('localectl set-keymap ' + keymap, shell=True)
