#!/usr/bin/python

"""
Python source code - Reads a file containing item stats in base 'identify' format,
splits it into appropriate variables, and stores them in the stat DB
"""

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

parser.add_option("-i", "--identify", default=False, metavar='file', 
        action='store', type='string',
        help='Parse a file and create SQL for DB import.')
parser.add_option("-s", "--short", action='store_true', default=False,
        help='Parse item DB for short_stats column.')
parser.add_option("-l", "--long", action='store_true', default=False,
        help='Parse item DB for long_stats column.')
parser.add_option("-e", "--legacy", action='store_true', default=False,
        help='Parse legacy item DB for import to new items DB.')
(options, args) = parser.parse_args()

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
    today = datetime.today()
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
            (flags, restrs, slots, effs) = [], [], [], []
            (name, keys, type, ench, dice, wtype, wclass) = '', '', '', '', '', '', ''
            (wt, val, ac, crit, multi) = 0, 0, 0, 0, 0
            (dam_pct, freq_pct, dam_mod, duration) = 0, 0, 0, 0
            (attrib1, attrib2, ptype) = '', '', ''
            (atval1, atval2, qual, stut, mlvl) = 0, 0, 0, 0, 0
            (pgs, lvl, apps, mchg, cchg) = 0, 0, 0, 0, 0
            lines = item.splitlines()
            for line in lines:
                line = line.strip()
                if "Name '" in line: # item_name
                    name = line.replace("Name '",'')
                    name = name[:len(name)-1]
                elif "Keyword '" in line: # keywords, type
                    # bug: if keywords too long, can't split properly
                    #regex: re.sub(r"Keyword '<stuff>', Item type: [A-Z_]+",' ',items)
                    #with a \n anywhere in the above line after Keyword '
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
                    effs = effs.split() # NOBITS is equivalent to null
                elif "Item is:" in line: # restricts/flags, NOBITSNOBITS null
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
                elif "Total Pages:" in line:
                    # Total Pages: 300
                    pgs = line.replace('Total Pages:','')
                    pgs = int(pgs.strip())
                elif "capacity, charged" in line:
                    # Has 700 capacity, charged with 700 points.
                    psps = line.split('cap')
                    psp = psps[0].replace('Has','')
                    psp = int(psp.strip())
                elif "Poison affects" in line:
                    # Poison affects as blindness at level 25.
                    poiss = line.split('at')
                    lvl = poiss[1].replace('level','')
                    lvl = int(lvl.strip('. '))
                    ptype = poiss[0].replace('Poison affects as','')
                    ptype = ptype.strip()
                elif "Applications remaining" in line:
                    # Applications remaining: 10
                    apps = line.replace('Applications remaining:','')
                    apps = line.strip()
                elif "Stutter:" in line:
                    # Quality: 15, Stutter: 0, Min Level: 40
                    ins = line.split(',')
                    qual = ins[0].replace('Quality:','')
                    qual = int(qual.strip())
                    stut = ins[1].replace('Stutter:','')
                    stut = int(stut.strip())
                    mlvl = ins[2].replace('Min Level:','')
                    mlvl = int(mlvl.strip())
                elif "charges, with" in line: # wand, staff
                    # Has 5 charges, with 4 charges left.
                    chgs = line.split(',')
                    mchg = chgs[0].replace('charges','')
                    mchg = mchg.replace('Has','')
                    mchg = int(mchg.strip())
                    cchg = chgs[1].replace('with','')
                    cchg = cchg.replace('charges left.','')
                    cchg = int(cchg.strip())
                elif "spells of:" in line: # potion/scroll
                    # Level 35 spells of: fly on its own line :/
                    lvl = line.replace('Level','')
                    lvl = lvl.replace('spells of:','')
                    lvl = int(lvl.strip())
                    # input spells manually?
                elif "spell of:" in line: # staff/wand, spell on its own line
                    lvl = line.replace('Level','')
                    lvl = lvl.replace('spell of:','')
                    lvl = int(lvl.strip())
                    # input spell manually?
                elif "Special Effects :" in line: # proc, can be multline sigh
                    pass # input manually?
                elif "Special Bonus" in line: # can be plural or singular
                    pass # manually?
                elif "Combat Critical :" in line:
                    pass # manually?
            # back to 'for item in items' iteration
            # check if exact name is already in DB
            query = "SELECT * FROM items WHERE item_name = %s"
            params = (name,)
            rows = db(query, params)
            if len(rows) > 0:
                # if already in DB, check each stat to see if it matches
                #print name+' is already in the DB.'
                # if it does match, update the date of last_id
                if len(rows) > 0:
                    pass
                # if it doesn't match, mark as potential update and compile
                # update queries
                else:
                    pass
            # if it's not in the DB, compile full insert queries
            else:
                sql = ('INSERT INTO items (item_name, keywords, weight, '
                        'c_value, item_type, full_stats, last_id) '
                        'VALUES(%s, %s, %s, %s, %s, %s, %s) '
                        'RETURNING item_id;')
                params = (name, keys, wt, val, type, item, today)
                cur = conn.cursor()
                print cur.mogrify(sql, (params))
                id = 0 # cur.execute(sql, params) ? conn.commit() ? fetchall() ?
                # build item_slots insert
                sql = ('INSERT INTO item_slots VALUES (%s, %s)')
                for slot in slots:
                    if slot != 'NOBITS':
                        params = (id, slot)
                        print cur.mogrify(sql, (params))
                # build item_specials insert
                sql = ('INSERT INTO item_specials VALUES (%s, %s)')
                if item_type == '':
                    pass
                # build item_attribs insert
                # build item_flags insert
                # build item_restricts insert
                # build item_effects insert
                # build item_enchants insert
                # build item_resists insert (when it's parseable)
        # send all insert/update queries as a .sql file to review
        # manual updates: resists (for now) procs, spells for potion/scroll/staff/wand,
        # container holds/wtless, zone, quest/used/rare/invasion/store

# generate short_stats from new items tables
def short_stats():
    query = "SELECT item_id FROM items"
    params = ''
    ids = db(query, params)
    for id in ids:
        query = ("SELECT item_name, "
                "INITCAP(item_type), weight, c_value, "
                "from_zone, last_id, is_rare, from_store, from_quest, "
                "for_quest, from_invasion, out_of_game, no_identify "
                "FROM items WHERE item_id = %s")
        params = (id[0],)
        item = db(query, params)
        i = item[0][0]
        query = "SELECT INITCAP(slot_abbr) FROM item_slots WHERE item_id = %s"
        slots = db(query, params)
        if len(slots) > 0: # if item has worn slots
            for slot in slots:
                i += ' ('+slot[0]+')'
        query = ("SELECT UPPER(spec_abbr), spec_value FROM item_specials "
                "WHERE item_id = %s AND item_type = 'armor'")
        specs = db(query, params)
        if len(specs) > 0: # if item has AC because it's type Armor
            for spec in specs:
                i += ' '+spec[0]+':'+str(spec[1])
        # put in attribs
        query = ("SELECT INITCAP(attrib_abbr), attrib_value "
                "FROM item_attribs WHERE item_id = %s")
        attrs = db(query, params)
        if len(attrs) > 0:
            for att in attrs:
                i += ' '+att[0]+':'+str(att[1])
        query = ("SELECT INITCAP(resist_abbr), resist_value "
                "FROM item_resists WHERE item_id = %s")
        resi = db(query, params)
        if len(resi) > 0: # if item has resistances
            for res in resi:
                i += ' '+res[0]+':'+str(res[1])+'%'
        query = ("SELECT item_type, INITCAP(spec_abbr), INITCAP(spec_value) "
                "FROM item_specials "
                "WHERE item_id = %s AND item_type != 'armor'")
        specs = db(query, params)
        if len(specs) > 0: # if item has specials, like weapon or instrument
            special = ' * ('+item[0][1]+')'
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
        query = ("SELECT INITCAP(effect_abbr) "
                "FROM item_effects WHERE item_id = %s")
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
        query = ("SELECT INITCAP(ench_name), "
                "dam_pct, freq_pct, sv_mod, duration "
                "FROM item_enchants WHERE item_id = %s")
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
        query = "SELECT INITCAP(flag_abbr) FROM item_flags WHERE item_id = %s"
        flags = db(query, params)
        if len(flags) > 0: # if item has flags like magic
            i += ' *'
            for flag in flags:
                i += ' '+flag[0]
        query = ("SELECT INITCAP(restrict_abbr) "
                "FROM item_restricts WHERE item_id = %s")
        restr = db(query, params)
        if len(restr) > 0: # if item has restrictions
            i += ' *'
            for res in restr:
                i += ' '+res[0]
        type = ' *'
        if item[0][12]:
            type += ' NoID'
        if item[0][2] != None:
            type += ' Wt:'+str(item[0][2])
        if item[0][3] != None:
            type += ' Val:'+str(item[0][3])
        #type += ' Type:'+item[0][1]
        i += type
        # add is_rare, from_quest, etc. to zone info
        zext = ''
        if item[0][6]:
            zext += 'R'
        if item[0][7]:
            zext += 'S'
        if item[0][8]:
            zext += 'Q'
        if item[0][9]:
            zext += 'U'
        if item[0][10]:
            zext += 'I'
        if item[0][11]:
            zext += 'O'
        zone = item[0][4]
        if zext != '':
            zone += ' ('+zext+')'
        i += ' * Zone: '+zone+' * Last ID: '+str(item[0][5])
        #print 'Item '+str(id[0])+': '+i
        query = "UPDATE items SET short_stats = %s WHERE item_id = %s"
        params = (i, id[0])
        db(query, params)

def long_stats():
    query = "SELECT item_id FROM items"
    params = ''
    ids = db(query, params)
    for id in ids:
        query = ("SELECT item_name, "
                "item_type, weight, c_value, zone_name, last_id, "
                "is_rare, from_store, from_quest, for_quest, from_invasion, "
                "out_of_game, no_identify, keywords "
                "FROM items i, zones z "
                "WHERE i.from_zone = z.zone_abbr AND item_id = %s")
        params = (id[0],)
        item = db(query, params)
        i = item[0][0]
        query = ("SELECT i.slot_abbr, slot_display "
                "FROM item_slots i, slots s "
                "WHERE i.slot_abbr = s.slot_abbr AND item_id = %s")
        slots = db(query, params)
        if len(slots) > 0:
            i += ' *'
            for slot in slots:
                i += ', '+slot[1]
            i += ' *'
        query = ("SELECT i.spec_abbr, spec_value, spec_display "
                "FROM item_specials i, specials s "
                "WHERE i.spec_abbr = s.spec_abbr AND item_id = %s "
                "AND i.spec_abbr = 'ac'")
        specs = db(query, params)
        if len(specs) > 0:
            i += ', '+specs[0][2]+': '+str(specs[0][1])
        query = ("SELECT i.attrib_abbr, attrib_value, attrib_display "
                "FROM item_attribs i, attribs a "
                "WHERE i.attrib_abbr = a.attrib_abbr AND item_id = %s")
        attrs = db(query, params)
        if len(attrs) > 0:
            i += ' *'
            for att in attrs:
                i += ', '+att[2]+': '+str(att[1])
        query = ("SELECT i.resist_abbr, resist_value, resist_display "
                "FROM item_resists i, resists r "
                "WHERE i.resist_abbr = r.resist_abbr AND item_id = %s")
        resis = db(query, params)
        if len(resis) > 0:
            i += ' *'
            for res in resis:
                i += ', '+res[2]+': '+str(res[1])+'%'
        query = ("SELECT i.spec_abbr, spec_value, spec_display "
                "FROM item_specials i, specials s "
                "WHERE i.spec_abbr = s.spec_abbr AND item_id = %s "
                "AND i.spec_abbr != 'ac' "
                "GROUP BY i.spec_abbr, spec_value, spec_display")
        specs = db(query, params)
        # should really switch this out into lots of if/else for proper
        # formatting, right now it's bugged
        if len(specs) > 0:
            i += ' *'
            if item[0][1] == 'crystal' or item[0][1] == 'spellbook' or \
            item[0][1] == 'comp_bag' or item[0][1] == 'ammo':
                for spec in specs:
                    i += ', '+spec[2]+': '+str(spec[1])
            elif item[0][1] == 'container':
                pass
            elif item[0][1] == 'poison':
                pass
            elif item[0][1] == 'scroll' or item[0][1] == 'potion':
                pass
            elif item[0][1] == 'staff' or item[0][1] == 'wand':
                pass
            elif item[0][1] == 'instrument':
                pass
            elif item[0][1] == 'weapon':
                pass
        query = ("SELECT i.effect_abbr, effect_display "
                "FROM item_effects i, effects e "
                "WHERE i.effect_abbr = e.effect_abbr AND item_id = %s")
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
        query = ("SELECT ench_name, dam_pct, freq_pct, sv_mod, duration "
                "FROM item_enchants WHERE item_id = %s")
        enchs = db(query, params)
        if len(enchs) > 0:
            i += ' *'
            pass
        query = ("SELECT i.flag_abbr, flag_display "
                "FROM item_flags i, flags f "
                "WHERE i.flag_abbr = f.flag_abbr AND item_id = %s")
        flags = db(query, params)
        if len(flags) > 0:
            i += ' *'
            for flag in flags:
                i += ', '+flag[1]
        query = ("SELECT i.restrict_abbr, restrict_name "
                "FROM item_restricts i, restricts r "
                "WHERE i.restrict_abbr = r.restrict_abbr AND item_id = %s")
        rests = db(query, params)
        if len(rests) > 0:
            i += ' *'
            for rest in rests:
                i += ', '+rest[1]
        if item[0][13]:
            i += ' * Keywords:('+item[0][13]+')'
        type = ' *'
        if item[0][12]:
            type += ', No-Identify'
        if item[0][2] != None:
            wt = locale.format("%d", item[0][2], grouping=True)
            type += ', Weight: '+str(wt)+' lbs'
        if item[0][3] != None:
            val = locale.format("%d", item[0][3], grouping=True)
            type += ', Value: '+str(val)+' copper'
        #type += ', Type: '+item[0][1]
        i += type
        # add is_rare, from_quest, etc. to zone info
        zext = ''
        if item[0][6]:
            zext += ', Is Rare'
        if item[0][7]:
            zext += ', From Store'
        if item[0][8]:
            zext += ', From Quest'
        if item[0][9]:
            zext += ', Used In Quest'
        if item[0][10]:
            zext += ', From Invasion'
        if item[0][11]:
            zext += ', Out Of Game'
        zone = item[0][4]
        if zext != '':
            zone += ' ('+zext+')'
            zone = zone.replace('(, ', '(')
        i += ' * Zone: '+zone+' * Last ID: '+str(item[0][5])
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

if conn:
    conn.close()
