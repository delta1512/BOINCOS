#!/usr/bin/python

import subprocess as sp

newpass = False
with open('/var/lib/boinc/gui_rpc_auth.cfg', 'r') as RPC_pass_file:
    if RPC_pass_file.read().replace('\n', '') == 'boincos':
        newpass = True
if newpass:
    with open('/var/lib/boinc/gui_rpc_auth.cfg', 'w') as RPC_pass_file:
        RPC_pass_file.write(sp.check_output('head -n 3 /dev/urandom | sha256sum', shell=True).decode()[:8])
