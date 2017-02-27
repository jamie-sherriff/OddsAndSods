#!/usr/bin/env python
__author__ = "Jamie Sherriff"
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Jamie Sherriff"
__contact__ = "https://github.com/jamie-sherriff"
__status__ = "Prototype"
__date__ = "27-02-2017"
'''
Simple script to connect to a wifi lazy bone mains switch to control it
HostName is in the format ex: 192.168.5.2:4550
'''
import telnetlib
ESCAPE_CODE = chr(29)
SOFTWARE_CODE = chr(90)
RELAY_STATE = chr(91)
RELAY_1_CODE = chr(101)
RELAY_0_CODE = chr(111)
RELAY_CODE = hex(ord('['))
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='specify a hostname with port to run on in the format <hostname|ip>:<port>')
parser.add_argument('--cmd', choices=['ON', 'OFF', 'VERSION', 'STATE'], help='specify cmd to run on the relay')
args = parser.parse_args()
if not args.host:
    raise RuntimeError('need to specify Host, please run with -h')
if not args.cmd:
    raise RuntimeError('need to specify cmd, please run with -h')
split_host = args.host.split(':')
if len(split_host) != 2:
    raise ValueError('split host needs to be a length of 2 only')
host_name = split_host[0]
port = int(split_host[1])
command = args.cmd
print('using port: ' + str(port))
print('using host_name: ' + str(host_name))
print('using command: ' + str(command))


def do_command(tel, cmd):
    if cmd == 'ON':
        tel.write(RELAY_1_CODE.encode('ascii'))
    elif cmd == 'OFF':
        tel.write(RELAY_0_CODE.encode('ascii'))
    elif cmd == 'VERSION':
        tel.write(SOFTWARE_CODE.encode('ascii'))
        print(repr(tel.read_some()))
    elif cmd == 'STATE':
        tel.write(RELAY_STATE.encode('ascii'))
        print(repr(tel.read_some()))


telnet = telnetlib.Telnet(host=host_name, port=port, timeout=10)
start = telnet.read_until(b'*HELLO*')
print(start)
do_command(telnet, command)
telnet.close()
