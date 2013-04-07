#!/usr/bin/python

"""
Python source code - This is a program thingy to do things and stuff
"""

# kegor's functions: http://z15.invisionfree.com/Triterium_BBS/index.php?showforum=161
# python tutorial: http://docs.python.org/2/tutorial/index.html
# database walkthrough: http://zetcode.com/db/postgresqlpythontutorial/
# can allow about 310 characters per tell? character names included??

import sys
import psycopg2
import string
from datetime import datetime, timedelta, date

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

def notfound(type):
    return '404 '+type+' not found: '+oper

def find_item(type):
    # query item table for exact item name
    query = "SELECT "+type+" FROM items\
    WHERE item_name = %s LIMIT 1"
    params = (oper,)
    rows = db(query, params)
    if len(rows) == 1:
        return rows[0][0]
    # if no exact match on item name, check LIKE
    else:
        #print 'Not an exact match.'
        item = '%%'+oper+'%%'
        query = "SELECT "+type+" FROM items WHERE item_name ILIKE %s LIMIT 1"
        params = (item,)
        rows = db(query, params)
        if len(rows) == 1:
            return rows[0][0]
        else:
            #print 'Not a like match.'
            # if no match on LIKE, check with %'s in place of spaces
            item = ' '+oper+' '
            item = item.replace(' ', '%')
            query = "SELECT "+type+" FROM items WHERE item_name ILIKE %s LIMIT 1"
            params = (item,)
            rows = db(query, params)
            if len(rows) == 1:
                return rows[0][0]
            else:
                #print 'Not an in order match.'
                # if no match on %'s, check general strings in any order
                query = "SELECT ts_rank_cd(tsv, plainto_tsquery(%s)) rank, "+type+" \
                FROM items ORDER BY rank DESC LIMIT 5;"
                params = (oper,)
                rows = db(query, params)
                if len(rows) > 0:
                    if rows[0][0] >= 0.1:
                        return rows[0][1]
                    else:
                        return notfound('item')
                else:
                    return notfound('item')

def reply(msg):
    print 't '+char+' '+msg

def findcmd(rows):
    tdelta = datetime.now() - rows[0][2]
    online = False
    if tdelta.days == 1:
        delta = str(tdelta.days)+' day'
    elif tdelta.days > 1:
        delta = str(tdelta.days)+' days'
    elif tdelta.seconds > 3600:
        hours, remainder = divmod(tdelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        delta = '%sh%sm' % (hours, minutes)
    elif tdelta.seconds > 60:
        minutes, seconds = divmod(tdelta.seconds, 60)
        delta = '%sm%ss' % (minutes, seconds)
    else:
        online = True
        delta = str(tdelta.seconds)+'s'
    if online:
        reply('@'+rows[0][0]+' is online as '+rows[0][1])
    else:
        reply('@'+rows[0][0]+' last seen '+delta+' ago as '+rows[0][1])

def clistcmd(rows):
    for row in rows:
        reply('['+str(row[0])+' '+row[1]+'] '+row[2]\
        +' ('+row[3]+') (@'+row[4]+') seen '+str(row[5]))

def whocmd(rows):
    clist = '@' + rows[0][0]
    for row in rows:
        clist += ", %s" % (row[1])
    reply(clist)

oper = '' # Operant, such as item or char names
char = sys.argv[1] # Character name of user
tell = sys.argv[2].split(None,1) # whole tell string from user
cmd = tell[0].lower() # Command input from user
if len(tell) > 1: # If there's actually an operant
    oper = tell[1]

site = 'http://www.example.com/' # Website for stuff
info = 'I am a Helper Bot (Beta). Valid commands: ?, help <cmd>, hidden?, \
who <char>, char <char>, clist <char>, find <char>, class <class>, \
delalt <char>, addalt <char>, lr, lr <report>, stat <item>, astat <item>. \
For further information, tell katumi help <cmd>'
syntax = 'Invalid syntax. For valid syntax: tell katumi ?, \
tell katumi help <cmd>'

if cmd == '?':
    reply(info)
elif cmd == 'help':
    if oper == '':
        reply(info)
    elif oper == '?':
        reply("Syntax: tell katumi ? -- "+
                "Katumi provides a full listing of valid commands.")
    elif oper == 'hidden?':
        reply("Syntax: tell katumi hidden? -- "+
                "Katumi sends a tell in reply "+
                "if she can see you. If you receive no reply, you are hidden. "+
                "Katumi has permanent detect invis to ensure that won't cause "+
                "issues.")
    elif oper == 'who':
        reply("Syntax: tell katumi who <acct/char> -- "+
                "Example: tell katumi who rynshana -- "+
                "Katumi provides the account name along with a list of every "+
                "known alt of the named character as a reply. Also works with "+
                "account names.")
    elif oper == 'char':
        reply("Syntax: tell katumi char <char> -- "+
                "Example: tell katumi char rynshana -- "+
                "Katumi provides the account name along with full information "+
                "on the named character as a reply, "+
                "to include level, class, race, and date/time last seen.")
    elif oper == 'find':
        reply("Syntax: tell katumi find <acct/char> -- "+
                "Example: tell katumi find rynshana -- "+
                "Katumi provides the account name along with the last known "+
                "sighting of any of that character's alts. If they have an alt online, "+
                "the time will measure in seconds. Also works with account names.")
    elif oper == 'clist':
        reply("Syntax: tell katumi clist <acct/char> -- "+
                "Example: tell katumi clist rynshana -- "+
                "Katumi provides a full "+
                "listing of every known alt belonging to <char>, including race, "+
                "class, level, and date/time last seen, matching the format of "+
                "the 'char' command. Also works with account names.")
    elif oper == 'class':
        reply("Syntax: tell katumi class <class> -- "+
                "Example: tell katumi class enchanter -- "+
                "Katumi provides a "+
                "list of alts matching the named class for characters who "+
                "are currently online, letting group leaders find useful "+
                "alts from the 'who' list.")
    elif oper == 'delalt':
        reply("Syntax: tell katumi delalt <char> -- "+
                "Example: tell katumi delalt rynshana -- "+
                "Katumi no longer "+
                "provides information on the alt, removing it from 'clist', "+
                "'who', and 'find' commands. Only works for characters "+
                "attached to the same account requesting the removal.")
    elif oper == 'addalt':
        reply("Syntax: tell katumi addalt <char> -- "+
                "Example: tell katumi addalt rynshana -- "+
                "Katumi begins "+
                "providing information on the named alt, who had previously "+
                "been removed with 'delalt', adding the character back to "+
                "'clist', 'who', and 'find' commands. Only works for chars "+
                "attached to the same account.")
    elif oper == 'lr':
        reply("Syntax: tell katumi lr -- "+
                "Katumi provides a list of load "+
                "reports for the current boot. This could be rares or quests "+
                "other players have found or completed. Use the 'lrdel' command "+
                "to remove bad or out of date reports.")
        reply("Syntax: tell katumi lr <report> -- "+
                "Example: tell katumi lr timestop gnome at ako village -- "+
                "Katumi adds <report> "+
                "to the list of load reports for the current boot. If you find "+
                "a rare, global load, or complete a quest or the like, report "+
                "it along with a location so other players will know!")
    elif oper == 'lrdel':
        reply("Syntax: tell katumi lrdel <num> -- "+
                "Example: tell katumi lrdel 3 -- "+
                "Katumi removes the "+
                "numbered item from the load reports, if a quest is completed "+
                "or a rare killed, or a report found to be inaccurate. Please "+
                "do not abuse this command - this service helps everyone.")
    elif oper == 'stat':
        reply("Syntax: tell katumi stat <item> -- "+
                "Example: tell katumi stat isha cloak -- "+
                "Katumi provides stat info for the item named. "+
                "Use 'astat' for full text of acronyms and keywords. "+
                "The name search is fairly forgiving. Please send new stats "+
                "in an mwrite to katumi or email to kristi.michaels@gmail.com")
    elif oper == 'astat':
        reply("Syntax: tell katumi astat <item> -- "+
                "Example tell katumi astat destruction sword -- "+
                "Katumi provides full "+
                "stat information for the item named. Use 'stat' for short "+
                "text. The name search is fairly forgiving, though the stats "+
                "are a little buggy right now since I haven't put much time "+
                "into it.")
    elif oper == 'fstat':
        reply("Syntax: tell katumi fstat <stat> <sym> <num>"+
        "[, <stat2> <sym2> <num2>][, resist <resist>] -- "+
        "Example: tell katumi fstat maxagi > 0, resist fire -- "+
        "Katumi provides up to 10 results which match the parameters.")
        reply("Type attribs as they appear in stats: str, maxstr, svsp,"+
        " sf_illu, fire, unarm, etc. Valid comparisons are >, <, and =."+
        " Resists check for a positive value. Other options will be added later."
        )
elif (cmd == 'hidden' or cmd == 'hidden?' or cmd == 'hidden/') and oper == '':
    if char != 'Someone':
        reply(char+' is NOT hidden')
elif cmd == 'stat':
    reply(find_item('short_stats'))
elif cmd == 'astat':
    reply(find_item('long_stats'))
elif cmd == 'fstat':
    (att, comp, val) = '', '', 0
    opers = oper.split(',')
    query = "SELECT short_stats FROM items"
    params = ()
    for ops in opers:
        fop = ops.split()
        if fop[1] in '=<>' and len(fop) == 3:
            att = fop[0]
            comp = fop[1]
            val = fop[2]
            if 'WHERE' not in query:
                query += " WHERE item_id IN"
            else:
                query += " AND item_id IN"
            query += " (SELECT i.item_id FROM items i, item_attribs a \
            WHERE i.item_id = a.item_id \
            AND attrib_abbr = %s AND attrib_value "+comp+" %s)"
            params += (att, val)
        elif fop[0] == 'resist' and len(fop) == 2:
            res = fop[1]
            if 'WHERE' not in query:
                query += " WHERE item_id IN"
            else:
                query += " AND item_id IN"
            query += " (SELECT i.item_id FROM items i, item_resists r \
            WHERE i.item_id = r.item_id \
            AND resist_abbr = %s AND resist_value > 0)"
            params += (res,)
        else:
            reply(syntax)
    query += " LIMIT 10;"
    if 'WHERE' in query:
        rows = db(query, params)
        if len(rows) > 0:
            for row in rows:
                reply(row[0])
        else:
            reply(notfound('item(s)'))
    else:
        reply(syntax)
elif cmd == 'who':
    query = "SELECT account_name, char_name FROM chars WHERE vis = true AND account_name \
    = (SELECT account_name FROM chars WHERE LOWER(char_name) = LOWER(%s))"
    params = (oper,)
    rows = db(query, params)
    if len(rows) > 0:
        whocmd(rows)
    else:
        acct = oper.strip('@')
        query = "SELECT account_name, char_name FROM chars WHERE vis = true \
        AND LOWER(account_name) = LOWER(%s)"
        params = (acct,)
        rows = db(query, params)
        if len(rows) > 0:
            whocmd(rows)
        else:
            reply(notfound('character'))
elif cmd == 'clist':
    query ="SELECT char_level, class_name, char_name, char_race, account_name, \
    last_seen FROM chars WHERE vis = true AND account_name = \
    (SELECT account_name FROM chars \
    WHERE LOWER(char_name) = LOWER(%s) AND vis = true)"
    params = (oper,)
    rows = db(query, params)
    if len(rows) > 0:
        clistcmd(rows)
    else:
        acct = oper.strip('@')
        query = "SELECT char_level, class_name, char_name, char_race, \
        account_name, last_seen FROM chars WHERE vis = true \
        AND LOWER(account_name) = LOWER(%s)"
        params = (acct,)
        rows = db(query, params)
        if len(rows) > 0:
            clistcmd(rows)
        else:
            reply(notfound('character'))
elif cmd == 'char':
    query ="SELECT char_level, class_name, char_name, char_race, account_name, \
    last_seen FROM chars WHERE vis = true AND LOWER(char_name) = LOWER(%s)"
    params = (oper,)
    rows = db(query, params)
    if len(rows) > 0:
        reply('['+str(rows[0][0])+' '+rows[0][1]+'] '+rows[0][2]\
        +' ('+rows[0][3]+') (@'+rows[0][4]+') seen '+str(rows[0][5]))
    else:
        reply(notfound('character'))
elif cmd == 'find':
    query = "SELECT account_name, char_name, last_seen FROM chars \
    WHERE vis = true AND account_name = \
    (SELECT account_name FROM chars \
    WHERE LOWER(char_name) = LOWER(%s) AND vis = true) \
    ORDER BY last_seen DESC LIMIT 1"
    params = (oper,)
    rows = db(query, params)
    if len(rows) > 0:
        findcmd(rows)
    else:
        acct = oper.strip('@')
        query = "SELECT account_name, char_name, last_seen FROM chars \
        WHERE vis = true AND LOWER(account_name) = LOWER(%s) \
        ORDER BY last_seen DESC LIMIT 1"
        params = (acct,)
        rows = db(query, params)
        if len(rows) > 0:
            findcmd(rows)
        else:
            reply(notfound('character'))
elif cmd == 'class':
    query="SELECT char_name, class_name, char_race, char_level, account_name FROM chars \
    WHERE LOWER(class_name) = LOWER(%s) AND vis = true AND account_name IN \
    (SELECT account_name FROM chars \
    WHERE last_seen > (CURRENT_TIMESTAMP - INTERVAL '1 minute') AND vis = true) \
    ORDER BY char_level DESC"
    params = (oper,)
    rows = db(query, params)
    if len(rows) > 0:
        for row in rows:
            reply('['+str(row[3])+' '+row[1]+'] '\
            +row[0]+' ('+row[2]+') (@'+row[4]+')')
    else:
        reply(notfound('class'))
elif cmd == 'delalt':
    query = "SELECT account_name, char_name FROM chars WHERE LOWER(char_name) = LOWER(%s) \
    AND account_name = (SELECT account_name FROM chars WHERE char_name = %s)"
    params = (oper,char)
    rows = db(query, params)
    if len(rows) > 0:
        for row in rows:
            query = "UPDATE chars SET vis = false WHERE LOWER(char_name) = LOWER(%s)"
            params = (oper,)
            db(query, params)
            reply('Removed character from your alt list: '+oper)
    else:
        reply(notfound('character or account'))
elif cmd == 'addalt':
    query = "SELECT account_name, char_name FROM chars WHERE LOWER(char_name) = LOWER(%s) \
    AND account_name = (SELECT account_name FROM chars WHERE char_name = %s)"
    params = (oper,char)
    rows = db(query, params)
    if len(rows) > 0:
        for row in rows:
            query = "UPDATE chars SET vis = true WHERE LOWER(char_name) = LOWER(%s)"
            params = (oper,)
            db(query, params)
            reply('Re-added character to your alt list: '+oper)
    else:
        reply(notfound('character or account'))
elif cmd == 'lr':
    # query DB for latest boot_id
    query = "SELECT MAX(boot_id) FROM boots"
    params = ''
    rows = db(query, params)
    curboot = rows[0][0]
    if oper == '': # give user load reports for current boot
        query = "SELECT char_name, report_text, date_trunc('seconds', report_time) \
        FROM loads WHERE boot_id = %s AND deleted IS FALSE"
        params = (curboot,)
        rows = db(query, params)
        if len(rows) > 0:
            reply('Loads reported for current boot:')
            for idx, row in enumerate(rows):
                reply(str(idx+1)+': '+row[1]+' ['+\
                row[0]+' at '+str(row[2])+']')
        else:
            reply('No loads reported for current boot.')
    else: # add load report for current boot
        query = "INSERT INTO loads VALUES(%s, CURRENT_TIMESTAMP, %s, %s, false)"
        params = (curboot, oper, char)
        db(query, params)
        reply('Load reported: '+oper)
elif cmd == 'lrdel':
    if oper.isdigit():
        query = "SELECT boot_id, report_time FROM loads WHERE deleted IS FALSE\
        AND boot_id = (SELECT MAX(boot_id) FROM boots)"
        params = ''
        rows = db(query, params)
        if len(rows) > 0:
            curboot = rows[0][0]
            rtime = rows[int(oper)-1][1]
            query = "UPDATE loads SET deleted = true WHERE boot_id = %s\
            AND report_time = %s"
            params = (curboot, rtime)
            db(query, params)
            reply('Load report '+oper+' deleted')
        else:
            reply('No loads reported for current boot.')
else:
    reply(syntax)
