#!/usr/bin/python

"""
Python source code - Reads a file containing item stats in base 'identify' format,
splits it into appropriate variables, and stores them in the stat DB
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import psycopg2
import locale
import re
from optparse import OptionParser # replace with argparse in 2.7
from datetime import datetime, timedelta
from subprocess import Popen, PIPE

timestart = datetime.now()
locale.setlocale(locale.LC_ALL, 'en_US')

parser = OptionParser()

parser.add_option("-i", "--identify", default='newstats.txt', metavar='file', 
        action='store', type='string',
        help='Parse a file and create SQL for DB import.')
parser.add_option("-s", "--short", action='store_true', default=False,
        help='Parse item DB for short_stats column.')
parser.add_option("-l", "--long", action='store_true', default=False,
        help='Parse item DB for long_stats column.')
parser.add_option("-e", "--legacy", action='store_true', default=False,
        help='Parse legacy item DB for import to new items DB.')
(options, args) = parser.parse_args()

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

# import short_stats from torileq website output
def import_legacy():
    cmd = 'cat'
    file = 'short_stats.txt'
    stats = Popen([cmd, file], stdout=PIPE, stderr=PIPE).communicate()
    if stats[1] != '':
        print 'Error: '+stats[1]
    else:
        lines = stats[0].splitlines()
        for line in lines:
            line = line.strip()
            item = line.split('*', 1)
            name = item[0].strip()
            query = "UPDATE items SET short_stats = %s WHERE item_name = %s"
            params = (line, name)
            db(query, params)

def parse_identify():
    cmd = 'cat'
    file = options.identify
    stats = Popen([cmd, file], stdout=PIPE, stderr=PIPE).communicate()
    if stats[1] != '':
        print 'Error: '+stats[1]
    else: 
        # put all flags/restricts, or effects, on one line
        items = re.sub(r'(?<=[A-Z]){2}\n(?=[A-Z]{2})',' ', stats[0])
        # put enchant info on one line
        items = re.sub(r'\n(?=Duration)',' ', items)
        # split into separate items
        items = items.split('\n\n')
        for item in items:
            # instantiate a blank item template with all variables at default
            (flags, restrs) = [], []
            (name, keys, type, ench, dice, wtype, wclass) = '', '', '', '', '', '', ''
            (slots, effs) = [], []
            (wt, val, ac, crit, multi) = 0, 0, 0, 0, 0
            (dam_pct, freq_pct, dam_mod, duration) = 0, 0, 0, 0
            (attrib1, attrib2) = '', ''
            (atval1, atval2) = 0, 0
            lines = item.splitlines()
            for line in lines:
                line = line.strip()
                if "Name '" in line: # item_name
                    name = line.replace("Name '",'')
                    name = name[:len(name)-1]
                elif "Keyword '" in line: # keywords, type
                    kt = line.split(',')
                    keys = kt[0].replace("Keyword '",'')
                    keys = keys.strip("' ")
                    type = kt[1].replace("Item type:",'')
                    type = type.strip()
                elif "Item can be worn" in line: # worn slots
                    worn = line.replace("Item can be worn on:",'')
                    worn = worn.strip()
                    slots = worn.split()
                elif "Item will give you" in line: # effects
                    effs = line.replace("Item will give you following abilities:",'')
                    effs = effs.split() # NOBITS is equivalent to empty
                elif "Item is:" in line: # restricts/flags
                    rfs = line.replace("Item is:",'')
                    rfs = rfs.split()
                    for rf in rfs:
                        if rf.startswith("ANTI-") or rf.startswith("NO-"):
                            restrs.append(rf)
                        else:
                            flags.append(rf)
                elif "Weight:" in line: # wt/val
                    wv = line.split(',')
                    wt = wv[0].replace("Weight:",'')
                    wt = int(wt.strip())
                    val = wv[1].replace("Value:",'')
                    val = int(val.strip())
                elif "AC-apply is" in line: # AC
                    ac = line.replace("AC-apply is",'')
                    ac = int(ac.strip())
                elif "Damage Dice" in line: # old weapon dice
                    dice = line.replace("Damage Dice are '",'')
                    dice = dice.strip("' ")
                elif "Class:" in line: # new weapon, type/class
                    tc = line.replace("Type: ",'')
                    tc = tc.replace("Class: ",'')
                    tc = tc.rsplit(None, 1)
                    wtype = tc[0].strip()
                    wclass = tc[1].strip()
                elif "Crit Range:" in line: # new weapon, dice/crit/multi
                    dcc = line.split('%')
                    dc = dcc[0].replace("Damage:",'')
                    dc = dc.replace("Crit Range:",'')
                    dc = dc.split()
                    dice = dc[0]
                    crit = int(dc[1])
                    multi = dcc[1].replace("Crit Bonus: ",'')
                    multi = multi.strip('x ')
                    multi = int(multi)
                elif "Frequency:" in line: # enchantment
                    enchs = line.replace('Type:','')
                    enchs = enchs.replace('Damage:','')
                    enchs = enchs.replace('Frequency:','')
                    enchs = enchs.replace('Modifier:','')
                    enchs = enchs.replace('Duration:','')
                    enchs = enchs.replace('%','')
                    enchs = enchs.rsplit(None, 4)
                    ench = enchs[0]
                    dam_pct = int(enchs[1])
                    freq_pct = int(enchs[2])
                    dam_mod = int(enchs[3])
                    duration = int(enchs[4])
                elif "Affects :" in line: # attribs
                    attrs = line.replace("Affects :",'')
                    attrs = attrs.replace('by','By')
                    attrs = attrs.split('By')
                    if attrib1 == '':
                        attrib1 = attrs[0]
                        atval1 = int(attrs[1])
                    else:
                        attrib2 = attrs[0]
                        atval2 = int(attrs[1])
                elif "Special Effects :" in line: # proc, can be multline sigh
                    pass
                elif "Special Bonus" in line: # can be plural or singular
                    pass
                elif "Combat Critical :" in line:
                    pass
                elif "spells of:" in line:
                    pass # Level 35 spells of: fly on its own line :/
                elif "Total Pages:" in line:
                    pass # Total Pages: 300
            # back to 'for item in items' iteration
            # check if exact name is already in DB
            query = "SELECT * FROM items WHERE item_name = %s"
            params = (name,)
            rows = db(query, params)
            if len(rows) > 0:
                # if already in DB, check each stat to see if it matches
                pass
                # if it does match, update the date of last_id
                if len(rows) > 0:
                    pass
                # if it doesn't match, mark as potential update and compile update queries
                else:
                    pass
            # if it's not in the DB, compile full insert queries
            else:
                pass
        # send all insert/update queries as a .sql file to review

# generate short_stats from new items tables
def short_stats():
    query = "SELECT item_id FROM items"
    params = ''
    ids = db(query, params)
    for id in ids:
        query = "SELECT item_name, initcap(attrib1), attrib1_value, \
        initcap(attrib2), attrib2_value, initcap(item_type), weight, c_value, \
        from_zone, last_id, is_rare, from_store, from_quest, for_quest, \
        from_invasion, out_of_game, no_identify \
        FROM items WHERE item_id = %s"
        params = (id[0],)
        item = db(query, params)
        i = item[0][0]
        query = "SELECT initcap(slot_abbr) FROM item_slots WHERE item_id = %s"
        slots = db(query, params)
        if len(slots) > 0: # if item has worn slots
            for slot in slots:
                i += ' ('+slot[0]+')'
        query = "SELECT upper(spec_abbr), spec_value FROM item_specials \
        WHERE item_id = %s AND item_type = 'armor'"
        specs = db(query, params)
        if len(specs) > 0: # if item has AC because it's type Armor
            for spec in specs:
                i += ' '+spec[0]+':'+str(spec[1])
        if item[0][1] != None:
            i += ' '+item[0][1]+':'+str(item[0][2])
        if item[0][3] != None:
            i += ' '+item[0][3]+':'+str(item[0][4])
        query = "SELECT initcap(resist_abbr), resist_value \
        FROM item_resists WHERE item_id = %s"
        resi = db(query, params)
        if len(resi) > 0: # if item has resistances
            for res in resi:
                i += ' '+res[0]+':'+str(res[1])+'%'
        query = "SELECT item_type, initcap(spec_abbr), initcap(spec_value) \
        FROM item_specials \
        WHERE item_id = %s AND item_type != 'armor'"
        specs = db(query, params)
        if len(specs) > 0: # if item has specials, like weapon or instrument
            special = ' * ('+item[0][5]+')'
            if specs[0][0] == 'crystal' or specs[0][0] == 'spellbook' or \
            specs[0][0] == 'comp_bag' or specs[0][0] == 'ammo':
                for spec in specs:
                    special += ' '+spec[1]+':'+spec[2]
            elif specs[0][0] == 'container':
                (holds, wtless) = '', ''
                for spec in specs:
                    if spec[1] == 'Holds':
                        holds = ' '+spec[1]+':'+spec[2]
                    elif spec[1] == 'Wtless':
                        wtless = ' '+spec[1]+':'+spec[2]
                special += holds+wtless
            elif specs[0][0] == 'poison':
                (lvl, type, apps) = '', '', ''
                for spec in specs:
                    if spec[1] == 'Level':
                        lvl = ' Lvl:'+spec[2]
                    elif spec[1] == 'Type':
                        type = ' '+spec[1]+':'+spec[2]
                    elif spec[1] == 'Apps':
                        apps = ' '+spec[1]+':'+spec[2]
                special += lvl+type+apps
            elif specs[0][0] == 'scroll' or specs[0][0] == 'potion':
                (lvl, sp1, sp2, sp3) = '', '', '', ''
                for spec in specs:
                    if spec[1] == 'Level':
                        lvl = ' Lvl:'+spec[2]
                    elif spec[1] == 'Spell1':
                        sp1 = ' '+spec[2]
                    elif spec[1] == 'Spell2' or spec[1] == 'Spell3':
                        sp2 = ' - '+spec[2]
                special += lvl+sp1+sp2+sp3
            elif specs[0][0] == 'staff' or specs[0][0] == 'wand':
                (lvl, sp, ch) = '', '', ''
                for spec in specs:
                    if spec[1] == 'Level':
                        lvl = ' Lvl:'+spec[2]
                    elif spec[1] == 'Spell':
                        sp = ' '+spec[2]
                    elif spec[1] == 'Charges':
                        ch = ' '+spec[1]+':'+spec[2]
                special += lvl+sp+ch
            elif specs[0][0] == 'instrument':
                (qua, stu, min) = '', '', ''
                for spec in specs:
                    if spec[1] == 'Quality':
                        qua = ' '+spec[1]+':'+spec[2]
                    elif spec[1] == 'Stutter':
                        stu = ' '+spec[1]+':'+spec[2]
                    elif spec[1] == 'Min_Level':
                        min = ' '+spec[1]+':'+spec[2]
                special += qua+stu+min
            elif specs[0][0] == 'weapon':
                (dice, type, clas, crit, multi) = '', '', '', '', ''
                for spec in specs:
                    if spec[1] == 'Dice':
                        dice = ' '+spec[1]+':'+spec[2]
                    elif spec[1] == 'Crit':
                        crit = ' '+spec[1]+':'+spec[2]+'%'
                    elif spec[1] == 'Multi':
                        multi = ' '+spec[1]+':'+spec[2]+'x'
                    elif spec[1] == 'Class':
                        clas = ' ('+spec[1]+':'+spec[2]
                    elif spec[1] == 'Type':
                        type = ' '+spec[1]+':'+spec[2]+')'
                special += dice+crit+multi+clas+type
            i += special
        query = "SELECT initcap(effect_abbr) FROM item_effects WHERE item_id = %s"
        effects = db(query, params)
        if len(effects) > 0: # if item has effects like infra
            i += ' *'
            for eff in effects:
                i += ' '+eff[0]
        query = "SELECT proc_name FROM item_procs WHERE item_id = %s"
        procs = db(query, params)
        if len(procs) > 0: # if item has procs
            process = ' * Procs:'
            for proc in procs:
                if process == ' * Procs:':
                    process += ' '+proc[0]
                else:
                    process += ' - '+proc[0]
            i += process
        query = "SELECT initcap(ench_name), dam_pct, freq_pct, sv_mod, duration \
        FROM item_enchants WHERE item_id = %s"
        enchs = db(query, params)
        if len(enchs) > 0: # if item has weapon enchantment
            enchant = ' *'
            for ench in enchs:
                if enchant == ' *':
                    enchant += ' '
                else:
                    enchant += ' - '
                enchant += ench[0]+' '+str(ench[1])+'% '+str(ench[2])\
                +'% '+str(ench[3])+' '+str(ench[4])
            i += enchant
        query = "SELECT initcap(flag_abbr) FROM item_flags WHERE item_id = %s"
        flags = db(query, params)
        if len(flags) > 0: # if item has flags like magic
            i += ' *'
            for flag in flags:
                i += ' '+flag[0]
        query = "SELECT initcap(restrict_abbr) FROM item_restricts WHERE item_id = %s"
        restr = db(query, params)
        if len(restr) > 0: # if item has restrictions
            i += ' *'
            for res in restr:
                i += ' '+res[0]
        type = ' *'
        if item[0][16] != None:
            type += ' NoID'
        if item[0][6] != None:
            type += ' Wt:'+str(item[0][6])
        if item[0][7] != None:
            type += ' Val:'+str(item[0][7])
        #type += ' Type:'+item[0][5]
        i += type
        # add is_rare, from_quest, etc. to zone info
        zext = ''
        if item[0][10]:
            zext += 'R'
        if item[0][11]:
            zext += 'S'
        if item[0][12]:
            zext += 'Q'
        if item[0][13]:
            zext += 'U'
        if item[0][14]:
            zext += 'I'
        if item[0][15]:
            zext += 'O'
        zone = item[0][8]
        if zext != '':
            zone += ' ('+zext+')'
        i += ' * Zone: '+zone+' * Last ID: '+str(item[0][9])
        #print 'Item '+str(id[0])+': '+i
        query = "UPDATE items SET short_stats = %s WHERE item_id = %s"
        params = (i, id[0])
        db(query, params)

def long_stats():
    query = "SELECT item_id FROM items"
    params = ''
    ids = db(query, params)
    for id in ids:
        query = "SELECT item_name, attrib1, attrib1_value, attrib2, \
        attrib2_value, item_type, weight, c_value, zone_name, last_id, \
        is_rare, from_store, from_quest, for_quest, from_invasion, \
        out_of_game, no_identify, keywords \
        FROM items i, zones z \
        WHERE i.from_zone = z.zone_abbr AND item_id = %s"
        params = (id[0],)
        item = db(query, params)
        i = item[0][0]
        query = "SELECT i.slot_abbr, slot_display \
        FROM item_slots i, slots s \
        WHERE i.slot_abbr = s.slot_abbr AND item_id = %s"
        slots = db(query, params)
        if len(slots) > 0:
            i += ' *'
            for slot in slots:
                i += ', '+slot[1]
            i += ' *'
        query = "SELECT i.spec_abbr, spec_value, spec_display \
        FROM item_specials i, specials s \
        WHERE i.spec_abbr = s.spec_abbr AND item_id = %s \
        AND i.spec_abbr = 'ac'"
        specs = db(query, params)
        if len(specs) > 0:
            i += ', '+specs[0][2]+': '+str(specs[0][1])
        if item[0][1] != None:
            query = "SELECT attrib_display FROM attribs \
            WHERE attrib_abbr = %s"
            params = (item[0][1],)
            attrs = db(query, params)
            if len(attrs) > 0:
                i += ', '+attrs[0][0]+': '+str(item[0][2])
        if item[0][3] != None:
            query = "SELECT attrib_display FROM attribs \
            WHERE attrib_abbr = %s"
            params = (item[0][3],)
            attrs = db(query, params)
            if len(attrs) > 0:
                i += ', '+attrs[0][0]+': '+str(item[0][4])
        query = "SELECT i.resist_abbr, resist_value, resist_display \
        FROM item_resists i, resists r \
        WHERE i.resist_abbr = r.resist_abbr AND item_id = %s"
        params = (id[0],)
        resis = db(query, params)
        if len(resis) > 0:
            i += ' *'
            for res in resis:
                i += ', '+res[2]+': '+str(res[1])+'%'
        query = "SELECT i.spec_abbr, spec_value, spec_display \
        FROM item_specials i, specials s \
        WHERE i.spec_abbr = s.spec_abbr AND item_id = %s \
        AND i.spec_abbr != 'ac' \
        GROUP BY i.spec_abbr, spec_value, spec_display"
        specs = db(query, params)
        if len(specs) > 0:
            i += ' *'
            for spec in specs:
                i += ', '+spec[2]+': '+str(spec[1])
        query = "SELECT i.effect_abbr, effect_display \
        FROM item_effects i, effects e \
        WHERE i.effect_abbr = e.effect_abbr AND item_id = %s"
        effs = db(query, params)
        if len(effs) > 0:
            i += ' *'
            for eff in effs:
                i += ', '+eff[1]
        query = "SELECT proc_name FROM item_procs WHERE item_id = %s"
        procs = db(query, params)
        if len(procs) > 0:
            i += ' *'
            for proc in procs:
                i += ', '+proc[0]
        query = "SELECT ench_name, dam_pct, freq_pct, sv_mod, duration \
        FROM item_enchants WHERE item_id = %s"
        enchs = db(query, params)
        if len(enchs) > 0:
            i += ' *'
            pass
        query = "SELECT i.flag_abbr, flag_display \
        FROM item_flags i, flags f \
        WHERE i.flag_abbr = f.flag_abbr AND item_id = %s"
        flags = db(query, params)
        if len(flags) > 0:
            i += ' *'
            for flag in flags:
                i += ', '+flag[1]
        query = "SELECT i.restrict_abbr, restrict_name \
        FROM item_restricts i, restricts r \
        WHERE i.restrict_abbr = r.restrict_abbr AND item_id = %s"
        rests = db(query, params)
        if len(rests) > 0:
            i += ' *'
            for rest in rests:
                i += ', '+rest[1]
        if item[0][17]:
            i += ' * Keywords:('+item[0][17]+')'
        type = ' *'
        if item[0][16]:
            type += ', No-Identify'
        if item[0][6] != None:
            wt = locale.format("%d", item[0][6], grouping=True)
            type += ', Weight: '+str(wt)+' lbs'
        if item[0][7] != None:
            val = locale.format("%d", item[0][7], grouping=True)
            type += ', Value: '+str(val)+' copper'
        #type += ', Type: '+item[0][5]
        i += type
        # add is_rare, from_quest, etc. to zone info
        zext = ''
        if item[0][10]:
            zext += ', Is Rare'
        if item[0][11]:
            zext += ', From Store'
        if item[0][12]:
            zext += ', From Quest'
        if item[0][13]:
            zext += ', Used In Quest'
        if item[0][14]:
            zext += ', From Invasion'
        if item[0][15]:
            zext += ', Out Of Game'
        zone = item[0][8]
        if zext != '':
            zone += ' ('+zext+')'
            zone = zone.replace('(, ', '(')
        i += ' * Zone: '+zone+' * Last ID: '+str(item[0][9])
        i = i.replace('*, ', '* ')
        i = i.replace('* *', '*')
        #print 'Item '+str(id[0])+': '+i
        query = "UPDATE items SET long_stats = %s WHERE item_id = %s"
        params = (i, id[0])
        db(query, params)

if options.legacy:
    import_legacy()
if options.identify:
    parse_identify()
if options.short:
    short_stats()
if options.long:
    long_stats()

timediff = datetime.now() - timestart
print 'The script took '+str(timediff)

