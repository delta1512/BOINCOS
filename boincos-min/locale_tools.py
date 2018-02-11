'''
BOINC OS locale configuration functions.
Functions for manipulating the locale settings of the BOINC OS system.
Authors:
  - Jokermc
'''

from os import path
from subprocess import check_call

setting_path = path.join('/etc', 'locale.conf')
locale_file = path.join('/etc', 'locale.gen')

def get_locale_list():
    locale_list = []
    with open(locale_file) as f:
        for locale in f.readlines():
            locale_list.append(locale.replace('#', '', 1).replace('\n', '').split()[0])
    return locale_list

def filter_query(locale_list, term):
    filtered = []
    for locale in locale_list:
        if term in locale:
            filtered.append(locale)
    return filtered

def set_locale(locale):
    with open(locale_file, mode='r+') as localegen, open(setting_path, mode='w') as localeconf:
        raw_locale = localegen.read()
        localegen.seek(0)
        if '#{} '.format(locale) in raw_locale:
            localegen.write(raw_locale.replace('#{} '.format(locale), locale + ' '))
        localeconf.write('LANG=' + locale)
    check_call(['locale-gen'])

if __name__ == '__main__':
    print('This file is not intended for command line usage.')
