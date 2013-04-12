#!/usr/bin/python

"""
Python source code - Reads a file containing heavily filtered 'who' data from
TorilMUD, breaks it down into dates, names, and accounts based on Kegor's old
character database
"""

import sys
import psycopg2
import re
from datetime import datetime, timedelta
from subprocess import Popen, PIPE

timestart = datetime.now()
conn = psycopg2.connect(database='torildb', user='kalkinine')

def db(query, params):
    try:
        cur = conn.cursor()
        cur.execute(query, (params))
        if query.startswith("SELECT"):
            return cur.fetchall()
        else:
            conn.commit()
    except psycopg2.DatabaseError, e:
        if not query.startswith("SELECT"):
            if conn:
                conn.rollback()
        print 'Error %s' % e
        sys.exit(1)

def parse_who():
    cmd = 'cat'
    file = 'who.txt'
    ppl = Popen([cmd, file], stdout=PIPE, stderr=PIPE).communicate()
    if ppl[1] != '':
        print 'Error: '+ppl[1]
    else:
        whod = {}
        lines = ppl[0].splitlines()
        for line in lines: # 2013-04-10,27,War,Topellel,Halfling 
            who = line.split(',')
            if len(who) != 5:
                print 'Invalid entry: '+line
            else:
                date = datetime.strptime(who[0], "%Y-%m-%d")
                lvl = int(who[1])
                clas = who[2]
                name = who[3]
                race = who[4]
                # save only the most recent for any particular char
                if whod[name] < date:
                    whod[name] = date



def parse_accounts():
    cmd = 'cat'
    file = 'accounts.txt'
    ppl = Popen([cmd, file], stdout=PIPE, stderr=PIPE).communicate()
    if ppl[1] != '':
        print 'Error: '+ppl[1]
    else:
        acctdb = []
        lines = ppl[0].splitlines()
        for line in lines: # 2013-04-09,1,Bard,Katumi,Half-Elf,Helper
            who = line.split(',')
            if len(who) != 6:
                print 'Invalid entry: '+line
            else:
                date = datetime.strptime(who[0], "%Y-%m-%d")
                lvl = int(who[1])
                clas = who[2]
                name = who[3]
                race = who[4]
                acct = who[5]
                # save only the most recent for any particular char
                acctdb.append([date, lvl, clas, name, race, acct])

parse_accounts()
parse_who()

if conn:
    conn.close()

timediff = datetime.now() - timestart
print 'The script took '+str(timediff)
