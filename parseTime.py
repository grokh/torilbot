#!/usr/bin/python

"""
Python source code - Call this script to update boot times, uptimes, and boot IDs
for load reporting and such
"""

import sys
import psycopg2
import notify
from datetime import datetime, timedelta

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

# Accepts time since boot in format H:MM:SS
curup = sys.argv[1]
curboot = curup.split(':')
curtime = timedelta(hours=int(curboot[0]), minutes=int(curboot[1]),
seconds=int(curboot[2]))

# query DB for details of most recent boot
query = ("SELECT boot_id, uptime FROM boots WHERE boot_time = "
        "(SELECT MAX(boot_time) FROM boots)")
params = ''
rows = db(query, params)
oldid = rows[0][0]
oldup = rows[0][1]
oldboot = oldup.split(':')
oldtime = timedelta(hours=int(oldboot[0]), minutes=int(oldboot[1]),
seconds=int(oldboot[2]))

# check if current boot time is less than last boot time
if curtime < oldtime: # if it is, create new boot_id
    query = ("INSERT INTO boots (boot_time, uptime) "
            "VALUES(CURRENT_TIMESTAMP - interval %s, %s)")
    params = (curup, curup)
    db(query, params)
    # send email to people who want to know about new boots
    notify.boot_notify()
else: # if not, update uptime
    query = "UPDATE boots SET uptime = %s WHERE boot_id = %s"
    params = (curup, oldid)
    db(query, params)

if conn:
    conn.close()
