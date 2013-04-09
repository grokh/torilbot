#!/usr/bin/python

"""
Python source code - Call this script to convert Kegor/Nerun's item stat DB
to new format after cleaning up all the old entries
"""

import sys
import psycopg2
from datetime import datetime, timedelta

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

# delete duplicate items
queries = ("delete from legacy where id = 451;"
, "delete from legacy where id = 452;"
, "delete from legacy where id = 2193;"
, "delete from legacy where id = 5789;"
, "delete from legacy where id = 6119;"
, "delete from legacy where id = 5674;"
, "delete from legacy where id = 4633;"
, "delete from legacy where id = 4684;"
, "delete from legacy where id = 1156;"
, "delete from legacy where id = 7765;"
, "delete from legacy where id = 4663;"
, "delete from legacy where id = 6922;"
, "delete from legacy where id = 6923;"
, "delete from legacy where id = 860;"
, "delete from legacy where id = 3341;"
, "delete from legacy where id = 4748;"
, "delete from legacy where id = 7455;"
, "delete from legacy where id = 753;"
, "delete from legacy where id = 2635;"
, "delete from legacy where id = 1023;"
, "delete from legacy where id = 1354;"
, "delete from legacy where id = 4720;"
, "delete from legacy where id = 4003;"
, "delete from legacy where id = 7732;"
, "delete from legacy where id = 2110;"
, "delete from legacy where id = 5238;"
, "delete from legacy where id = 3172;"
, "delete from legacy where id = 7763;"
# correct duplicate item names
, "update legacy set varname = 'a shimmering cloak of dragonscales 1' where id = 4516;"
, "update legacy set varname = 'a shimmering cloak of dragonscales 2' where id = 4517;"
, "update legacy set varname = 'a bright green potion 1' where id = 654;"
, "update legacy set varname = 'a bright green potion 2' where id = 655;"
, "update legacy set varname = 'a potion of invisibility 1' where id = 3769;"
, "update legacy set varname = 'a potion of invisibility 2' where id = 3770;"
, "update legacy set varname = 'a silver githyanki longsword 1' where id = 4682;"
, "update legacy set varname = 'a silver githyanki longsword 2' where id = 4683;"
, "update legacy set varname = 'the fiery crown of Surtur 1' where id = 7599;"
# change vardate to actual date type
, "update legacy set vardate = '6-23-07' where id = 3892;"
, "alter table legacy alter column vardate type date USING (vardate::date);"
# correct invalid entries in int-style fields
, "update legacy set inthit = null where inthit = 0;"
, "update legacy set intdam = null where intdam = 0;"
, "update legacy set intac = null where intac = 0 and vartype != 'ARMOR';"
, "update legacy set varvalue = '0' where varvalue = '0 new zone'"
, "update legacy set varwt = null where varwt = 'xxxx'"
, "update legacy set varmin = null where varmin = '10?'"
, "update legacy set varlevel = '45' where varlevel = '45.'"
# correct issues with text field entries, primarily setting to null
, "update legacy set varpoison = null where varpoison = '';"
, "update legacy set varbonus = null where varbonus = '';"
, "update legacy set varnoid = false where varnoid = '';"
, "update legacy set varnoid = true where varnoid != 'false';"
, "alter table legacy alter column varnoid type boolean using (varnoid::boolean);"
, "update legacy set varquest = false where varquest = '';"
, "update legacy set varquest = true where varquest != 'false';"
, "alter table legacy alter column varquest type boolean using (varquest::boolean);"
, "update legacy set varcrit = 'Unholy Word' where varcrit = 'Unholy Word Critical';"
, "update legacy set varcrit = null where varcrit = '';"
, "update legacy set varwclass = null where varwclass = '';"
, "update legacy set varwtype = null where varwtype = '';"
, "update legacy set vardice = null where vardice = 'NO-DICE';"
, "update legacy set vardice = null where vardice = '';"
, "update legacy set varenchant = null where varenchant = '';"
, "update legacy set vartype = '' where vartype = '?';"
, "update legacy set vartype = '' where vartype = 'CRUCIBLE';"
, "update legacy set vartype = 'LIQUID_CONT' where vartype = 'LIQUID_CONTAINER';"
, "update legacy set vartype = '' where vartype = 'UNDEFINED';"
, "update legacy set vartype = null where vartype = '';"
, "update legacy set varceffects = null where varceffects = '';"
, "update legacy set varname = 'a magical wand of the ice queen' where varname = 'a maical wand of the ice queen';"
, "update legacy set vardice = null where varname = 'a magical wand of the ice queen';"
, "update legacy set vartype = 'wand' where varname = 'a magical wand of the ice queen';"
, "update legacy set vartype = 'trash' where varname = 'a sprig of witch bane';"
, "update legacy set vartype = 'light' where varname = 'a globe of eternal light';"
, "update legacy set varworn = trim(varworn);"
, "update legacy set vartype = 'TREASURE' where varworn = '0';"
, "update legacy set varworn = 'INSIGNIA' where varworn = '0';"
, "update legacy set varworn = 'NOBITS' where varworn = 'NOBIT';"
, "update legacy set varworn = 'WIELD 2H' where varworn = 'NOBITS 2H';"
, "update legacy set varworn = 'WIELD' where varworn = 'WIELD 1H';"
, "update legacy set varworn = 'WIELD 2H' where varworn = '2H';"
, "update legacy set varaflags = 'SENSE-LIFE' where varaflags = 'SENSE-LIFE GROUP_CACHED ';"
, "update legacy set varaflags = 'NOBITS' where varaflags = 'GROUP_CACHED ';"
, "update legacy set varaflags = 'NOBITS' where varaflags = '';"
, "update legacy set vareffects = 'Chromatic Orb - Reflective Prisms' where vareffects = 'Chromatic Orb                 Reflective Prisms';"
, "update legacy set vareffects = E'Chimera\\'s Recall' where vareffects = E'\\'chimera\\'s recall\\'';"
, "update legacy set vareffects = E'Resiliency - Leopard Stance' where vareffects = E'\\'Resiliency\\' - \\'Leapard Stance\\'';"
, "update legacy set vareffects = null where vareffects = '';"
, "update legacy set varwspell = null where varwspell = 'UNKNOWN SPELL';"
, "update legacy set varwspell = null where varwspell = 'Undefined';"
, "update legacy set varwspell = null where varwspell = 'archery';"
, "update legacy set varwspell = null where varwspell = '';"
, "update legacy set variflags = trim(variflags);"
, "update legacy set variflags = 'MAGIC' where variflags = 'MAGIC NO-??';"
, "update legacy set variflags = '' where variflags = '?';"
, "update legacy set variflags = '' where variflags = 'STATS-UNKNOWN';"
, "update legacy set variflags = '' where variflags = '(Cannot Recite)';"
, "update legacy set variflags = '' where variflags = 'TRAP';"
, "update legacy set variflags = 'GLOW BLESS FLOAT TRANSIENT NORENT NO-PC' where variflags = 'GLOW BLESS FLOAT TRANSIENT NORENT ANTI-PLAYER';"
, "update legacy set variflags = 'NODROP TWOHANDS' where variflags = 'NODROP TWOHAND';"
, "update legacy set variflags = 'MAGIC NODROP TWOHANDS' where variflags = 'MAGIC NODROP TWO-HANDS';"
, "update legacy set variflags = 'MAGIC NOBURN ANTIPALADIN-ONLY' where variflags = 'MAGIC NOBURN ANTI-PALADIN ONLY';"
, "update legacy set variflags = 'NOTAKE' where variflags = 'NO-TAKE';"
, "update legacy set variflags = 'MAGIC NOTAKE' where variflags = 'MAGIC NO-TAKE';"
, "update legacy set variflags = 'MAGIC NODROP ANTI-EVIL ANTI-NEUTRAL NO-CLERIC NO-THIEF NO-MAGE' where variflags = 'MAGIC NO-DROP ANTI-EVIL ANTI-NEUTRAL NO-CLERIC NO-THIEF NO-MAGE';"
, "update legacy set variflags = 'MAGIC NORENT ANTI-NEUTRAL FLOAT NOBURN NO-CLERIC NO-THIEF NO-MAGE' where variflags = 'MAGIC NO-RENT ANTI-NEUTRAL FLOAT NOBURN NO-CLERIC NO-THIEF NO-MAGE';"
, "update legacy set variflags = 'ANTI-GOOD ANTI-NEUTRAL NO-WARRIOR NO-THIEF' where variflags = 'NO-GOOD NO-NEUTRAL NO-WARRIOR NO-THIEF';"
, "update legacy set variflags = 'ANTI-GOOD' where variflags = 'NO-GOOD';"
, "update legacy set variflags = 'MAGIC ANTI-GOOD ANTI-NEUTRAL' where variflags = 'MAGIC NO-GOOD NO-NEUTRAL';"
, "update legacy set variflags = 'MAGIC ANTI-GOOD ANTI-NEUTRAL NO-WARRIOR NO-THIEF NO-MAGE' where variflags = 'MAGIC NO-GOOD NO-NEUTRAL NO-WARRIOR NO-THIEF NO-MAGE';"
, "update legacy set variflags = 'MAGIC GLOW NODROP ANTI-GOOD' where variflags = 'MAGIC GLOW NODROP NO-GOOD';"
# create new columns for boolean handling of source/use
, "alter table legacy add column from_quest boolean;"
, "alter table legacy add column from_store boolean;"
, "alter table legacy add column from_invasion boolean;"
, "alter table legacy add column out_of_game boolean;"
, "alter table legacy add column is_rare boolean;"
)

params = ''
for query in queries:
    #print 'Running query: '+query
    db(query, params)

# change many columns to type integer
cols = ("varwt", "varholds", "varvalue", "varpages", "varhp", "varcrange",
"varstr", "varagi", "vardex", "varcon", "varpow", "varint", "varwis", "varcha",
"varmaxstr", "varmaxagi", "varmaxdex", "varmaxcon", "varmaxpow", "varmaxint",
"varmaxwis", "varmaxcha", "varluck", "varkarma", "varmana", "varmove", "varage",
"varweight", "varheight", "varmr", "varsfele", "varsfenc", "varsfheal",
"varsfill", "varsfinv", "varsfnature", "varsfnec", "varsfprot", "varsfpsi",
"varsfspirit", "varsfsum", "varsftele", "varpsp", "varquality", "varstutter",
"varmin", "varlevel", "varapplications", "varcharge", "varmaxcharge", "varwlevel",
"varunarmd", "varslash", "varbludgn", "varpierce", "varrange", "varspells",
"varsonic", "varpos", "varneg", "varpsi", "varmental", "vargoods", "varevils",
"varlaw", "varchaos", "varforce", "varfire", "varcold", "varelect", "varacid",
"varpois", "varspell", "varbreath", "varpara", "varpetri", "varrod", "vararmor",
"varcbonus")

for col in cols:
    #print 'Collecting rows from: '+col
    query = "SELECT id, "+col+" FROM legacy"
    params = ''
    rows = db(query, params)
    for row in rows:
        id = str(row[0])
        if row[1] is not None:
            val = str(row[1])
            if val.endswith('%'):
                #print 'Fixing item '+id+' for %'
                query = "update legacy set "+col+" = %s where id = %s"
                val = val.rstrip('%')
                params = (val, row[0])
                db(query, params)
            if val.startswith('+'):
                #print 'Fixing item '+id+' for +'
                query = "update legacy set "+col+" = %s where id = %s"
                val = val.lstrip('+')
                params = (val, row[0])
                db(query, params)
            if val == '?':
                #print 'Fixing item '+id+' for ?'
                query = "update legacy set "+col+" = null where id = %s"
                params = (row[0],)
                db(query, params)
            if val.endswith('x'):
                #print 'Fixing item '+id+' for x'
                query = "update legacy set "+col+" = %s where id = %s"
                val = val.rstrip('x')
                params = (val, row[0])
                db(query, params)
    query = "update legacy set "+col+" = null where "+col+" = ''"
    params = ''
    db(query, params)
    query = "alter table legacy alter column "+col+" type integer using ("+col+"::integer)"
    params = ''
    db(query, params)

# correct item flags and worn slots
#print 'Collecting rows from: variflags and varworn'
query = "SELECT id, variflags, varworn FROM legacy"
params = ''
rows = db(query, params)
for row in rows:
    id = str(row[0])
    if row[1] is not None:
        flags = str(row[1])
        if flags.endswith('NOBITS') or flags.startswith('NOBITS'):
            #print 'Fixing item '+id+' for nobits'
            query = "update legacy set variflags = %s where id = %s"
            flags = flags.replace('NOBITS', '')
            flags = flags.strip()
            params = (flags, row[0])
            db(query, params)
    if row[2] is not None:
        worn = str(row[2])
        if 'WHOLE-BODY' in worn:
            #print 'Fixing item '+id+' for WHOLE-*'
            worn = worn.replace('WHOLE-BODY', 'BODY')
            worn = worn.strip()
            flags = str(row[1])+' WHOLE-BODY'
            flags = flags.strip()
            query = "update legacy set variflags = %s where id = %s"
            params = (flags, row[0])
            db(query, params)
            query = "update legacy set varworn = %s where id = %s"
            params = (worn, row[0])
            db(query, params)
        elif 'WHOLE-HEAD' in worn:
            #print 'Fixing item '+id+' for WHOLE-*'
            worn = worn.replace('WHOLE-HEAD', 'HEAD')
            worn = worn.strip()
            flags = str(row[1])+' WHOLE-HEAD'
            flags = flags.strip()
            query = "update legacy set variflags = %s where id = %s"
            params = (flags, row[0])
            db(query, params)
            query = "update legacy set varworn = %s where id = %s"
            params = (worn, row[0])
            db(query, params)
        elif 'HOLD 2H' in worn:
            #print 'Fixing item '+id+' for 2H'
            worn = worn.replace('HOLD 2H', 'HOLD')
            worn = worn.strip()
            flags = str(row[1])+' TWOHANDS'
            flags = flags.strip()
            query = "update legacy set variflags = %s where id = %s"
            params = (flags, row[0])
            db(query, params)
            query = "update legacy set varworn = %s where id = %s"
            params = (worn, row[0])
            db(query, params)
        elif 'WIELD 2H' in worn:
            #print 'Fixing item '+id+' for 2H'
            worn = worn.replace('WIELD 2H', 'WIELD')
            worn = worn.strip()
            flags = str(row[1])+' TWOHANDS'
            flags = flags.strip()
            query = "update legacy set variflags = %s where id = %s"
            params = (flags, row[0])
            db(query, params)
            query = "update legacy set varworn = %s where id = %s"
            params = (worn, row[0])
            db(query, params)

# clean up zone entries
#print 'Collecting rows from: varzone'
query = "SELECT id, varzone FROM legacy"
params = ''
rows = db(query, params)
for row in rows:
    id = str(row[0])
    if row[1] is not None:
        zone = str(row[1])
        flags = ('(Q)', '(S)', '(I)', '(O)', '(R)')
        for flag in flags:
            if flag in zone:
                #print 'Fixing item '+id+' for '+flag
                query = "update legacy set varzone = %s where id = %s"
                zone = zone.replace(flag, '')
                zone = zone.strip()
                zone = zone.replace('  ', ' ')
                params = (zone, row[0])
                db(query, params)
                if flag == '(Q)':
                    col = 'from_quest'
                elif flag == '(S)':
                    col = 'from_store'
                elif flag == '(I)':
                    col = 'from_invasion'
                elif flag == '(O)':
                    col = 'out_of_game'
                elif flag == '(R)':
                    col = 'is_rare'
                query = "update legacy set "+col+" = true where id = %s"
                params = (row[0],)
                db(query, params)

# individual zone name cleanup
queries = ("update legacy set varzone = 'Halruaan Airship' where varzone = 'Airsihp';"
, "update legacy set varzone = 'Halruaan Airship' where varzone = 'Airship';"
, "update legacy set varzone = E'Amenth\\'G\\'narr' where varzone = E'Amenth\\'G\\'Narr';"
, "update legacy set varzone = 'Astral Plane' where varzone = 'Astral';"
, "update legacy set varzone = E'Baldur\\'s Gate - Silverymoon' where varzone = E'Baldur\\'s Gate, Silverymoon';"
, "update legacy set varzone = 'Brain Stem Tunnel' where varzone = 'Brainstem Tunnel';"
, "update legacy set varzone = 'Bryn Shander - Silverymoon' where varzone = 'Bryn Shander, Silverymoon';"
, "update legacy set varzone = 'City of Brass - Githyanki Fortress - Ice Castle - Citadel' where varzone = 'City of Brass, Githyanki Fortress, Ice Castle, Citadel';"
, "update legacy set varzone = 'Dread Mist' where varzone = E'Dread\\'s mist';"
, "update legacy set varzone = 'Drulak' where varzone = 'Drukal';"
, "update legacy set varzone = 'Elder Forest' where varzone = 'Eler Forest';"
, "update legacy set varzone = 'Elemental Plane of Fire' where varzone = 'Fire Plane';"
, "update legacy set varzone = 'Fortress of the Dragon Cult' where varzone = 'Fortress of the Dragon cult';"
, "update legacy set varzone = 'Fortress of the Dragon Cult' where varzone = 'Fortress if the Dragon Cult';"
, "update legacy set varzone = 'Ice Crag Castle 1' where varzone = 'Ice Crag 1';"
, "update legacy set varzone = 'Ice Crag Castle 1' where varzone = 'Ice Crag Castle';"
, "update legacy set varzone = 'Para-Elemental Plane of Ice' where varzone = 'Ice Plane';"
, "update legacy set varzone = 'Para-Elemental Plane of Ice' where varzone = 'Elemental Plane of Ice';"
, "update legacy set varzone = 'Labyrinth of No Return' where varzone = 'Labyrinth';"
, "update legacy set varzone = 'Ixarkon Prison' where varzone = 'Ixarkon Priston';"
, "update legacy set varzone = 'Jotunheim' where varzone = 'Jotenheim';"
, "update legacy set varzone = 'Keep of Finn McCumhail' where varzone = 'Keep Of Finn McCumhail';"
, "update legacy set varzone = 'Luskan Outpost' where varzone = 'Luskan';"
, "update legacy set varzone = 'Para-Elemental Plane of Magma' where varzone = 'Magma Plane';"
, "update legacy set varzone = 'Menden on the Deep' where varzone = 'Menden';"
, "update legacy set varzone = 'Mosswood Village' where varzone = 'Mosswood';"
, "update legacy set varzone = 'Nhavan Island' where varzone = 'Nhaven Island';"
, "update legacy set varzone = 'Rainbow Curtain of Ilsensine' where varzone = 'Curtain of Ilsensine';"
, "update legacy set varzone = 'Rainbow Curtain of Ilsensine' where varzone = 'Rainbow Curtain';"
, "update legacy set varzone = 'Scornubel' where varzone = 'Scornumbel';"
, "update legacy set varzone = 'Silverymoon' where varzone = 'SIlverymoon';"
, "update legacy set varzone = 'Para-Elemental Plane of Smoke' where varzone = 'Smoke';"
, "update legacy set varzone = 'Para-Elemental Plane of Smoke' where varzone = 'Smoke Plane';"
, "update legacy set varzone = 'Temple of Twisted Flesh' where varzone = 'Temple of Twiested Flesh';"
, "update legacy set varzone = 'Temple of Ghaunadaur' where varzone = 'Temple of the Eye';"
, "update legacy set varzone = 'Temple of Ghaunadaur' where varzone = 'The Temple of the Eye';"
, "update legacy set varzone = 'Trade Way, South' where varzone = 'The Trade Way, South';"
, "update legacy set varzone = 'Triterium Guildhall' where varzone = 'Triterium Castle';"
, "update legacy set varzone = 'Triterium Guildhall' where varzone = 'Triterium';"
, "update legacy set varzone = 'Trollbark Forest' where varzone = 'Trollbark Forrest';"
, "update legacy set varzone = 'Headquarters of the Twisted Rune' where varzone = 'Twisted Rune';"
, "update legacy set varzone = 'Waterdeep - Calimport' where varzone = 'Waterdeep  - Calimport';"
, "update legacy set varzone = 'Elemental Plane of Water' where varzone = 'Waterplane';"
, "update legacy set varzone = 'Elemental Plane of Water' where varzone = 'Water Plane';"
, "update legacy set varzone = 'Cursed City of West Falls' where varzone = 'West Falls';"
, "update legacy set varzone = 'Wormwrithings' where varzone = 'Worm Writhings';"
, "update legacy set varzone = 'Ruins of Yath Oloth' where varzone = 'Yath Oloth';"
, "update legacy set varzone = 'Elemental Plane of Air' where varzone = 'Air Plane';"
, "update legacy set varzone = 'Cloud Realms of Arlurrium' where varzone = 'Cloud Realms';"
, "update legacy set varzone = 'DemiPlane of Artimus Nevarlith' where varzone = 'DemiPlane';"
, "update legacy set varzone = 'Valley of Graydawn' where varzone = 'Graydawn';"
, "update legacy set varzone = 'Herd Island Chasm' where varzone = 'Herd Chasm';"
, "update legacy set varzone = 'Jungle City of Hyssk' where varzone = 'Hyssk';"
, "update legacy set varzone = 'Lost Library of the Seer Kings' where varzone = 'Seer Kings';"
, "update legacy set varzone = 'Lost Swamps of Meilech' where varzone = 'Swamps of Meilech';"
, "update legacy set varzone = 'Hive of the Manscorpions' where varzone = 'Manscorpions';"
, "update legacy set varzone = 'Temple of the Moon' where varzone = 'Moon Temple';"
, "update legacy set varzone = 'Neshkal, The Dragon Trail' where varzone = 'Neshkal';"
, "update legacy set varzone = 'Stronghold of Trahern Oakvale' where varzone = 'Oakvale';"
, "update legacy set varzone = 'Ribcage: Gate Town to Baator' where varzone = 'Ribcage';"
, "update legacy set varzone = 'Swift-Steel Mercenary Company' where varzone = 'Swift-Steel Company';"
, "update legacy set varzone = E'Tiamat\\'s Lair' where varzone = 'Tiamat';"
, "update legacy set varzone = 'Tower of Kenjin' where varzone = 'Kenjin Tower';"
, "update legacy set varzone = 'Bloodtusk Keep' where varzone = 'Bloodtusk';"
, "update legacy set varzone = 'Nine Hells: Avernus' where varzone = 'Avernus';"
, "update legacy set varzone = 'Nine Hells: Bronze Citadel' where varzone = 'Bronze Citadel';"
, "update legacy set varzone = 'Warders Guildhall' where varzone = 'Warders';"
, "update legacy set varzone = 'Shadows of Imphras Guildhall' where varzone = 'Shadows of Imphras';"
, "update legacy set varzone = 'Unknown' where varzone = '';"
, "update legacy set varzone = 'Western Realms' where varzone = 'The Wayward Inn';"
, "update legacy set varzone = 'Lurkwood' where varzone = 'Grunwald';"
, "update legacy set varzone = 'Trail to Ten Towns' where varzone = 'Trail To Ten Towns';"
, "update legacy set varzone = 'Pit of Souls' where varzone = 'Pit Of Souls';"
, "update legacy set varzone = 'Dobluth Kyor' where varzone = 'Dubloth Kyor';"
, "update legacy set varzone = 'Roleplay' where varzone = 'RP';"
, "update legacy set varzone = (select zone_abbr from zones where zone_name = varzone);"
, "update legacy set varzone = 'Common' where varzone is null;"
# preparation for import by converting to match new data fields
, "update legacy set vartype = 'ranged' where vartype = 'FIRE_WEAPON';"
, "update legacy set vartype = 'ammo' where vartype = 'MISSILE';"
, "update legacy set vartype = 'quill' where vartype = 'PEN';"
, "update legacy set vartype = 'drink' where vartype = 'LIQUID_CONT';"
, "update legacy set vartype = 'crystal' where vartype = 'PSP_CRYSTAL';"
, "update legacy set vartype = 'comp_bag' where vartype = 'COMPONENT_BAG';"
, "update legacy set vartype = 'spell_comp' where vartype = 'SPELL_COMPONENT';"
, "update legacy set vartype = lower(vartype);"
, "update legacy set vartype = 'crystal' where vartype = 'psp';"
, "update legacy set vartype = 'spellbook' where varname = 'a compendium of planar lore';"
, "update legacy set vartype = 'worn' where varname = 'an earring of favor from Deep Sashelas';"
, "update legacy set vartype = 'potion' where varname = 'an eyeball flask';"
, "update legacy set intac = null where vartype = 'worn' and intac is not null;"
, "update legacy set vartype = 'container' where varname = 'a crane-skin bag';"
, "update legacy set varholds = null where varname = 'some tattered black pants';"
, "update legacy set varholds = null where varname = 'a bushel of apples 1';"
, "update legacy set vartype = 'wand' where varname = 'a crystal rose';"
, "update legacy set varwspell = null where varname = 'a wolfsbane potion';"
, "update legacy set varwspell = 'fly' where varname = 'an amulet of the elements';"
, "update legacy set varname = 'an amulet of the elements 2' where varname = 'an amulet of the elements';"
, "update legacy set varworn = 'NOBITS' where varworn = '';"
, "update legacy set varworn = 'EARRING' where varworn = 'EAR';"
, "update legacy set (varaflags, variflags) = ('NOBITS', 'MAGIC BLESS NOBURN NOLOCATE') where varname = 'a pair of silver dragonscale leggings 2';"
, "update legacy set (varaflags, varacid) = ('NOBITS', 5) where varname = 'an enchanted opal';"
, "update legacy set variflags = 'MAGIC ANTI-EVIL NOLOCATE ANTI-EVILRACE ANTI-HUMAN ANTI-DWARF ANTI-HALFLING ANTI-GNOME ANTI-BARBARIAN ANTI-DUERGAR ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'a cloak of the elvenkind';"
, "update legacy set variflags = 'ANTI-EVIL ANTI-NEUTRAL NOBURN TWOHANDS ANTI-EVILRACE NO-CLERIC NO-THIEF NO-MAGE ANTI-WARRIOR ANTI-PALADIN ANTI-ANTIPALADIN ANTI-GREYELF ANTI-HALFELF' where varname = 'a powerful recurve bow';"
, "update legacy set variflags = 'MAGIC BLESS FLOAT NOBURN TWOHANDS NO-CLERIC NO-THIEF NO-MAGE ANTI-WARRIOR ANTI-RANGER ANTI-ANTIPALADIN ANTI-CLERIC ANTI-INVOKER ANTI-DRUID ANTI-SHAMAN ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-THIEF ANTI-ILLUSIONIST ANTI-BARD' where varname = 'a holy avenger enshrouded in light';"
, "update legacy set variflags = 'BLESS NO-CLERIC NO-MAGE ANTI-HUMAN ANTI-GREYELF ANTI-HALFELF ANTI-HALFLING ANTI-GNOME ANTI-BARBARIAN ANTI-DUERGAR ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'a double-bladed dwarvish axe of giantslaying';"
, "update legacy set variflags = 'MAGIC FLOAT NOBURN NO-MAGE ANTI-HUMAN ANTI-GREYELF ANTI-HALFELF ANTI-HALFLING ANTI-GNOME ANTI-BARBARIAN ANTI-DUERGAR ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'a fine dwarven battleaxe';"
, "update legacy set variflags = 'NOBURN NO-MAGE ANTI-ORC ANTI-GREYELF ANTI-HALFELF ANTI-HALFLING ANTI-GNOME ANTI-BARBARIAN ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'an amulet inscribed with glowing dwarven runes';"
, "update legacy set variflags = 'ANTI-GOODRACE MAGIC FLOAT NOBURN NO-CLERIC NO-THIEF NO-MAGE ANTI-ORC ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI' where varname = 'a blackened and bloodied battlehammer';"
, "update legacy set variflags = 'NOSELL ANTI-GOODRACE MAGIC ANTI-GOOD ANTI-NEUTRAL FLOAT NOBURN NO-CLERIC NO-THIEF NO-MAGE ANTI-WARRIOR' where varname = 'a warped broadsword';"
, "update legacy set variflags = 'MAGIC BLESS ANTI-EVIL FLOAT NOBURN NOLOCATE NOSLEEP NO-CLERIC NO-THIEF NO-MAGE ANTI-HUMAN ANTI-DWARF ANTI-HALFLING ANTI-GNOME ANTI-BARBARIAN ANTI-DUERGAR ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'a glittering elven scimitar';"
, "update legacy set variflags = 'MAGIC ANTI-GOOD ANTI-NEUTRAL FLOAT TWOHANDS ANTI-WARRIOR ANTI-RANGER ANTI-PALADIN ANTI-CLERIC ANTI-INVOKER ANTI-DRUID ANTI-SHAMAN ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-THIEF ANTI-ILLUSIONIST ANTI-BARD ANTI-LICH' where varname = 'an unholy avenger pulsing with blood';"
, "update legacy set variflags = 'ANTI-GOODRACE MAGIC NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-ILLUSIONIST ANTI-BARD ANTI-LICH' where varname = 'a citrine earring';"
, "update legacy set variflags = 'MAGIC BLESS ANTI-EVIL NOSUMMON ANTI-HUMAN ANTI-DWARF ANTI-HALFLING ANTI-GNOME ANTI-BARBARIAN ANTI-DUERGAR ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'a collar covered with glowing elven runes';"
, "update legacy set variflags = 'NOSELL MAGIC BLESS FLOAT NOBURN NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-PSIONICIST ANTI-ILLUSIONIST ANTI-BARD ANTI-LICH' where varname = 'a flowing granite staff of elemental domination';"
, "update legacy set variflags = 'MAGIC NOBURN NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-PSIONICIST ANTI-ILLUSIONIST ANTI-BARD ANTI-LICH' where varname = 'the bracers of elemental mastery';"
, "update legacy set variflags = 'MAGIC NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-ILLUSIONIST' where varname = 'an ancient scroll 1';"
, "update legacy set variflags = 'MAGIC NOBURN NO-MAGE ANTI-WARRIOR ANTI-RANGER ANTI-PALADIN ANTI-ANTIPALADIN ANTI-INVOKER ANTI-DRUID ANTI-SHAMAN ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-THIEF ANTI-ORC ANTI-ILLUSIONIST ANTI-BARD' where varname = 'a morning-star enshrouded in crimson flames';"
, "update legacy set variflags = 'MAGIC BLESS ANTI-GOOD ANTI-NEUTRAL NOBURN ANTI-CLERIC ANTI-INVOKER ANTI-DRUID ANTI-SHAMAN ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-THIEF ANTI-ILLUSIONIST ANTI-BARD ANTI-ILLITHID ANTI-LICH' where varname = 'the war gauntlets of conquest';"
, "update legacy set variflags = 'MAGIC ANTI-GOOD ANTI-NEUTRAL FLOAT NO-WARRIOR NO-THIEF NO-MAGE ANTI-HUMAN ANTI-GREYELF ANTI-HALFELF ANTI-DWARF ANTI-HALFLING ANTI-GNOME ANTI-DUERGAR ANTI-DROWELF ANTI-ILLITHID ANTI-YUANTI ANTI-LICH' where varname = 'a buzzard totem';"
, "update legacy set variflags = 'MAGIC FLOAT NOBURN NOLOCATE NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-ILLUSIONIST ANTI-LICH' where varname = 'a collection of dweomers and abjurations';"
, "update legacy set variflags = 'ANTI-GOODRACE FLOAT NOBURN NOLOCATE NOCHARM NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-ILLUSIONIST ANTI-BARD ANTI-LICH' where varname = 'a crystal band etched with diamonds 1';"
, "update legacy set variflags = 'MAGIC ANTI-GOOD ANTI-NEUTRAL FLOAT NOBURN NOLOCATE NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-ELEMENTALIST ANTI-ILLUSIONIST' where varname = 'a tome titled The ancient book of necromancy';"
, "update legacy set variflags = 'MAGIC NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-ILLUSIONIST ANTI-BARD' where varname = 'a devilskin robe emblazoned with skulls';"
, "update legacy set variflags = 'MAGIC ANTI-GOOD ANTI-NEUTRAL NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-PSIONICIST ANTI-ILLUSIONIST ANTI-BARD' where varname = 'a golden circlet lined with fingerbones';"
, "update legacy set variflags = 'FLOAT NO-WARRIOR NO-CLERIC NO-THIEF ANTI-ORC ANTI-DUERGAR ANTI-DROWELF ANTI-TROLL ANTI-OGRE ANTI-YUANTI ANTI-LICH ANTI-MALE ANTI-FEMALE' where varname = 'a squishy mask of giggling tentacles';"
, "update legacy set variflags = 'MAGIC FLOAT NOBURN NOLOCATE NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ILLUSIONIST ANTI-LICH' where varname = 'a compendium of planar lore';"
, "update legacy set variflags = 'MAGIC FLOAT NOBURN NOLOCATE NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-ELEMENTALIST ANTI-ILLUSIONIST' where varname = 'a tome of vile darkness';"
, "update legacy set variflags = 'GLOW FLOAT NOBURN NOLOCATE NORENT NO-WARRIOR NO-CLERIC NO-THIEF ANTI-INVOKER ANTI-ENCHANTER ANTI-NECROMANCER ANTI-ELEMENTALIST ANTI-ILLUSIONIST ANTI-BARD ANTI-LICH' where varname = 'a mindblade';"
)

params = ''
for query in queries:
    #print 'Running query: '+query
    db(query, params)

# Begin importing old data to new tables
#print 'Fill items table from legacy table'
query = "INSERT INTO items (item_name, keywords, weight, c_value, item_type, from_zone, for_quest, \
no_identify, is_rare, from_store, from_quest, from_invasion, out_of_game, last_id) \
SELECT varname, varkeywords, varwt, varvalue, vartype, varzone, varquest, varnoid, is_rare, \
from_store, from_quest, from_invasion, out_of_game, vardate \
FROM legacy;"
params = ''
db(query, params)

# populate item_specials, for the most part
abrs = ('pages', 'ac', 'psp', 'holds', 'level', \
'apps', 'level', 'charges', \
'stutter', 'quality', 'min_level', \
'dice', 'class', 'crit', 'multi', \
'type', 'type')
vals = ('varpages', 'intac', 'varpsp', 'varholds', 'varlevel', \
'varapplications', 'varwlevel', 'varmaxcharge', \
'varstutter', 'varquality', 'varmin', \
'vardice', 'varwclass', 'varcrange', 'varcbonus', \
'varpoison', 'varwtype')
for x in xrange(0, len(vals)):
    #print 'Inserting specials for '+abrs[x]+' / '+vals[x]
    query = "INSERT INTO item_specials \
    (item_id, item_type, spec_abbr, spec_value) \
    (SELECT item_id, vartype, '"+abrs[x]+"', "+vals[x]+" \
    FROM items, legacy WHERE item_name IN \
    (SELECT varname FROM legacy WHERE "+vals[x]+" IS NOT NULL) \
    AND item_name = varname)"
    params = ''
    db(query, params)

# finish item_specials: spell / varwspell
query = "SELECT item_id, vartype, 'spell', varwspell \
FROM items, legacy WHERE item_name IN \
(SELECT varname FROM legacy WHERE varwspell IS NOT NULL) \
AND item_name = varname"
paramy = ''
rows = db(query, params)
rows2 = []
for x in xrange(0, len(rows)):
    if '-' in rows[x][3]:
        spells = rows[x][3].split('-')
        for y in xrange(0, len(spells)):
            num = 'spell'+str(y+1)
            spell = spells[y].strip()
            row = (rows[x][0], rows[x][1], num, spell)
            rows2.append(row)
    elif rows[x][1] == 'potion' or rows[x][1] == 'scroll':
        num = 'spell1'
        row = (rows[x][0], rows[x][1], num, rows[x][3])
        rows2.append(row)
    else:
        row = (rows[x][0], rows[x][1], rows[x][2], rows[x][3])
        rows2.append(row)

for row in rows2:
    query = "INSERT INTO item_specials \
    (item_id, item_type, spec_abbr, spec_value) \
    VALUES(%s, %s, %s, %s)"
    params = (row[0], row[1], row[2], row[3])
    db(query, params)

# populate item_attribs w/ 44 attribs, all integer
cols = ('vararmor', 'varhp', 'inthit', 'intdam', \
'varspell', 'varbreath', 'varpara', 'varpetri', 'varrod', \
'varstr', 'varagi', 'vardex', 'varcon', \
'varpow', 'varint', 'varwis', 'varcha', \
'varmaxstr', 'varmaxagi', 'varmaxdex', 'varmaxcon', \
'varmaxpow', 'varmaxint', 'varmaxwis', 'varmaxcha', \
'varluck', 'varkarma', 'varmana', 'varmove', \
'varage', 'varweight', 'varheight', 'varmr', \
'varsfele', 'varsfenc', 'varsfheal', 'varsfill', \
'varsfinv', 'varsfnature', 'varsfnec', 'varsfprot', \
'varsfspirit', 'varsfsum', 'varsftele')

attribs = ('armor', 'hp', 'hit', 'dam', \
'svsp', 'svbr', 'svpar', 'svpet', 'svrod', \
'str', 'agi', 'dex', 'con', \
'pow', 'int', 'wis', 'cha', \
'maxstr', 'maxagi', 'maxdex', 'maxcon', \
'maxpow', 'maxint', 'maxwis', 'maxcha', \
'luck', 'karma', 'mana', 'mv', \
'age', 'wt', 'ht', 'MR', \
'sf_elem', 'sf_ench', 'sf_heal', 'sf_illu', \
'sf_invo', 'sf_nat', 'sf_nec', 'sf_prot', \
'sf_spir', 'sf_sum', 'sf_tele')

for x in xrange(0, len(cols)):
    col = cols[x]
    att = attribs[x]
    query = "SELECT item_id, "+col+" \
    FROM items, legacy \
    WHERE varname = item_name \
    AND "+col+" IS NOT NULL"
    params = ''
    rows = db(query, params)
    for row in rows:
        query = "INSERT INTO item_attribs VALUES(%s, %s, %s)"
        params = (row[0], att, row[1])
        db(query, params)


# populate item_resists
cols = ('varunarmd', 'varslash', 'varbludgn', 'varpierce', \
'varrange', 'varspells', 'varsonic', 'varpos', 'varneg', \
'varpsi', 'varmental', 'vargoods', 'varevils', \
'varlaw', 'varchaos', 'varforce', \
'varfire', 'varcold', 'varelect', 'varacid', 'varpois')

resists = ('unarm', 'slas', 'blud', 'pier', \
'rang', 'spells', 'sonic', 'pos', 'neg', \
'psion', 'mental', 'good', 'evil', \
'law', 'chaos', 'force', \
'fire', 'cold', 'elect', 'acid', 'pois')

for x in xrange(0, len(cols)):
    col = cols[x]
    res = resists[x]
    query = "SELECT item_id, "+col+" \
    FROM items, legacy \
    WHERE varname = item_name \
    AND "+col+" IS NOT NULL"
    params = ''
    rows = db(query, params)
    for row in rows:
        query = "INSERT INTO item_resists VALUES(%s, %s, %s)"
        params = (row[0], res, row[1])
        db(query, params)

# populate item_slots from varworn
query = "SELECT item_id, varworn FROM items, legacy WHERE item_name = varname"
params = ''
rows = db(query, params)
for row in rows:
    slots = row[1].split()
    for slot in slots:
        query = "SELECT slot_abbr FROM slots WHERE worn_slot = %s"
        params = (slot,)
        abbr = db(query, params)
        if len(abbr) == 0:
            print 'Slot name wrong for item: '+str(row[0])
        else:
            query = "INSERT INTO item_slots VALUES(%s, %s)"
            params = (row[0], abbr[0])
            db(query, params)

# populate item_effects from varaflags
query = "SELECT item_id, varaflags FROM items, legacy WHERE item_name = varname \
AND varaflags != %s"
params = ('NOBITS',)
rows = db(query, params)
for row in rows:
    effects = row[1].split()
    for effect in effects:
        query = "SELECT effect_abbr FROM effects WHERE effect_name = %s"
        params = (effect,)
        abbr = db(query, params)
        if len(abbr) == 0:
            print 'Effect name wrong for item: '+str(row[0])
        else:
            query = "INSERT INTO item_effects VALUES(%s, %s)"
            params = (row[0], abbr[0])
            db(query, params)

# populate item_flags, item_restricts from variflags
query = "SELECT flag_name FROM flags"
params = ''
flags = db(query, params)
query = "SELECT restrict_name FROM restricts"
params = ''
restricts = db(query, params)
query = "SELECT item_id, variflags FROM items, legacy WHERE item_name = varname \
AND variflags != ''"
params = ''
rows = db(query, params)
for row in rows:
    iflags = row[1].split()
    for iflag in iflags:
        abbr = ''
        for flag in flags:
            if iflag in flag:
                query = "SELECT flag_abbr FROM flags WHERE flag_name = %s"
                params = (iflag,)
                abbr = db(query, params)
                query = "INSERT INTO item_flags VALUES(%s, %s)"
                params = (row[0], abbr[0])
                db(query, params)
        for restrict in restricts:
            if iflag in restrict:
                query = "SELECT restrict_abbr FROM restricts WHERE restrict_name = %s"
                params = (iflag,)
                abbr = db(query, params)
                query = "INSERT INTO item_restricts VALUES(%s, %s)"
                params = (row[0], abbr[0])
                db(query, params)
        if abbr == '':
            print 'Variflags wrong for item: '+str(row[0])

# populate item_enchants from varenchant
queries = ("update legacy set varenchant = 'Frost 100 100 0 0' where varname = 'a dormant elven longsword shrouded in frost';"
, "update legacy set varenchant = 'Holy 100 100 0 0 - Bane 100 100 0 0 - Holy Burst 100 100 0 0 - Force 100 100 0 0' where varname = 'an eerily glowing trident';"
, "update legacy set varenchant = 'Sonic Burst 100 100 0 0 - Thundering 100 100 -10 32 - Force 100 100 -10 32' where varname = 'an astral-forged force whip';"
, "update legacy set varenchant = 'Keen 100 100 0 0 - Vampiric 100 100 0 0' where varname = 'a mindblade';"
, "update legacy set varenchant = 'Holy 100 100 0 0 - Ghost Touch 100 100 0 0' where varname = 'a ghostly bladed gauntlet wreathed in holy light';"
, "update legacy set varenchant = 'Acid Burst 100 100 0 0 - Unholy 100 100 0 0 - Vampiric 100 100 0 0' where varname = 'a vile onyx greatsword of life-stealing';"
, "update legacy set varenchant = 'Sonic 100 100 0 0 - Shocking Burst 100 100 0 0' where varname = 'a pair of screaming nunchaku crackling with electricity';"
, "update legacy set varenchant = 'Shocking 100 100 0 0 - Shocking Burst 100 100 0 0' where varname = 'an infernal whip of lightning';"
, "update legacy set varenchant = 'Keen 100 100 0 0 - Vampiric 75 100 -25 0' where varname = 'a runed adamantine longsword';"
, "update legacy set varenchant = 'Sonic 200 100 0 0 - Sonic Burst 200 100 0 0 - Force 100 75 0 3' where varname = 'a concussive warmaul of the dwarven kings';"
, "update legacy set varenchant = 'Holy 100 100 0 0' where varname = 'a sacred dwarven axe';"
, "update legacy set varenchant = 'Acidic 100 100 0 0 - Acid Burst 100 100 0 0' where varname = 'a vicious looking dagger with a spider shaped pommel';"
# these two are guesses!
, "update legacy set varenchant = 'Anarchic 100 100 0 0 - Bane 100 100 0 0 - Keen 100 100 0 0 - Anarchic Burst 100 100 0 0' where varname = 'an ornate githyanki dagger';"
, "update legacy set varenchant = 'Flaming 100 100 0 0 - Flaming Burst 100 100 0 0 - Unholy 100 100 0 0' where varname = 'an unholy war scythe wreathed in flames';"
, "update legacy set vareffects = 'Animate Random Undead - Life Drain - Greater Thought' where varname = 'a dagger of oblivion';"
, "update legacy set varcres = 'Necromancer Only' where varname = 'a dagger of oblivion';"
, "update legacy set vareffects = 'Flamestrike - Tick Damage' where varname = 'a gleaming red greatsword';"
, "update legacy set varceffects = E'\\'Ches\\' Haste 1/6 hours' where varname = 'a mithril stiletto with an aquamarine hilt';"
, "update legacy set varceffects = E'\\'Weak fuels the Strong\\' 1/day' where varname = 'a demonic crown of immortality';"
, "update legacy set varceffects = E'\\'Dragonpoison\\' effect: poison, 1 charge - \\'Dragonslow\\' effect: slow, 2 charge - \\'Dragonblind\\' effect: blind, 3 charge - \\'Dragonstrike\\' effect: instant kill, 5 charge' where varname = 'the infernal stiletto of bane';"
, "update items set item_type = 'trash' where item_name = 'a stone crucible';"
)

params = ''
for query in queries:
    db(query, params)

query = "SELECT item_id, varenchant FROM items, legacy WHERE item_name = varname AND varenchant IS NOT NULL"
params = ''
rows = db(query, params)
for row in rows:
    enchs = row[1].split(' - ')
    for ench in enchs:
        ench = ench.strip()
        ench = ench.replace('%', '')
        ench = ench.rsplit(' ', 4)
        #print str(row[0])+', '+str(ench)
        query = "INSERT INTO item_enchants VALUES(%s, %s, %s, %s, %s, %s)"
        params = (row[0], ench[0], ench[1], ench[2], ench[3], ench[4])
        db(query, params)

# populate item_procs
query = "SELECT item_id, varcrit FROM items, legacy WHERE varname = item_name AND varcrit != '';"
params = ''
rows = db(query, params)
for row in rows:
    procs = row[1].split(' - ')
    for proc in procs:
        proc = proc.strip()
        query = "INSERT INTO item_procs VALUES(%s, %s, %s, %s, %s, %s)"
        params = (row[0], proc, 'Crit', '', 'Critical Hit', '')
        db(query, params)

query = "SELECT item_id, vareffects FROM items, legacy WHERE varname = item_name AND vareffects != '';"
params = ''
rows = db(query, params)
for row in rows:
    procs = row[1].split(' - ')
    for proc in procs:
        proc = proc.strip()
        query = "INSERT INTO item_procs VALUES(%s, %s, %s, %s, %s, %s)"
        params = (row[0], proc, '', '', '', '')
        db(query, params)

query = "SELECT item_id, varceffects FROM items, legacy WHERE varname = item_name AND varceffects != '';"
params = ''
rows = db(query, params)
for row in rows:
    procs = row[1].split(' - ')
    for proc in procs:
        proc = proc.strip()
        query = "INSERT INTO item_procs VALUES(%s, %s, %s, %s, %s, %s)"
        params = (row[0], proc, '', '', '', '')
        db(query, params)


timediff = datetime.now() - timestart
print 'The script took '+str(timediff)

if conn:
    conn.close()
