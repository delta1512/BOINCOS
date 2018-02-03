#!/usr/bin/python2

'''
BOINC OS reporter script to collect system data and report it to the user.
--dump simply collects data and dumps it into a file in /tmp/ for monitoring.py
Authors:
  - Delta
'''

#from base64 import b64encode
from xml.dom import minidom
from sys import argv, exit
import subprocess as sp
#from os import urandom
from glob import glob
import pickle
#import string
import time

### DEFINITIONS ###
KB = 1000
MB = 1000**2
GB = 1000**3
TB = 1000**4
PB = 1000**5

### FUNCTIONS ###
def write_polled_data(boinc_perct):
    with open('/tmp/boinc_percent.dat', 'w') as data_file:
        data_file.write(str(round(boinc_perct, 1)) + '%')

def size_conv(val):
    if 0 < val < KB:
        return str(val) + ' B'
    elif KB <= val < MB:
        return str(round(val / KB, 1)) + ' KB'
    elif MB <= val < GB:
        return str(round(val / MB, 1)) + ' MB'
    elif GB <= val < TB:
        return str(round(val / GB, 1)) + ' GB'
    elif TB <= val < PB:
        return str(round(val / TB, 1)) + ' TB'

def fetch_data():
    avg_cpu = ''
    net_total_up, net_total_down = '', ''
    disk_perct_used, disk_free = '', ''
    temperature = 'Unable to fetch temperature, consult user documentation'
    net_connect = 'Not Connected'
    task_count = 0
    users, teams = [], []
    final_dictionary = {}

    avg_cpu = str(round(float(sp.check_output("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'", shell=True)), 1)) + '%'

    with open('/proc/net/dev', 'r') as net_dev:
        for line in net_dev.readlines():
            line_arr = line.split()
            if line_arr[0].startswith('e') or line_arr[0].startswith('w'):
                net_total_up = size_conv(int(line_arr[9]))
                net_total_down = size_conv(int(line_arr[1]))

    raw_disk_data = sp.check_output('df -h /', shell=True).split()[10:12]
    disk_free = raw_disk_data[0]
    disk_perct_used = raw_disk_data[1]

    tmp = sp.check_output('sensors | grep Core', shell=True).split()
    if len(tmp) > 1:
        temperature = ''
        brack_open = False
        for chars in tmp:
            if '(' in chars:
                brack_open = True
            if not brack_open:
                temperature += chars + ' '
            if ')' in chars:
                brack_open = False
                temperature += '\n'

    exit_code = sp.call('ping -c 1 archlinux.org', shell=True)
    if exit_code == 0:
        net_connect = 'Connected'

    slot_dirs = glob('/var/lib/boinc/slots/?')
    for slot in slot_dirs:
        if len(glob(slot + '/*')) > 0:
            task_count += 1
            boinc_xml = minidom.parse(slot + '/init_data.xml')
            slot_user = boinc_xml.getElementsByTagName('user_name').item(0).childNodes[0].data
            slot_team = boinc_xml.getElementsByTagName('team_name').item(0).childNodes[0].data
            if not slot_user in users:
                users.append(slot_user)
            if not slot_team in teams:
                teams.append(slot_team)

    with open('/tmp/boinc_percent.dat', 'r') as data_file:
        final_dictionary['boinc_percent'] = data_file.read()
    final_dictionary['avg_cpu'] = avg_cpu
    final_dictionary['net_total_up'] = net_total_up
    final_dictionary['net_total_down'] = net_total_down
    final_dictionary['disk_perct_used'] = disk_perct_used
    final_dictionary['disk_free'] = disk_free
    final_dictionary['temperature'] = temperature
    final_dictionary['net_connect'] = net_connect
    final_dictionary['task_count'] = task_count
    final_dictionary['users'] = users
    final_dictionary['teams'] = teams
    pickle.dump(final_dictionary, open('/tmp/report.pkl', 'wb'))


### START CODE ###
if len(argv) > 1: # If cmd arguments found, set them if correct
    for i, arg in enumerate(argv):
        if arg == '-p':
            try:
                POLL_RATE = int(argv[i+1])
            except:
                print 'Invalid polling rate provided.'
                exit(1)
        elif arg == '--dump': # Fetch all data and write to file
            fetch_data()
            exit(0)
else: # Set defaults
    POLL_RATE = 3

newpass = False
with open('/var/lib/boinc/gui_rpc_auth.cfg', 'r') as RPC_pass_file:
    if RPC_pass_file.read().replace('\n', '') == 'boincos':
        newpass = True
if newpass:
    with open('/var/lib/boinc/gui_rpc_auth.cfg', 'w') as RPC_pass_file:
        #RPC_pass_file.write(b64encode(urandom(60)).decode('utf-8').translate(str.maketrans(string.punctuation, 'a'*32))[:8])
        RPC_pass_file.write(sp.check_output('head -n 3 /dev/urandom | sha256sum', shell=True).decode()[:8])

sys_start_time = round(time.time())
boinc_time = 0

while True:
    time.sleep(POLL_RATE)
    boinc_search_exit_code = sp.call('ps -e | grep boinc_client', shell=True)
    if boinc_search_exit_code == 0:
        boinc_time += POLL_RATE
    write_polled_data((boinc_time / (round(time.time()) - sys_start_time))*100)
