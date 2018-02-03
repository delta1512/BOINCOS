#!/usr/bin/python

from base64 import b64encode
from os import urandom
import string

newpass = False
with open('/var/lib/boinc/gui_rpc_auth.cfg', 'r') as RPC_pass_file:
    if RPC_pass_file.read().replace('\n', '') == 'boincos':
        newpass = True
if newpass:
    with open('/var/lib/boinc/gui_rpc_auth.cfg', 'w') as RPC_pass_file:
        RPC_pass_file.write(b64encode(urandom(60)).decode('utf-8').translate(dict((ord(char), None) for char in string.punctuation))[:8].encode('ascii', 'ignore'))
