--convert old values to slightly improved new values:
INSERT INTO zones VALUES(E'Izan\'s', E'Izan\'s Floating Fortress');
UPDATE items SET from_zone = E'Izan\'s' WHERE from_zone = 'Izans';
DELETE FROM zones WHERE zone_abbr = 'Izans';
INSERT INTO flags VALUES('no_sum', 'NOSUMMON', 'No Summon');
UPDATE item_flags SET flag_abbr = 'no_sum' WHERE flag_abbr = 'nosum';
DELETE FROM flags WHERE flag_abbr = 'nosum';
INSERT INTO flags VALUES('no_sleep', 'NOSLEEP', 'No Sleep');
UPDATE item_flags SET flag_abbr = 'no_sleep' WHERE flag_abbr = 'nosleep';
DELETE FROM flags WHERE flag_abbr = 'nosleep';
INSERT INTO flags VALUES('no_charm', 'NOCHARM', 'No Charm');
UPDATE item_flags SET flag_abbr = 'no_charm' WHERE flag_abbr = 'nocharm';
DELETE FROM flags WHERE flag_abbr = 'nocharm';
INSERT INTO flags VALUES('no_burn', 'NOBURN', 'No Burn');
UPDATE item_flags SET flag_abbr = 'no_burn' WHERE flag_abbr = 'noburn';
DELETE FROM flags WHERE flag_abbr = 'noburn';
INSERT INTO flags VALUES('no_drop', 'NODROP', 'No Drop');
UPDATE item_flags SET flag_abbr = 'no_drop' WHERE flag_abbr = 'nodrop';
DELETE FROM flags WHERE flag_abbr = 'nodrop';
INSERT INTO flags VALUES('no_loc', 'NOLOCATE', 'No Locate');
UPDATE item_flags SET flag_abbr = 'no_loc' WHERE flag_abbr = 'noloc';
DELETE FROM flags WHERE flag_abbr = 'noloc';
INSERT INTO flags VALUES('no_sell', 'NOSELL', 'No Sell');
UPDATE item_flags SET flag_abbr = 'no_sell' WHERE flag_abbr = 'nosell';
DELETE FROM flags WHERE flag_abbr = 'nosell';
INSERT INTO flags VALUES('no_rent', 'NORENT', 'No Rent');
UPDATE item_flags SET flag_abbr = 'no_rent' WHERE flag_abbr = 'norent';
DELETE FROM flags WHERE flag_abbr = 'norent';
INSERT INTO flags VALUES('no_take', 'NOTAKE', 'No Take');
UPDATE item_flags SET flag_abbr = 'no_take' WHERE flag_abbr = 'notake';
DELETE FROM flags WHERE flag_abbr = 'notake';
INSERT INTO restricts VALUES('!priest', 'NO-CLERIC');
UPDATE item_restricts SET restrict_abbr = '!priest' WHERE restrict_abbr = '!cleric';
DELETE FROM restricts WHERE restrict_abbr = '!cleric';
INSERT INTO restricts VALUES('!cleric', 'ANTI-CLERIC');
UPDATE item_restricts SET restrict_abbr = '!cleric' WHERE restrict_abbr = '!cler';
DELETE FROM restricts WHERE restrict_abbr = '!cler';
INSERT INTO restricts VALUES('!fighter', 'NO-WARRIOR');
UPDATE item_restricts SET restrict_abbr = '!fighter' WHERE restrict_abbr = '!war';
DELETE FROM restricts WHERE restrict_abbr = '!war';
INSERT INTO effects VALUES('slow_poi', 'SLOW-POISON', 'Slow Poison');
UPDATE item_effects SET effect_abbr = 'slow_poi' WHERE effect_abbr = 'slowpoi';
DELETE FROM effects WHERE effect_abbr = 'slowpoi';

--convert attrib1, attrib1_value, attrib2, attrib2_value to item_attribs:
CREATE TABLE item_attribs(
	item_id integer REFERENCES items(item_id)
	,attrib_abbr varchar(25) REFERENCES attribs(attrib_abbr)
	,attrib_value integer
	,PRIMARY KEY (item_id, attrib_abbr)
);
INSERT INTO item_attribs (item_id, attrib_abbr, attrib_value)
	SELECT item_id, attrib1, attrib1_value FROM items
	WHERE attrib1 is not null;
INSERT INTO item_attribs (item_id, attrib_abbr, attrib_value)
	SELECT item_id, attrib2, attrib2_value FROM items
	WHERE attrib2 is not null;
ALTER TABLE items DROP COLUMN attrib1;
ALTER TABLE items DROP COLUMN attrib2;
ALTER TABLE items DROP COLUMN attrib1_value;
ALTER TABLE items DROP COLUMN attrib2_value;

