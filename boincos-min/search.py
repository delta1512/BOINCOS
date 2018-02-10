from os import path
from subprocess import check_call

setting_path = path.join('etc', 'locale.conf')
locale_file = path.join('etc', 'locale.gen')

def get_locale_list():
    locale_list = []
    with open(locale_file) as f:
        for locale in f.readlines():
            locale_list.append(locale.replace('#', '', 1))
    return locale_list

def filter_query(locale_list, term):
    filtered = []
    for locale in locale_list:
        if term in locale:
            filtered.append(locale)
    return filtered

def set_locale(locale):
    with open(locale_file) as f:
        raw_locale = f.read()
    if '#' + locale in raw_locale:
        with open(locale_file, mode='w') as f:
            f.write(raw_locale.replace('#' + locale, locale))
    with open(setting_path, mode='w') as f:
        f.write('LANG=' + locale)
    check_call(['locale-gen'])

if __name__ == '__main__':
    print('This file is not intended for command line usage.')
