#!/usr/bin/python

"""
Python source code - Developed by kristi.michaels@gmail.com to
run tests against parseTell.py, parseWho.py, and parseTime.py,
which are all components of the TorilMUD bot Katumi
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import string
from subprocess import Popen, PIPE
import smtplib

def runcmd(cmd, args):
	for arg in args:
		print Popen(cmd+arg, stdout=PIPE, shell=True).stdout.read().rstrip()

cmd = './parseTell.py '
args = ('"Rynshana" "who rynshana"', '"Rynshana" "WHO RYNSHANA"', \
'"Rynshana" "who blahblah"', '"Rynshana" "clist rynshana"', \
'"Rynshana" "clist blahblah"', '"Rynshana" "char rynshana"', \
'"Rynshana" "char blahblah"', '"Rynshana" "find rynshana"', \
'"Rynshana" "find blahblah"', '"Rynshana" "stat keprum\'s"', \
'"Rynshana" "astat keprum\'s"', '"Rynshana" "hidden?"', \
'"Someone" "hidden?"', '"Rynshana" "?"', '"Rynshana" "blahblah"', \
'"Rynshana" "lr"')
runcmd(cmd, args)

