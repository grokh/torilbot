-- create new character tracking tables and populate with base data
CREATE TABLE race_types(
	race_type varchar(20) PRIMARY KEY
	,anti_flag varchar(20)
);
INSERT INTO race_types VALUES('Good', 'ANTI-GOODRACE');
INSERT INTO race_types VALUES('Evil', 'ANTI-EVILRACE');
INSERT INTO race_types VALUES('Neutral', '');
CREATE TABLE races(
	race_name varchar(20) PRIMARY KEY
	,race_abbr varchar(10)
	,anti_flag varchar(20)
	,race_type varchar(20) REFERENCES race_types(race_type)
);
INSERT INTO races VALUES('Human', 'Human', 'ANTI-HUMAN', 'Good');
INSERT INTO races VALUES('Barbarian', 'Barb', 'ANTI-BARBARIAN', 'Good');
INSERT INTO races VALUES('Drow Elf', 'Drow', 'ANTI-DROWELF', 'Evil');
INSERT INTO races VALUES('Moon Elf', 'Elf', 'ANTI-GREYELF', 'Good');
INSERT INTO races VALUES('Half-Elf', 'Helf', 'ANTI-HALFELF', 'Good');
INSERT INTO races VALUES('Shield Dwarf', 'Dwarf', 'ANTI-DWARF', 'Good');
INSERT INTO races VALUES('Half-Orc', 'Horc', 'ANTI-HALFORC', 'Neutral');
INSERT INTO races VALUES('Duergar', 'Duergar', 'ANTI-DUERGAR', 'Evil');
INSERT INTO races VALUES('Gnome', 'Gnome', 'ANTI-GNOME', 'Good');
INSERT INTO races VALUES('Halfling', 'Halfling', 'ANTI-HALFLING', 'Good');
INSERT INTO races VALUES('Ogre', 'Ogre', 'ANTI-OGRE', 'Evil');
INSERT INTO races VALUES('Troll', 'Troll', 'ANTI-TROLL', 'Evil');
INSERT INTO races VALUES('Illithid', 'Squid', 'ANTI-ILLITHID', 'Evil');
INSERT INTO races VALUES('Orc', 'Orc', 'ANTI-ORC', 'Evil');
INSERT INTO races VALUES('Yuan-Ti', 'Yuan', 'ANTI-YUANTI', 'Evil');
CREATE TABLE class_types(
	class_type varchar(10) PRIMARY KEY
	,anti_flag varchar(20)
);
INSERT INTO class_types VALUES('Fighter', 'NO-WARRIOR');
INSERT INTO class_types VALUES('Priest', 'NO-CLERIC');
INSERT INTO class_types VALUES('Rogue', 'NO-THIEF');
INSERT INTO class_types VALUES('Mage', 'NO-MAGE');
CREATE TABLE classes(
	class_name varchar(30) PRIMARY KEY
	,class_abbr varchar(3)
	,class_type varchar(10) REFERENCES class_types(class_type)
	,anti_flag varchar(20)
);
CREATE INDEX idx_lowclass_name ON classes (LOWER(class_name));
INSERT INTO classes VALUES('Warrior', 'War', 'Fighter', 'ANTI-WARRIOR');
INSERT INTO classes VALUES('Ranger', 'Ran', 'Fighter', 'ANTI-RANGER');
INSERT INTO classes VALUES('Paladin', 'Pal', 'Fighter', 'ANTI-PALADIN');
INSERT INTO classes VALUES('Anti-Paladin', 'A-P', 'Fighter', 'ANTI-ANTIPALADIN');
INSERT INTO classes VALUES('Dire Raider', 'Dir', 'Fighter', 'ANTI-DIRERAIDER');
INSERT INTO classes VALUES('Cleric', 'Cle', 'Priest', 'ANTI-CLERIC');
INSERT INTO classes VALUES('Druid', 'Dru', 'Priest', 'ANTI-DRUID');
INSERT INTO classes VALUES('Shaman', 'Sha', 'Priest', 'ANTI-SHAMAN');
INSERT INTO classes VALUES('Rogue', 'Rog', 'Rogue', 'ANTI-ROGUE');
INSERT INTO classes VALUES('Bard', 'Bar', 'Rogue', 'ANTI-BARD');
INSERT INTO classes VALUES('Battlechanter', 'Ctr', 'Rogue', 'ANTI-BARD');
INSERT INTO classes VALUES('Enchanter', 'Enc', 'Mage', 'ANTI-ENCHANTER');
INSERT INTO classes VALUES('Invoker', 'Inv', 'Mage', 'ANTI-INVOKER');
INSERT INTO classes VALUES('Elementalist', 'Ele', 'Mage', 'ANTI-ELEMENTALIST');
INSERT INTO classes VALUES('Necromancer', 'Nec', 'Mage', 'ANTI-NECROMANCER');
INSERT INTO classes VALUES('Illusionist', 'Ill', 'Mage', 'ANTI-ILLUSIONIST');
INSERT INTO classes VALUES('Psionicist', 'Psi', 'Mage', 'ANTI-PSIONICIST');
INSERT INTO classes VALUES('Lich', 'Lic', 'Mage', 'ANTI-LICH');
CREATE TABLE accounts(
	account_name varchar(30) PRIMARY KEY
	,player_name varchar(30)
);
CREATE TABLE chars(
	account_name varchar(30) REFERENCES accounts(account_name)
	,char_name varchar(30)
	,class_name varchar(30) REFERENCES classes(class_name)
	,char_race varchar(20) REFERENCES races(race_name)
	,char_level integer
	,last_seen timestamp
	,vis boolean
	,PRIMARY KEY (account_name, char_name)
);
CREATE INDEX idx_chars_name ON chars (LOWER(char_name));


-- create new boot/load report tables and populate with base data
CREATE TABLE boots(
	boot_id serial PRIMARY KEY
	,boot_time timestamp NOT NULL
	,uptime varchar(10) NOT NULL
);
INSERT INTO boots (boot_time, uptime) VALUES(CURRENT_TIMESTAMP - interval '00:35:00', '0:34:10');
CREATE TABLE loads(
	boot_id integer REFERENCES boots(boot_id) NOT NULL
	,report_time timestamp NOT NULL
	,report_text varchar(320) NOT NULL
	,char_name varchar(30) NOT NULL
	,deleted boolean NOT NULL
	,PRIMARY KEY (boot_id, report_time)
);


-- create new item stat tables and populate with base data
CREATE TABLE enchants(
	ench_name varchar(25) PRIMARY KEY
	,ench_desc varchar(100)
);
INSERT INTO enchants VALUES('Flaming', '+2d4 fire damage per hit');
INSERT INTO enchants VALUES('Flaming Burst', '(+5d10 * crit mod of weapon) fire damage on critical hit');
INSERT INTO enchants VALUES('Shocking', '+2d4 electricity damage per hit');
INSERT INTO enchants VALUES('Shocking Burst', '(+5d10 * crit mod of weapon) electricity damage on critical hit');
INSERT INTO enchants VALUES('Acidic', '+2d4 acid damage per hit');
INSERT INTO enchants VALUES('Acid Burst', '(+5d10 * crit mod of weapon) acid damage on critical hit');
INSERT INTO enchants VALUES('Sonic', '+2d4 sonic damage per hit');
INSERT INTO enchants VALUES('Sonic Burst', '(+5d10 * crit mod of weapon) sonic damage on critical hit');
INSERT INTO enchants VALUES('Frost', '+2d4 cold damage per hit');
INSERT INTO enchants VALUES('Icy Burst', '(+5d10 * crit mod of weapon) cold damage on critical hit');
INSERT INTO enchants VALUES('Anarchic', '+3d5 chaotic damage per hit vs. lawful align');
INSERT INTO enchants VALUES('Anarchic Burst', '(+10d10 * crit mod of weapon) chaotic damage per hit vs. lawful align on critical hit');
INSERT INTO enchants VALUES('Axiomatic', '+3d5 lawful damage per hit vs. chaotic align');
INSERT INTO enchants VALUES('Axiomatic Burst', '(+10d10 * crit mod of weapon) lawful damage per hit vs. chaotic align on critical hit');
INSERT INTO enchants VALUES('Unholy', '+3d5 unholy damage per hit vs. good align');
INSERT INTO enchants VALUES('Unholy Burst', '(+10d10 * crit mod of weapon) unholy damage per hit vs. good align on critical hit');
INSERT INTO enchants VALUES('Holy', '+3d5 holy damage per hit vs. evil align');
INSERT INTO enchants VALUES('Holy Burst', '(+10d10 * crit mod of weapon) holy damage per hit vs. evil align on critical hit');
INSERT INTO enchants VALUES('Force', 'Chance to bash');
INSERT INTO enchants VALUES('Thundering', 'Chance to stun');
INSERT INTO enchants VALUES('Ghost Touch', 'Halves the negative modifier to damage on wraithform NPCs.');
INSERT INTO enchants VALUES('Vampiric', '+3d4 and chance to heal back part of that on hit. Save vs. CON negates damage and heal.');
INSERT INTO enchants VALUES('Bane', '+4d5 damage vs. one specified race, per hit.');
INSERT INTO enchants VALUES('Keen', 'Double the critical hit range of the weapon.');
INSERT INTO enchants VALUES('Brilliant', 'Blindness');
CREATE TABLE attribs(
	attrib_abbr varchar(10) PRIMARY KEY
	,attrib_name varchar(25)
	,attrib_display varchar(25)
);
INSERT INTO attribs VALUES('armor', 'ARMOR', 'Armor');
INSERT INTO attribs VALUES('hit', 'HITROLL', 'Hitroll');
INSERT INTO attribs VALUES('dam', 'DAMROLL', 'Damroll');
INSERT INTO attribs VALUES('hp', 'HITPOINTS', 'Hitpoints');
INSERT INTO attribs VALUES('mv', 'MOVE', 'Movement');
INSERT INTO attribs VALUES('mana', 'MANA', 'Mana');
INSERT INTO attribs VALUES('svsp', 'SV_SPELL', 'Save Spell');
INSERT INTO attribs VALUES('svbr', 'SV_BREATH', 'Save Breath');
INSERT INTO attribs VALUES('svpar', 'SV_PARA', 'Save Paralysis');
INSERT INTO attribs VALUES('svpet', 'SV_PETRI', 'Save Petrification');
INSERT INTO attribs VALUES('svrod', 'SV_ROD', 'Save Rod');
INSERT INTO attribs VALUES('maxstr', 'STR_MAX', 'Max Strength');
INSERT INTO attribs VALUES('maxagi', 'AGI_MAX', 'Max Agility');
INSERT INTO attribs VALUES('maxdex', 'DEX_MAX', 'Max Dexterity');
INSERT INTO attribs VALUES('maxcon', 'CON_MAX', 'Max Constitution');
INSERT INTO attribs VALUES('maxpow', 'POW_MAX', 'Max Power');
INSERT INTO attribs VALUES('maxint', 'INT_MAX', 'Max Intelligence');
INSERT INTO attribs VALUES('maxwis', 'WIS_MAX', 'Max Wisdom');
INSERT INTO attribs VALUES('maxcha', 'CHA_MAX', 'Max Charisma');
INSERT INTO attribs VALUES('str', 'STR', 'Strength');
INSERT INTO attribs VALUES('agi', 'AGI', 'Agility');
INSERT INTO attribs VALUES('dex', 'DEX', 'Dexterity');
INSERT INTO attribs VALUES('con', 'CON', 'Constitution');
INSERT INTO attribs VALUES('pow', 'POW', 'Power');
INSERT INTO attribs VALUES('int', 'INT', 'Intelligence');
INSERT INTO attribs VALUES('wis', 'WIS', 'Wisdom');
INSERT INTO attribs VALUES('cha', 'CHA', 'Charisma');
INSERT INTO attribs VALUES('MR', 'MAGIC_RESIST', 'Magic Resistance');
INSERT INTO attribs VALUES('age', 'AGE', 'Age');
INSERT INTO attribs VALUES('wt', 'WEIGHT', 'Weight');
INSERT INTO attribs VALUES('ht', 'HEIGHT', 'Height');
INSERT INTO attribs VALUES('luck', 'LUCK', 'Luck');
INSERT INTO attribs VALUES('karma', 'KARMA', 'Karma');
INSERT INTO attribs VALUES('sf_elem', 'SPELL_FOCUS_ELEMENTAL', 'Spell Focus Elemental');
INSERT INTO attribs VALUES('sf_ench', 'SPELL_FOCUS_ENCHANTMENT', 'Spell Focus Enchantment');
INSERT INTO attribs VALUES('sf_heal', 'SPELL_FOCUS_HEALING', 'Spell Focus Healing');
INSERT INTO attribs VALUES('sf_illu', 'SPELL_FOCUS_ILLUSION', 'Spell Focus Illusion');
INSERT INTO attribs VALUES('sf_invo', 'SPELL_FOCUS_INVOCATION', 'Spell Focus Invocation');
INSERT INTO attribs VALUES('sf_nat', 'SPELL_FOCUS_NATURE', 'Spell Focus Nature');
INSERT INTO attribs VALUES('sf_nec', 'SPELL_FOCUS_NECROMANCY', 'Spell Focus Necromancy');
INSERT INTO attribs VALUES('sf_prot', 'SPELL_FOCUS_PROTECTION', 'Spell Focus Protection');
INSERT INTO attribs VALUES('sf_spir', 'SPELL_FOCUS_SPIRIT', 'Spell Focus Spirit');
INSERT INTO attribs VALUES('sf_sum', 'SPELL_FOCUS_SUMMONING', 'Spell Focus Summoning');
INSERT INTO attribs VALUES('sf_tele', 'SPELL_FOCUS_TELEPORTATION', 'Spell Focus Teleportation');
CREATE TABLE effects(
	effect_abbr varchar(10) PRIMARY KEY
	,effect_name varchar(25)
	,effect_display varchar(25)
);
INSERT INTO effects VALUES('pr_evil', 'PR-EVIL', 'Protection From Evil');
INSERT INTO effects VALUES('pr_good', 'PR-GOOD', 'Protection From Good');
INSERT INTO effects VALUES('dm', 'DET-MAGIC', 'Detect Magic');
INSERT INTO effects VALUES('di', 'DET-INVIS', 'Detect Invisibility');
INSERT INTO effects VALUES('det_evil', 'DET-EVIL', 'Detect Evil');
INSERT INTO effects VALUES('det_good', 'DET-GOOD', 'Detect Good');
INSERT INTO effects VALUES('infra', 'INFRA', 'Infravision');
INSERT INTO effects VALUES('sense', 'SENSE-LIFE', 'Sense Life');
INSERT INTO effects VALUES('fly', 'FLY', 'Fly');
INSERT INTO effects VALUES('lev', 'LEVITATE', 'Levitate');
INSERT INTO effects VALUES('farsee', 'FARSEE', ' Farsee');
INSERT INTO effects VALUES('slow_poi', 'SLOW-POISON', 'Slow Poison');
INSERT INTO effects VALUES('haste', 'HASTE', 'Haste');
INSERT INTO effects VALUES('sneak', 'SNEAK', 'Sneak');
INSERT INTO effects VALUES('wb', 'WATERBREATH', 'Water Breathing');
INSERT INTO effects VALUES('aware', 'AWARE', 'Awareness');
INSERT INTO effects VALUES('min_globe', 'MIN-GLOBE', 'Minor Globe');
INSERT INTO effects VALUES('mis_shield', 'MSL-SHLD', 'Missile Shield');
INSERT INTO effects VALUES('blind', 'BLINDNESS', 'Blindness');
INSERT INTO effects VALUES('slow', 'SLOW', 'Slowness');
INSERT INTO effects VALUES('ultra', 'ULTRA', 'Ultravision');
CREATE TABLE resists(
	resist_abbr varchar(10) PRIMARY KEY
	,resist_name varchar(25)
	,resist_display varchar(25)
);
INSERT INTO resists VALUES('fire', 'Fire', 'Fire');
INSERT INTO resists VALUES('cold', 'Cold', 'Cold');
INSERT INTO resists VALUES('acid', 'Acid', 'Acid');
INSERT INTO resists VALUES('pois', 'Poison', 'Poison');
INSERT INTO resists VALUES('elect', 'Elect', 'Electricity');
INSERT INTO resists VALUES('spells', 'Spells', 'Spells');
INSERT INTO resists VALUES('rang', 'Range', 'Ranged');
INSERT INTO resists VALUES('pier', 'Pierce', 'Pierce');
INSERT INTO resists VALUES('blud', 'Bludgn', 'Bludgeon');
INSERT INTO resists VALUES('slas', 'Slash', 'Slash');
INSERT INTO resists VALUES('unarm', 'Unarmd', 'Unarmed');
INSERT INTO resists VALUES('force', 'Force', 'Force');
INSERT INTO resists VALUES('chaos', 'Chaos', 'Chaos');
INSERT INTO resists VALUES('law', 'Law', 'Law');
INSERT INTO resists VALUES('evil', 'Evils', 'Evil');
INSERT INTO resists VALUES('good', 'Goods', 'Good');
INSERT INTO resists VALUES('mental', 'Mental', 'Mental');
INSERT INTO resists VALUES('psion', 'Psi', 'Psionic');
INSERT INTO resists VALUES('neg', 'Neg', 'Negative');
INSERT INTO resists VALUES('pos', 'Pos', 'Positive');
INSERT INTO resists VALUES('sonic', 'Sonic', 'Sonic');
CREATE TABLE restricts(
	restrict_abbr varchar(10) PRIMARY KEY
	,restrict_name varchar(25)
);
INSERT INTO restricts VALUES('!goodrace', 'ANTI-GOODRACE');
INSERT INTO restricts VALUES('!evilrace', 'ANTI-EVILRACE');
INSERT INTO restricts VALUES('!fighter', 'NO-WARRIOR');
INSERT INTO restricts VALUES('!thief', 'NO-THIEF');
INSERT INTO restricts VALUES('!priest', 'NO-CLERIC');
INSERT INTO restricts VALUES('!mage', 'NO-MAGE');
INSERT INTO restricts VALUES('!good', 'ANTI-GOOD');
INSERT INTO restricts VALUES('!neut', 'ANTI-NEUTRAL');
INSERT INTO restricts VALUES('!evil', 'ANTI-EVIL');
INSERT INTO restricts VALUES('!male', 'ANTI-MALE');
INSERT INTO restricts VALUES('!female', 'ANTI-FEMALE');
INSERT INTO restricts VALUES('!duergar', 'ANTI-DUERGAR');
INSERT INTO restricts VALUES('!drow', 'ANTI-DROWELF');
INSERT INTO restricts VALUES('!human', 'ANTI-HUMAN');
INSERT INTO restricts VALUES('!halfelf', 'ANTI-HALFELF');
INSERT INTO restricts VALUES('!dwarf', 'ANTI-DWARF');
INSERT INTO restricts VALUES('!halfling', 'ANTI-HALFLING');
INSERT INTO restricts VALUES('!gnome', 'ANTI-GNOME');
INSERT INTO restricts VALUES('!squid', 'ANTI-ILLITHID');
INSERT INTO restricts VALUES('!yuan', 'ANTI-YUANTI');
INSERT INTO restricts VALUES('!elf', 'ANTI-GREYELF');
INSERT INTO restricts VALUES('!barb', 'ANTI-BARBARIAN');
INSERT INTO restricts VALUES('!troll', 'ANTI-TROLL');
INSERT INTO restricts VALUES('!ogre', 'ANTI-OGRE');
INSERT INTO restricts VALUES('!orc', 'ANTI-ORC');
INSERT INTO restricts VALUES('!horc', 'ANTI-HALFORC');
INSERT INTO restricts VALUES('!warr', 'ANTI-WARRIOR');
INSERT INTO restricts VALUES('!rang', 'ANTI-RANGER');
INSERT INTO restricts VALUES('!pal', 'ANTI-PALADIN');
INSERT INTO restricts VALUES('!ap', 'ANTI-ANTIPALADIN');
INSERT INTO restricts VALUES('!dire', 'ANTI-DIRERAIDER?');
INSERT INTO restricts VALUES('!cleric', 'ANTI-CLERIC');
INSERT INTO restricts VALUES('!druid', 'ANTI-DRUID');
INSERT INTO restricts VALUES('!sham', 'ANTI-SHAMAN');
INSERT INTO restricts VALUES('!rogue', 'ANTI-THIEF');
INSERT INTO restricts VALUES('!bard', 'ANTI-BARD');
INSERT INTO restricts VALUES('!bchant', 'ANTI-BATTLECHANTER?');
INSERT INTO restricts VALUES('!ench', 'ANTI-ENCHANTER');
INSERT INTO restricts VALUES('!invo', 'ANTI-INVOKER');
INSERT INTO restricts VALUES('!elem', 'ANTI-ELEMENTALIST');
INSERT INTO restricts VALUES('!necro', 'ANTI-NECROMANCER');
INSERT INTO restricts VALUES('!illus', 'ANTI-ILLUSIONIST');
INSERT INTO restricts VALUES('!psi', 'ANTI-PSIONICIST');
INSERT INTO restricts VALUES('!lich', 'ANTI-LICH');
CREATE TABLE flags(
	flag_abbr varchar(10) PRIMARY KEY
	,flag_name varchar(25)
	,flag_display varchar(25)
);
INSERT INTO flags VALUES('no_sum', 'NOSUMMON', 'No Summon');
INSERT INTO flags VALUES('no_sleep', 'NOSLEEP', 'No Sleep');
INSERT INTO flags VALUES('no_charm', 'NOCHARM', 'No Charm');
INSERT INTO flags VALUES('no_burn', 'NOBURN', 'No Burn');
INSERT INTO flags VALUES('no_drop', 'NODROP', 'No Drop');
INSERT INTO flags VALUES('two_hand', 'TWOHANDS', 'Two Handed');
INSERT INTO flags VALUES('lit', 'LIT', 'Lit');
INSERT INTO flags VALUES('invis', 'INVISIBLE', 'Invisible');
INSERT INTO flags VALUES('float', 'FLOAT', 'Float');
INSERT INTO flags VALUES('no_loc', 'NOLOCATE', 'No Locate');
INSERT INTO flags VALUES('no_sell', 'NOSELL', 'No Sell');
INSERT INTO flags VALUES('transient', 'TRANSIENT', 'Transient');
INSERT INTO flags VALUES('magic', 'MAGIC', 'Magic');
INSERT INTO flags VALUES('bless', 'BLESS', 'Bless');
INSERT INTO flags VALUES('hidden', 'SECRET', 'Hidden');
INSERT INTO flags VALUES('no_rent', 'NORENT', 'No Rent');
INSERT INTO flags VALUES('glow', 'GLOW', 'Glowing');
INSERT INTO flags VALUES('dark', 'DARK', 'Dark');
INSERT INTO flags VALUES('no_take', 'NOTAKE', 'No Take');
INSERT INTO flags VALUES('whole_head', 'WHOLE-HEAD', 'Whole Head');
INSERT INTO flags VALUES('whole_body', 'WHOLE-BODY', 'Whole Body');
CREATE TABLE slots(
	slot_abbr varchar(10) PRIMARY KEY
	,worn_slot varchar(25)
	,slot_display varchar(25)
);
INSERT INTO slots VALUES('head', 'HEAD', 'Head');
INSERT INTO slots VALUES('eyes', 'EYES', 'Eyes');
INSERT INTO slots VALUES('ear', 'EARRING', 'Ear');
INSERT INTO slots VALUES('face', 'FACE', 'Face');
INSERT INTO slots VALUES('neck', 'NECK', 'Neck');
INSERT INTO slots VALUES('on_body', 'BODY', 'On Body');
INSERT INTO slots VALUES('about', 'ABOUT', 'About Body');
INSERT INTO slots VALUES('waist', 'WAIST', 'About Waist');
INSERT INTO slots VALUES('arms', 'ARMS', 'Arms');
INSERT INTO slots VALUES('wrist', 'WRIST', 'Wrist');
INSERT INTO slots VALUES('hands', 'HANDS', 'Hands');
INSERT INTO slots VALUES('finger', 'FINGER', 'Finger');
INSERT INTO slots VALUES('wield', 'WIELD', 'Wielded');
INSERT INTO slots VALUES('shield', 'SHIELD', 'Shield');
INSERT INTO slots VALUES('held', 'HOLD', 'Held');
INSERT INTO slots VALUES('legs', 'LEGS', 'Legs');
INSERT INTO slots VALUES('feet', 'FEET', 'Feet');
INSERT INTO slots VALUES('no_wear', 'NOBITS', E'Can\'t Wear');
INSERT INTO slots VALUES('tail', 'TAIL', 'Tail');
INSERT INTO slots VALUES('quiver', 'QUIVER', 'Quiver');
INSERT INTO slots VALUES('badge', 'INSIGNIA', 'Badge');
INSERT INTO slots VALUES('component', 'COMPONENT_BAG', 'Component Bag');
INSERT INTO slots VALUES('learn', 'LEARN', E'Can\'t Wear');
INSERT INTO slots VALUES('light', 'LIGHT', E'Can\'t Wear');
INSERT INTO slots VALUES('throw', 'THROW', E'Can\'t Wear');
CREATE TABLE item_types(
	type_abbr varchar(10) PRIMARY KEY
	,item_type varchar(25)
	,type_display varchar(25)
);
INSERT INTO item_types VALUES('armor', 'ARMOR', 'Armor');
INSERT INTO item_types VALUES('worn', 'WORN', 'Worn');
INSERT INTO item_types VALUES('weapon', 'WEAPON', 'Weapon');
INSERT INTO item_types VALUES('ranged', 'FIRE_WEAPON', 'Ranged Weapon');
INSERT INTO item_types VALUES('quiver', 'QUIVER', 'Quiver');
INSERT INTO item_types VALUES('ammo', 'MISSILE', 'Ranged Ammo');
INSERT INTO item_types VALUES('container', 'CONTAINER', 'Container');
INSERT INTO item_types VALUES('spellbook', 'SPELLBOOK', 'Spellbook');
INSERT INTO item_types VALUES('quill', 'PEN', 'Quill');
INSERT INTO item_types VALUES('pick', 'PICK', 'Lockpicks');
INSERT INTO item_types VALUES('boat', 'BOAT', 'Boat');
INSERT INTO item_types VALUES('light', 'LIGHT', 'Light');
INSERT INTO item_types VALUES('staff', 'STAFF', 'Staff');
INSERT INTO item_types VALUES('wand', 'WAND', 'Wand');
INSERT INTO item_types VALUES('scroll', 'SCROLL', 'Scroll');
INSERT INTO item_types VALUES('potion', 'POTION', 'Potion');
INSERT INTO item_types VALUES('key', 'KEY', 'Key');
INSERT INTO item_types VALUES('poison', 'POISON', 'Poison');
INSERT INTO item_types VALUES('drink', 'LIQUID_CONT', 'Liquid Container');
INSERT INTO item_types VALUES('food', 'FOOD', 'Food');
INSERT INTO item_types VALUES('summon', 'SUMMON', 'Summon');
INSERT INTO item_types VALUES('instrument', 'INSTRUMENT', 'Instrument');
INSERT INTO item_types VALUES('crystal', 'PSP_CRYSTAL', 'PSP Crystal');
INSERT INTO item_types VALUES('comp_bag', 'COMPONENT_BAG', 'Component Bag');
INSERT INTO item_types VALUES('spell_comp', 'SPELL_COMPONENT', 'Spell Component');
INSERT INTO item_types VALUES('book', 'BOOK', 'Book');
INSERT INTO item_types VALUES('switch', 'SWITCH', 'Switch');
INSERT INTO item_types VALUES('note', 'NOTE', 'Note');
INSERT INTO item_types VALUES('treasure', 'TREASURE', 'Treasure');
INSERT INTO item_types VALUES('trash', 'TRASH', 'Trash');
INSERT INTO item_types VALUES('other', 'OTHER', 'Other');
INSERT INTO item_types VALUES('teleport', 'TELEPORT', 'Teleport');
CREATE TABLE zones(
	zone_abbr varchar(25) PRIMARY KEY
	,zone_name varchar(150)
);
INSERT INTO zones VALUES('SF', 'Southern Forest');
INSERT INTO zones VALUES('Jot', 'Jotunheim');
INSERT INTO zones VALUES('Monastery', 'Abandoned Monastery');
INSERT INTO zones VALUES('Adamantite Mine', 'Adamantite Mine');
INSERT INTO zones VALUES('Bloodtusk', 'Bloodtusk Keep');
INSERT INTO zones VALUES('BS', 'Bloodstone');
INSERT INTO zones VALUES('BB', 'Blood Bayou');
INSERT INTO zones VALUES('Beluir', 'Beluir');
INSERT INTO zones VALUES('Basin Wastes', 'Basin Wastes');
INSERT INTO zones VALUES('Bandit Hideout', 'Bandit Hideout');
INSERT INTO zones VALUES('BG', E'Baldur\'s Gate');
INSERT INTO zones VALUES('Astral', 'Astral Plane');
INSERT INTO zones VALUES('Ashstone', 'Ashstone');
INSERT INTO zones VALUES('Ashrumite', 'Ashrumite');
INSERT INTO zones VALUES('Ashgorrock', 'Ashgorrock');
INSERT INTO zones VALUES(E'Arnd\'ir', E'Arnd\'ir');
INSERT INTO zones VALUES('AV', E'A\'Quarthus Velg\'Larn');
INSERT INTO zones VALUES('Ant Farm', 'Ant Farm');
INSERT INTO zones VALUES('AO', 'Ancient Oak');
INSERT INTO zones VALUES('Ancient Mines', 'Ancient Mines');
INSERT INTO zones VALUES('AG(ZNM)', E'Amenth\'G\'narr');
INSERT INTO zones VALUES('Alterian Wilderness', 'Alterian Wilderness');
INSERT INTO zones VALUES('Alterian Mountains', 'Alterian Mountains');
INSERT INTO zones VALUES('Alabaster Caverns', 'Alabaster Caverns');
INSERT INTO zones VALUES('Ako', 'Ako Village');
INSERT INTO zones VALUES('Crypts', 'Crypts of Netheril');
INSERT INTO zones VALUES('Cormanthor Roads', 'Cormanthor Roads');
INSERT INTO zones VALUES('CV', 'Conquered Village');
INSERT INTO zones VALUES('Common', 'Common');
INSERT INTO zones VALUES('CM', 'Comarian Mines');
INSERT INTO zones VALUES('Clouds', 'Cloud Realms of Arlurrium');
INSERT INTO zones VALUES('Brass', 'City of Brass');
INSERT INTO zones VALUES('Citadel', 'Citadel');
INSERT INTO zones VALUES('Christmas', 'Christmas');
INSERT INTO zones VALUES('ChP', 'Choking Palace');
INSERT INTO zones VALUES('CC', 'Cave City');
INSERT INTO zones VALUES('Calimshan', 'Calimshan Desert');
INSERT INTO zones VALUES('CPV', 'Calimport Palace Vault');
INSERT INTO zones VALUES('CP', 'Calimport');
INSERT INTO zones VALUES('Bryn', 'Bryn Shander');
INSERT INTO zones VALUES('Brain Stem', 'Brain Stem Tunnel');
INSERT INTO zones VALUES('DSC', 'Dragonspear Castle');
INSERT INTO zones VALUES('Dood Workshop', E'Doodajipple\'s Workshop');
INSERT INTO zones VALUES('DK', 'Dobluth Kyor');
INSERT INTO zones VALUES('Derro', 'Derro Pit');
INSERT INTO zones VALUES('Demi', 'DemiPlane of Artimus Nevarlith');
INSERT INTO zones VALUES('Tarrasque', 'Deep Jungle (Tarrasque)');
INSERT INTO zones VALUES('DT', 'Darktree');
INSERT INTO zones VALUES('Darklake', 'Darklake');
INSERT INTO zones VALUES('Darkhold', 'Darkhold Castle');
INSERT INTO zones VALUES('Dark Forest', 'Dark Forest');
INSERT INTO zones VALUES('Dark Dominion', 'Dark Dominion');
INSERT INTO zones VALUES('Newhaven', 'Curse of Newhaven');
INSERT INTO zones VALUES('West Falls', 'Cursed City of West Falls');
INSERT INTO zones VALUES('Cursed Cemetary', 'Cursed Cemetary');
INSERT INTO zones VALUES(E'Elg\'cahl Niar', E'Elg\'cahl Niar');
INSERT INTO zones VALUES('WP', 'Elemental Plane of Water');
INSERT INTO zones VALUES('FP', 'Elemental Plane of Fire');
INSERT INTO zones VALUES('Air', 'Elemental Plane of Air');
INSERT INTO zones VALUES('Elemental Glades', 'Elemental Glades');
INSERT INTO zones VALUES('Elder Forest', 'Elder Forest');
INSERT INTO zones VALUES('Dwarf Settlement', 'Dwarven Mining Settlement');
INSERT INTO zones VALUES('Dusk Road', 'Dusk Road');
INSERT INTO zones VALUES('Drulak', 'Drulak');
INSERT INTO zones VALUES('DS', E'Druid\'s Sanctuary');
INSERT INTO zones VALUES('Druid Grove', E'Druid\'s Grove');
INSERT INTO zones VALUES('Driders', 'Drider Cavern');
INSERT INTO zones VALUES('Dread Mist', 'Dread Mist');
INSERT INTO zones VALUES('Dragonspine', 'Dragonspine Mountains');
INSERT INTO zones VALUES('Gith', 'Githyanki Fortress');
INSERT INTO zones VALUES('Ghore', 'Ghore');
INSERT INTO zones VALUES('DCult', 'Fortress of the Dragon Cult');
INSERT INTO zones VALUES('Mir', 'Forest of Mir');
INSERT INTO zones VALUES('Fog Enshrouded Woods', 'Fog Enshrouded Woods');
INSERT INTO zones VALUES('FGV', 'Fire Giant Village');
INSERT INTO zones VALUES('FGL', 'Fire Giant Lair');
INSERT INTO zones VALUES('Finders', E'Finder\'s');
INSERT INTO zones VALUES('Faerie Realms', 'Faerie Realms');
INSERT INTO zones VALUES('Faang', 'Faang');
INSERT INTO zones VALUES('Evermoors', 'Evermoors');
INSERT INTO zones VALUES('EM Roads', 'Evermeet Roads');
INSERT INTO zones VALUES('Embay', 'Evermeet Bay');
INSERT INTO zones VALUES('EM', 'Evermeet');
INSERT INTO zones VALUES('Eth', 'Ethereal Plane');
INSERT INTO zones VALUES('Endu Village', 'Endu Village');
INSERT INTO zones VALUES('Elven Settlement', 'Elven Settlement');
INSERT INTO zones VALUES('Scorps', 'Hive of the Manscorpions');
INSERT INTO zones VALUES('Hidden Mines', 'Hidden Mines');
INSERT INTO zones VALUES('Herd Chasm', 'Herd Island Chasm');
INSERT INTO zones VALUES('Heartland Roads', 'Heartland Roads');
INSERT INTO zones VALUES('Trune', 'Headquarters of the Twisted Rune');
INSERT INTO zones VALUES('HP', 'Havenport');
INSERT INTO zones VALUES('Airship', 'Halruaan Airship');
INSERT INTO zones VALUES('GN', E'Griffon\'s Nest');
INSERT INTO zones VALUES('GC', 'Greycloak Hills');
INSERT INTO zones VALUES('GF', 'Golem Forge');
INSERT INTO zones VALUES('GH', 'Gloomhaven');
INSERT INTO zones VALUES('Global', 'Global');
INSERT INTO zones VALUES('Menden', 'Menden on the Deep');
INSERT INTO zones VALUES('Luskan', 'Luskan Outpost');
INSERT INTO zones VALUES('Lurkwood', 'Lurkwood');
INSERT INTO zones VALUES('Meilech', 'Lost Swamps of Meilech');
INSERT INTO zones VALUES('Lost Pyramid', 'Lost Pyramid');
INSERT INTO zones VALUES('Seer Kings', 'Lost Library of the Seer Kings');
INSERT INTO zones VALUES('Longhollow', 'Longhollow');
INSERT INTO zones VALUES('Llyrath Forest', 'Llyrath Forest');
INSERT INTO zones VALUES('Lizard Marsh', 'Lizard Marsh');
INSERT INTO zones VALUES('Leuth', 'Leuthilspar');
INSERT INTO zones VALUES('Lava Tubes', 'Lava Tubes');
INSERT INTO zones VALUES('Larallyn', 'Larallyn');
INSERT INTO zones VALUES('Skeldrach', 'Lake Skeldrach');
INSERT INTO zones VALUES('Deep Dragon', 'Lair of the Deep Dragon');
INSERT INTO zones VALUES('Laby', 'Labyrinth of No Return');
INSERT INTO zones VALUES('Old KV', 'Kobold Village');
INSERT INTO zones VALUES('KV', 'Klauthen Vale');
INSERT INTO zones VALUES('Keprum', E'Keprum Vhai\'Rhel');
INSERT INTO zones VALUES('FK', 'Keep of Finn McCumhail');
INSERT INTO zones VALUES('Jungles of Ssrynss', 'Jungles of Ssrynss');
INSERT INTO zones VALUES('Hyssk', 'Jungle City of Hyssk');
INSERT INTO zones VALUES(E'Izan\'s', E'Izan\'s Floating Fortress');
INSERT INTO zones VALUES('IxP', 'Ixarkon Prison');
INSERT INTO zones VALUES('Ix', 'Ixarkon');
INSERT INTO zones VALUES('Ice Prison', 'Ice Prison');
INSERT INTO zones VALUES('IC2', 'Ice Crag Castle 2');
INSERT INTO zones VALUES('IC1', 'Ice Crag Castle 1');
INSERT INTO zones VALUES('Hulburg', 'Hulburg');
INSERT INTO zones VALUES('Northern High Road', 'Northern High Road');
INSERT INTO zones VALUES('Nizari', 'Nizari');
INSERT INTO zones VALUES('BC', 'Nine Hells: Bronze Citadel');
INSERT INTO zones VALUES('Avernus', 'Nine Hells: Avernus');
INSERT INTO zones VALUES('Nightwood', 'Nightwood');
INSERT INTO zones VALUES('Nhavan Island', 'Nhavan Island');
INSERT INTO zones VALUES('Neverwinter', 'Neverwinter');
INSERT INTO zones VALUES('Neshkal', 'Neshkal, The Dragon Trail');
INSERT INTO zones VALUES('Necro Lab', E'Necromancer\'s Laboratory');
INSERT INTO zones VALUES('Myth Unnohyr', 'Myth Unnohyr');
INSERT INTO zones VALUES('MD', 'Myth Drannor');
INSERT INTO zones VALUES('Myrloch Vale', 'Myrloch Vale');
INSERT INTO zones VALUES('Musp', 'Muspelheim');
INSERT INTO zones VALUES('Mosswood', 'Mosswood Village');
INSERT INTO zones VALUES('Moonshaes', 'Moonshae Islands');
INSERT INTO zones VALUES('MHP', 'Mithril Hall Palace');
INSERT INTO zones VALUES('MH', 'Mithril Hall');
INSERT INTO zones VALUES('Misty', 'Misty Woods');
INSERT INTO zones VALUES('Minos', 'Minotaur Outpost');
INSERT INTO zones VALUES('Menzo', 'Menzoberranzan');
INSERT INTO zones VALUES('Scardale', 'Scardale');
INSERT INTO zones VALUES(E'Rurrgr T\'Ohrr', E'Rurrgr T\'Ohrr');
INSERT INTO zones VALUES('Yath Oloth', 'Ruins of Yath Oloth');
INSERT INTO zones VALUES('Ruined Keep', 'Ruined Keep');
INSERT INTO zones VALUES('RP', 'Roleplay');
INSERT INTO zones VALUES('Roots', 'Roots');
INSERT INTO zones VALUES(E'Rogue\'s Lair', E'Rogue\'s Lair');
INSERT INTO zones VALUES('Rogath Swamp', 'Rogath Swamp');
INSERT INTO zones VALUES('Ribcage', 'Ribcage: Gate Town to Baator');
INSERT INTO zones VALUES('Reaching Woods', 'Reaching Woods');
INSERT INTO zones VALUES('Rat Hills', 'Rat Hills');
INSERT INTO zones VALUES('Randars', E'Randar\'s Hideout');
INSERT INTO zones VALUES('RC', 'Rainbow Curtain of Ilsensine');
INSERT INTO zones VALUES('PoS', 'Pit of Souls');
INSERT INTO zones VALUES('PI', 'Pirate Isles');
INSERT INTO zones VALUES('Smoke', 'Para-Elemental Plane of Smoke');
INSERT INTO zones VALUES('Magma', 'Para-Elemental Plane of Magma');
INSERT INTO zones VALUES('Ice', 'Para-Elemental Plane of Ice');
INSERT INTO zones VALUES('OHP', 'Orcish Hall of Plunder');
INSERT INTO zones VALUES('Ogre Lair', 'Ogre Lair');
INSERT INTO zones VALUES('Sylvan Glades', 'Sylvan Glades');
INSERT INTO zones VALUES('SSC', 'Swift-Steel Mercenary Company');
INSERT INTO zones VALUES('Sunken City', 'Sunken Slave City');
INSERT INTO zones VALUES('Stump Bog', 'Stump Bog');
INSERT INTO zones VALUES('Oakvale', 'Stronghold of Trahern Oakvale');
INSERT INTO zones VALUES('SS', 'Split Shield Village');
INSERT INTO zones VALUES('Spirit World', 'Spirit World');
INSERT INTO zones VALUES('PShip', 'Spirit Raven');
INSERT INTO zones VALUES('SH', 'Spiderhaunt Woods');
INSERT INTO zones VALUES('SPoB', 'Soulprison of Bhaal');
INSERT INTO zones VALUES('SP Island', 'Skullport Prison Island');
INSERT INTO zones VALUES('SP', 'Skullport');
INSERT INTO zones VALUES('SG', 'Skerttd-Gul');
INSERT INTO zones VALUES('SM', 'Silverymoon');
INSERT INTO zones VALUES('Shadow Swamp', 'Shadow Swamp');
INSERT INTO zones VALUES('SoI Guild', 'Shadows of Imphras Guildhall');
INSERT INTO zones VALUES('Settlestone', 'Settlestone');
INSERT INTO zones VALUES('Serene Forest', 'Serene Forest');
INSERT INTO zones VALUES('Seelie', 'Seelie Faerie Court');
INSERT INTO zones VALUES('Seaweed Tribe', 'Seaweed Tribe');
INSERT INTO zones VALUES('Scorx', 'Scorxariam');
INSERT INTO zones VALUES('Scorn', 'Scornubel');
INSERT INTO zones VALUES('Scorched Forest', 'Scorched Forest');
INSERT INTO zones VALUES('UM2', 'Undermountain 2');
INSERT INTO zones VALUES('UM1', 'Undermountain 1');
INSERT INTO zones VALUES('UM', 'Undermountain');
INSERT INTO zones VALUES('UD River Ruins', 'Underdark River Ruins');
INSERT INTO zones VALUES('UD', 'Underdark');
INSERT INTO zones VALUES('Undead Farm', 'Undead Farm');
INSERT INTO zones VALUES('Tunnel of Dread', 'Tunnel of Dread');
INSERT INTO zones VALUES('TK', 'Troll King');
INSERT INTO zones VALUES('Troll Hills', 'Troll Hills');
INSERT INTO zones VALUES('TB', 'Trollbark Forest');
INSERT INTO zones VALUES('Trit Guild', 'Triterium Guildhall');
INSERT INTO zones VALUES('Trail to Ten Towns', 'Trail to Ten Towns');
INSERT INTO zones VALUES('Trade Way, South', 'Trade Way, South');
INSERT INTO zones VALUES('Trade Way', 'Trade Way');
INSERT INTO zones VALUES(E'Trader\'s Road', E'Trader\'s Road');
INSERT INTO zones VALUES('TE', 'Tower of the Elementalist');
INSERT INTO zones VALUES('Kenjin', 'Tower of Kenjin');
INSERT INTO zones VALUES('Tower', 'Tower of High Sorcery');
INSERT INTO zones VALUES('Tiamat', E'Tiamat\'s Lair');
INSERT INTO zones VALUES('Thunderhead Peak', 'Thunderhead Peak');
INSERT INTO zones VALUES('The Labyrinth', 'The Labyrinth');
INSERT INTO zones VALUES('TTF', 'Temple of Twisted Flesh');
INSERT INTO zones VALUES('Moon Temple', 'Temple of the Moon');
INSERT INTO zones VALUES('Eye Temple', 'Temple of Ghaunadaur');
INSERT INTO zones VALUES('Temple of Dumathoin', 'Temple of Dumathoin');
INSERT INTO zones VALUES('Blipdoolpoolp', 'Temple of Blipdoolpoolp');
INSERT INTO zones VALUES('TF', 'Tarsellian Forest');
INSERT INTO zones VALUES('Talthalra Haszakkin', 'Talthalra Haszakkin');
INSERT INTO zones VALUES('Talenrock', 'Talenrock');
INSERT INTO zones VALUES('ZK', 'Zhentil Keep');
INSERT INTO zones VALUES('Wyllowwood', 'Wyllowwood');
INSERT INTO zones VALUES('Wormwrithings', 'Wormwrithings');
INSERT INTO zones VALUES('Wildland Trails', 'Wildland Trails');
INSERT INTO zones VALUES('Western Realms', 'Western Realms');
INSERT INTO zones VALUES('Way Inn', 'Way Inn');
INSERT INTO zones VALUES('WD Sewers', 'Waterdeep Sewers');
INSERT INTO zones VALUES('WD Docks', 'Waterdeep Docks');
INSERT INTO zones VALUES('WD Coast Road', 'Waterdeep Coast Road');
INSERT INTO zones VALUES('WD', 'Waterdeep');
INSERT INTO zones VALUES('Warder Guild', 'Warders Guildhall');
INSERT INTO zones VALUES('VT', 'Viperstongue Outpost');
INSERT INTO zones VALUES('Graydawn', 'Valley of Graydawn');
INSERT INTO zones VALUES('Crushk', 'Valley of Crushk');
INSERT INTO zones VALUES('Unknown', 'Unknown');
CREATE TABLE mobs(
	mob_name varchar(150) PRIMARY KEY
	,mob_abbr varchar(25)
	,from_zone varchar(10) REFERENCES zones(zone_abbr)
	,from_quest boolean
	,has_quest boolean
	,is_rare boolean
	,from_invasion boolean
);
CREATE TABLE specials(
	item_type varchar(10) REFERENCES item_types(type_abbr)
	,spec_abbr varchar(10)
	,spec_display varchar(25)
	,PRIMARY KEY (item_type, spec_abbr)
);
INSERT INTO specials VALUES('armor', 'ac', 'Armor Class'); -- intac
INSERT INTO specials VALUES('crystal', 'psp', 'Crystal PSP'); -- varpsp
INSERT INTO specials VALUES('spellbook', 'pages', 'Pages'); -- varpages
INSERT INTO specials VALUES('container', 'holds', 'Capacity'); -- varholds
INSERT INTO specials VALUES('container', 'wtless', 'Weightless');
INSERT INTO specials VALUES('comp_bag', 'holds', 'Capacity'); -- varholds
INSERT INTO specials VALUES('poison', 'level', 'Level'); -- varlevel
INSERT INTO specials VALUES('poison', 'type', 'Poison Type'); -- varpoison
INSERT INTO specials VALUES('poison', 'apps', 'Applications'); -- varapplications
INSERT INTO specials VALUES('scroll', 'level', 'Level'); -- varwlevel
INSERT INTO specials VALUES('scroll', 'spell1', 'First Spell'); -- varwspell
INSERT INTO specials VALUES('scroll', 'spell2', 'Second Spell'); -- varwspell
INSERT INTO specials VALUES('scroll', 'spell3', 'Third Spell'); -- varwspell
INSERT INTO specials VALUES('potion', 'level', 'Level'); -- varwlevel
INSERT INTO specials VALUES('potion', 'spell1', 'First Spell'); -- varwspell
INSERT INTO specials VALUES('potion', 'spell2', 'Second Spell'); -- varwspell
INSERT INTO specials VALUES('potion', 'spell3', 'Third Spell'); -- varwspell
INSERT INTO specials VALUES('staff', 'level', 'Level'); -- varwlevel
INSERT INTO specials VALUES('staff', 'spell', 'Spell'); -- varwspell
INSERT INTO specials VALUES('staff', 'charges', 'Charges'); -- varmaxcharge
INSERT INTO specials VALUES('wand', 'level', 'Level'); -- varwlevel
INSERT INTO specials VALUES('wand', 'spell', 'Spell'); -- varwspell
INSERT INTO specials VALUES('wand', 'charges', 'Charges'); -- varmaxcharge
INSERT INTO specials VALUES('instrument', 'stutter', 'Stutter'); -- varstutter
INSERT INTO specials VALUES('instrument', 'quality', 'Quality'); -- varquality
INSERT INTO specials VALUES('instrument', 'min_level', 'Min Level'); -- varmin
INSERT INTO specials VALUES('weapon', 'dice', 'Damage Dice'); -- vardice
INSERT INTO specials VALUES('weapon', 'type', 'Type'); -- varwtype
INSERT INTO specials VALUES('weapon', 'class', 'Class'); -- varwclass
INSERT INTO specials VALUES('weapon', 'crit', 'Crit Chance'); -- varcrange
INSERT INTO specials VALUES('weapon', 'multi', 'Crit Multiplier'); -- varcbonus
INSERT INTO specials VALUES('ammo', 'dice', 'Damage Dice'); -- vardice
CREATE TABLE items(
	item_id serial PRIMARY KEY
	,item_name varchar(100) NOT NULL
	,keywords varchar(100)
	,weight integer
	,c_value integer
	,item_type varchar(10) REFERENCES item_types(type_abbr)
	,from_zone varchar(25) REFERENCES zones(zone_abbr)
	,from_mob varchar(150) REFERENCES mobs(mob_name)
	,no_identify boolean
	,is_rare boolean
	,from_store boolean
	,from_quest boolean
	,for_quest boolean
	,from_invasion boolean
	,out_of_game boolean
	,short_stats varchar(450)
	,long_stats varchar(900)
	,full_stats text
	,comments text
	,last_id date
	,tsv tsvector
);
CREATE INDEX idx_item_name ON items (item_name);
UPDATE items SET tsv =
	to_tsvector('english', coalesce(item_name,'') || ' ' || coalesce(keywords,''));
CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
	ON items FOR EACH ROW EXECUTE PROCEDURE
	tsvector_update_trigger(tsv, 'pg_catalog.english', item_name, keywords);
CREATE TABLE item_procs(
	item_id integer REFERENCES items(item_id)
	,proc_name text
	,proc_type varchar(25)
	,proc_desc varchar(25)
	,proc_trig varchar(25)
	,proc_effect varchar(25)
	,PRIMARY KEY (item_id, proc_name)
);
CREATE TABLE item_slots(
	item_id integer REFERENCES items(item_id)
	,slot_abbr varchar(10) REFERENCES slots(slot_abbr)
	,PRIMARY KEY (item_id, slot_abbr)
);
CREATE TABLE item_flags(
	item_id integer REFERENCES items(item_id)
	,flag_abbr varchar(10) REFERENCES flags(flag_abbr)
	,PRIMARY KEY (item_id, flag_abbr)
);
CREATE TABLE item_restricts(
	item_id integer REFERENCES items(item_id)
	,restrict_abbr varchar(10) REFERENCES restricts(restrict_abbr)
	,PRIMARY KEY (item_id, restrict_abbr)
);
CREATE TABLE item_resists(
	item_id integer REFERENCES items(item_id)
	,resist_abbr varchar(10) REFERENCES resists(resist_abbr)
	,resist_value integer
	,PRIMARY KEY (item_id, resist_abbr)
);
CREATE TABLE item_effects(
	item_id integer REFERENCES items(item_id)
	,effect_abbr varchar(10) REFERENCES effects(effect_abbr)
	,PRIMARY KEY (item_id, effect_abbr)
);
CREATE TABLE item_specials(
	item_id integer REFERENCES items(item_id)
	,item_type varchar(10)
	,spec_abbr varchar(10)
	,spec_value varchar(30)
	,FOREIGN KEY (item_type, spec_abbr) REFERENCES specials (item_type, spec_abbr)
	,PRIMARY KEY (item_id, item_type, spec_abbr)
);
CREATE TABLE item_enchants(
	item_id integer REFERENCES items(item_id)
	,ench_name varchar(25) REFERENCES enchants(ench_name)
	,dam_pct integer
	,freq_pct integer
	,sv_mod integer
	,duration integer
	,PRIMARY KEY (item_id, ench_name)
);
CREATE TABLE item_attribs(
	item_id integer REFERENCES items(item_id)
	,attrib_abbr varchar(25) REFERENCES attribs(attrib_abbr)
	,attrib_value integer
	,PRIMARY KEY (item_id, attrib_abbr)
);

CREATE TABLE legacy (
	id serial PRIMARY KEY,
	varName text, varKeywords text, varZone text, varLoad text, varQuest text, varNoID text,
	varType text, varWorn text, varWt text, varHolds text, varValue text, intAC integer,
	varArmor text, varPages text, varHP text, varDice text, varWType text, varWClass text,
	varCRange text, varCBonus text, intHit integer, intDam integer, varSpell text,
	varBreath text, varPara text, varPetri text, varRod text, varStr text, varAgi text,
	varDex text, varCon text, varPow text, varInt text, varWis text, varCha text,
	varMaxstr text, varMaxagi text, varMaxdex text, varMaxcon text, varMaxpow text,
	varMaxint text, varMaxwis text, varMaxcha text, varLuck text, varKarma text, varMana text,
	varMove text, varAge text, varWeight text, varHeight text, varMR text, varSFEle text,
	varSFEnc text, varSFHeal text, varSFIll text, varSFInv text, varSFNature text,
	varSFNec text, varSFProt text, varSFPsi text, varSFSpirit text, varSFSum text,
	varSFTele text, varPsp text, varQuality text, varStutter text, varMin text,
	varPoison text, varLevel text, varApplications text, varCharge text, varMaxcharge text,
	varWlevel text, varWspell text, varRes text, varCRes text, varEnchant text,
	varEffects text, varCrit text, varBonus text, varCeffects text, varUnarmd text,
	varSlash text, varBludgn text, varPierce text, varRange text, varSpells text,
	varSonic text, varPos text, varNeg text, varPsi text, varMental text, varGoods text,
	varEvils text, varLaw text, varChaos text, varForce text, varFire text, varCold text,
	varElect text, varAcid text, varPois text, varAflags text, varIflags text, varDate text
);
\COPY legacy (varName, varKeywords, varZone, varLoad, varQuest, varNoID, varType, varWorn, varWt, varHolds, varValue, intAC, varArmor, varPages, varHP, varDice, varWType, varWClass, varCRange, varCBonus, intHit, intDam, varSpell, varBreath, varPara, varPetri, varRod, varStr, varAgi, varDex, varCon, varPow, varInt, varWis, varCha, varMaxstr, varMaxagi, varMaxdex, varMaxcon, varMaxpow, varMaxint, varMaxwis, varMaxcha, varLuck, varKarma, varMana, varMove, varAge, varWeight, varHeight, varMR, varSFEle, varSFEnc, varSFHeal, varSFIll, varSFInv, varSFNature, varSFNec, varSFProt, varSFPsi, varSFSpirit, varSFSum, varSFTele, varPsp, varQuality, varStutter, varMin, varPoison, varLevel, varApplications, varCharge, varMaxcharge, varWlevel, varWspell, varRes, varCRes, varEnchant, varEffects, varCrit, varBonus, varCeffects, varUnarmd, varSlash, varBludgn, varPierce, varRange, varSpells, varSonic, varPos, varNeg, varPsi, varMental, varGoods, varEvils, varLaw, varChaos, varForce, varFire, varCold, varElect, varAcid, varPois, varAflags, varIflags, varDate) FROM 'torileq_tab_2013_02_15.txt' WITH DELIMITER E'\t'
