'''
BOINC OS Helper language/locale handling script.
Allows the user to see current locale and change it if neccessary.
Authors:
  - Delta
'''

from value_change_template import template
import curses

### DEFINITIONS ###
LANG_FILE = '/etc/locale.conf'

def lang_change():
    selection = True
    # Enter the main loop
    while selection:
        with open(LANG_FILE, 'r') as lang_conf:
            lang = lang_conf.read().replace('\n', '').replace('LANG=', '')
        selection = template('locale', lang, 'Change locale')
        if selection:
            pass # Code for changing locale goes here
