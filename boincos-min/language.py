'''
BOINC OS Helper language/locale handling script.
Allows the user to see current locale and change it if neccessary.
Authors:
  - Delta
'''

from value_change_template import template
from subprocess import check_output
import locale_tools as ltools
from math import floor
import curses

### DEFINITIONS ###
LANG_FILE = '/etc/locale.conf'
rows, columns = [int(i) for i in check_output('stty size', shell=True).decode().split()]
LONG_LOCALE = 18 # 1 + the length of the longest locale name
COL_DELIM = int(floor(columns/LONG_LOCALE))

def lang_change():
    screen = curses.initscr()
    selection = True
    # Enter the main loop
    while selection:
        with open(LANG_FILE, 'r') as lang_conf:
            lang = lang_conf.read().replace('\n', '').replace('LANG=', '')
        selection = template('locale', lang, 'Change locale')
        if selection:
            done = False
            search = ''
            locale_list = ltools.get_locale_list()
            while not done:
                screen.keypad(1)
                screen.clear()
                screen.border(0)
                screen.addstr(1, 1, 'Type desired locale and press enter when done.')
                screen.addstr(2, 1, 'New locale: ' + search)
                counter = 0
                for row in range(rows-5):
                    for col in range(COL_DELIM):
                        if counter < len(locale_list):
                            screen.addstr(row+4, col*LONG_LOCALE, locale_list[counter])
                            counter += 1
                screen.refresh()
                raw_char = screen.getch(2, 13+len(search))
                if raw_char in [127, 8]:
                    search = search[:len(search)-1]
                elif raw_char == 10:
                    done = True
                else:
                    search += chr(raw_char)
                    locale_list = ltools.filter_query(locale_list, search)

            if search in locale_list:
                ltools.set_locale(locale_list[locale_list.index(search)])
            elif len(locale_list) == 1:
                ltools.set_locale(locale_list[0])
