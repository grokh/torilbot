#!/usr/bin/python

"""
Python source code - This is a program thingy to do things and stuff
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import psycopg2
import string
import datetime

def db(query, params):
	conn = None
	try:
		conn = psycopg2.connect(database='torildb', user='kalkinine')
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
	finally:
		if conn:
			conn.close()

acct = ''
char = sys.argv[1] # Character name
clas = sys.argv[2].strip() # Class of character
level = sys.argv[3] # Level of character
race = sys.argv[4] # Race of character
if len(sys.argv) > 5:
	acct = sys.argv[5]
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")

# check if it's a global 'who' or a direct 'who <char>'
if acct == '': # it's a global 'who'
	# check if character exists in DB
	query = "SELECT account_name, char_name FROM chars\
	WHERE LOWER(char_name) = LOWER(%s)"
	params = (char,)
	rows = db(query, params)
	if len(rows) == 0: # if not, 'who <char>'
		print 'who '+char
	else: # update level and last_seen
		acct = rows[0][0]
		query = "UPDATE chars SET char_level=%s, last_seen=%s WHERE \
		account_name = %s AND char_name = %s"
		params = (level, date, acct, char)
		db(query, params)
else: # it's a direct 'who <char>'
	# check if character exists in DB
	query = "SELECT char_name FROM chars WHERE LOWER(char_name) = LOWER(%s)"
	params = (char,)
	rows = db(query, params)
	if len(rows) == 0: # if no char, check if account exists in DB, create char
		query = "SELECT account_name FROM accounts WHERE \
		LOWER(account_name) = LOWER(%s)"
		params = (acct,)
		rows = db(query, params)
		if len(rows) == 0: # if no acct, create acccount
			query = "INSERT INTO accounts (account_name) VALUES(%s)"
			params = (acct,)
			db(query, params)
		# create character
		query = "INSERT INTO chars VALUES(%s, %s, %s, %s, %s, %s, true)"
		params = (acct, char, clas, race, level, date)
		db(query, params)
