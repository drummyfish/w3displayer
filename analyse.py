# -*- coding: utf-8 -*-
#
#  This script takes a Warcraft III replay file (.w3g) and
#  outputs a text information about the game states at
#  different times, that can then be played by various
#  players.
#
#  Miloslav Číž, 2015

# This file is part of w3displayer.
# 
# w3displayer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# w3displayer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with w3displayer.  If not, see <http://www.gnu.org/licenses/>.

import w3g
from sets import Set
import sys
import json

TIME_STEP = 500             # time of periodic update, in miliseconds
ACTIONS_SHOWN = 5           # how many last player action to show
RECENTLY_USED_COUNTDOWN = 3 # for how many frames a recently used ability will be shown

APM_INTERVAL = 5000;        # current APM is computed from actions in last APM_INTERVAL ms

TIER_UPGRADE_TIME = 140000;

HERO_REVIVE_TIMES = {  # revive times of heroes by level  
    0 :  55000,
    1 :  35750,
    2 :  71500,
    3 : 107250,
    4 : 143000,
    5 : 178750,
    6 : 214500,
    7 : 250250,
    8 : 286000, 
    9 : 321750,
   10 : 357500 
  }

NEUTRAL_HERO_STRINGS = [
  w3g.ITEMS[b'Nngs'],
  w3g.ITEMS[b'Nbrn'],
  w3g.ITEMS[b'Npbm'],
  w3g.ITEMS[b'Nbst'],
  w3g.ITEMS[b'Npld'],
  w3g.ITEMS[b'Ntin'],
  w3g.ITEMS[b'Nfir'],
  w3g.ITEMS[b'Nalc'],
  ]

HERO_STRINGS = [
  w3g.ITEMS[b'Hpal'],
  w3g.ITEMS[b'Hamg'],
  w3g.ITEMS[b'Hmkg'],
  w3g.ITEMS[b'Hblm'],
  w3g.ITEMS[b'Ofar'],
  w3g.ITEMS[b'Oshd'],
  w3g.ITEMS[b'Obla'],
  w3g.ITEMS[b'Otch'],
  w3g.ITEMS[b'Udea'],
  w3g.ITEMS[b'Ulic'],
  w3g.ITEMS[b'Udre'],
  w3g.ITEMS[b'Ucrl'],
  w3g.ITEMS[b'Edem'],
  w3g.ITEMS[b'Ekee'],
  w3g.ITEMS[b'Emoo'],
  w3g.ITEMS[b'Ewar']
  ]

HERO_STRINGS += NEUTRAL_HERO_STRINGS

ACTION_COSTS = {       # gold, lumber, food
  # human:
  w3g.ITEMS[b'Hamg'] : (0,0,0),     # archmage
  w3g.ITEMS[b'Hmkg'] : (0,0,0),     # mountain king
  w3g.ITEMS[b'Hblm'] : (0,0,0),     # blood mage
  w3g.ITEMS[b'Hpal'] : (0,0,0),     # paladin
  w3g.ITEMS[b'hpea'] : (0,0,0),     # peasant
  w3g.ITEMS[b'hfoo'] : (0,0,0),     # footman
  w3g.ITEMS[b'hrif'] : (0,0,0),     # rifleman
  w3g.ITEMS[b'hkni'] : (0,0,0),     # knight
  w3g.ITEMS[b'hmpr'] : (0,0,0),     # priest
  w3g.ITEMS[b'hsor'] : (0,0,0),     # sorceress
  w3g.ITEMS[b'hspt'] : (0,0,0),     # spell breaker
  w3g.ITEMS[b'hmtm'] : (0,0,0),     # mortar team
  w3g.ITEMS[b'hmtt'] : (0,0,0),     # siege engine
  w3g.ITEMS[b'hgry'] : (0,0,0),     # gryphon rider
  w3g.ITEMS[b'nws1'] : (0,0,0),     # dragon hawk
  w3g.ITEMS[b'hgyr'] : (0,0,0),     # flying machine
  w3g.ITEMS[b'htow'] : (0,0,0),     # town hall
  w3g.ITEMS[b'hkee'] : (0,0,0),     # keep
  w3g.ITEMS[b'hcas'] : (0,0,0),     # castle   
  w3g.ITEMS[b'halt'] : (0,0,0),     # altar of kings
  w3g.ITEMS[b'hvlt'] : (0,0,0),     # arcane vault
  w3g.ITEMS[b'hars'] : (0,0,0),     # arcane sanctum
  w3g.ITEMS[b'hbar'] : (0,0,0),     # barracks
  w3g.ITEMS[b'hbla'] : (0,0,0),     # blacksmith
  w3g.ITEMS[b'harm'] : (0,0,0),     # workshop
  w3g.ITEMS[b'hatw'] : (0,0,0),     # arcane tower
  w3g.ITEMS[b'hctw'] : (0,0,0),     # cannon tower
  w3g.ITEMS[b'hgtw'] : (0,0,0),     # guard tower
  w3g.ITEMS[b'hlum'] : (0,0,0),     # lumber mill
  w3g.ITEMS[b'hgra'] : (0,0,0),     # gryphon aviary
  w3g.ITEMS[b'hwtw'] : (0,0,0),     # scout tower
  w3g.ITEMS[b'hhou'] : (0,0,0),     # farm
  w3g.ITEMS[b'Rhaa'] : (0,0,0),     # artillery
  w3g.ITEMS[b'Rhac'] : (0,0,0),     # masonry
  w3g.ITEMS[b'Rhan'] : (0,0,0),     # animal war training
  w3g.ITEMS[b'Rhar'] : (0,0,0),     # plating
  w3g.ITEMS[b'Rhcd'] : (0,0,0),     # cloud
  w3g.ITEMS[b'Rhde'] : (0,0,0),     # defend
  w3g.ITEMS[b'Rhfc'] : (0,0,0),     # flak cannons
  w3g.ITEMS[b'Rhfs'] : (0,0,0),     # fragmentation shards
  w3g.ITEMS[b'Rhgb'] : (0,0,0),     # flying machine bombs
  w3g.ITEMS[b'Rhhb'] : (0,0,0),     # storm hammers
  w3g.ITEMS[b'Rhla'] : (0,0,0),     # leather armor
  w3g.ITEMS[b'Rhlh'] : (0,0,0),     # lumber harvesting
  w3g.ITEMS[b'Rhme'] : (0,0,0),     # melee weapons
  w3g.ITEMS[b'Rhmi'] : (0,0,0),     # gold
  w3g.ITEMS[b'Rhpt'] : (0,0,0),     # priest training
  w3g.ITEMS[b'Rhra'] : (0,0,0),     # ranged weapons
  w3g.ITEMS[b'Rhri'] : (0,0,0),     # long rifles
  w3g.ITEMS[b'Rhrt'] : (0,0,0),     # barrage
  w3g.ITEMS[b'Rhse'] : (0,0,0),     # magic sentry
  w3g.ITEMS[b'Rhsr'] : (0,0,0),     # flare
  w3g.ITEMS[b'Rhss'] : (0,0,0),     # control magic
  w3g.ITEMS[b'Rhst'] : (0,0,0),     # sorceress training
  # orc:
  w3g.ITEMS[b'Obla'] : (0,0,0),     # blademaster
  w3g.ITEMS[b'Ofar'] : (0,0,0),     # far seer
  w3g.ITEMS[b'Oshd'] : (0,0,0),     # shadow hunter
  w3g.ITEMS[b'Otch'] : (0,0,0),     # tauren chieftain
  w3g.ITEMS[b'opeo'] : (0,0,0),     # peon
  w3g.ITEMS[b'ogru'] : (0,0,0),     # grunt
  w3g.ITEMS[b'ohun'] : (0,0,0),     # troll headhunter
  w3g.ITEMS[b'otbk'] : (0,0,0),     # troll berserker
  w3g.ITEMS[b'oshm'] : (0,0,0),     # shaman
  w3g.ITEMS[b'odoc'] : (0,0,0),     # witch doctor
  w3g.ITEMS[b'ospw'] : (0,0,0),     # spirit walker
  w3g.ITEMS[b'orai'] : (0,0,0),     # raider
  w3g.ITEMS[b'okod'] : (0,0,0),     # kodo beast
  w3g.ITEMS[b'ocat'] : (0,0,0),     # demolisher
  w3g.ITEMS[b'otbr'] : (0,0,0),     # troll batrider
  w3g.ITEMS[b'owyv'] : (0,0,0),     # wind rider
  w3g.ITEMS[b'otau'] : (0,0,0),     # tauren
  w3g.ITEMS[b'ogre'] : (0,0,0),     # great hall
  w3g.ITEMS[b'ostr'] : (0,0,0),     # stronghold
  w3g.ITEMS[b'ofrt'] : (0,0,0),     # fortress
  w3g.ITEMS[b'osld'] : (0,0,0),     # spirit lodge
  w3g.ITEMS[b'otto'] : (0,0,0),     # tauren totem
  w3g.ITEMS[b'obea'] : (0,0,0),     # beastiary
  w3g.ITEMS[b'ovln'] : (0,0,0),     # voodoo lounge
  w3g.ITEMS[b'obar'] : (0,0,0),     # orc barracks
  w3g.ITEMS[b'otrb'] : (0,0,0),     # orc burrow
  w3g.ITEMS[b'owtw'] : (0,0,0),     # watch tower
                          # war mill missing
  w3g.ITEMS[b'oalt'] : (0,0,0),     # altar of storms
  w3g.ITEMS[b'Roaa'] : (0,0,0),     # orc artillery
  w3g.ITEMS[b'Roar'] : (0,0,0),     # unit armor
  w3g.ITEMS[b'Robf'] : (0,0,0),     # burning oil
  w3g.ITEMS[b'Robk'] : (0,0,0),     # berserker
  w3g.ITEMS[b'Robs'] : (0,0,0),     # berserker strength
  w3g.ITEMS[b'Roch'] : (0,0,0),     # chaos
  w3g.ITEMS[b'Roen'] : (0,0,0),     # ensnare
  w3g.ITEMS[b'Rolf'] : (0,0,0),     # liquid fire
  w3g.ITEMS[b'Rome'] : (0,0,0),     # melee weapons
  w3g.ITEMS[b'Ropg'] : (0,0,0),     # pillage
  w3g.ITEMS[b'Rora'] : (0,0,0),     # ranged weapons
  w3g.ITEMS[b'Rorb'] : (0,0,0),     # reinforced defenses
  w3g.ITEMS[b'Rosp'] : (0,0,0),     # spiked barricades
  w3g.ITEMS[b'Rost'] : (0,0,0),     # shaman training
  w3g.ITEMS[b'Rotr'] : (0,0,0),     # troll regeneration
  w3g.ITEMS[b'Rovs'] : (0,0,0),     # envenomed spears
  w3g.ITEMS[b'Rowd'] : (0,0,0),     # witch doctor training
  w3g.ITEMS[b'Rows'] : (0,0,0),     # pulverize
  w3g.ITEMS[b'Rowt'] : (0,0,0),     # spirit walker training
  # night elf:
  w3g.ITEMS[b'Edem'] : (0,0,0),     # demon hunter
  w3g.ITEMS[b'Ekee'] : (0,0,0),     # keeper of the grove
  w3g.ITEMS[b'Emoo'] : (0,0,0),     # priestess of the moon
  w3g.ITEMS[b'Ewar'] : (0,0,0),     # warden
  w3g.ITEMS[b'ewsp'] : (0,0,0),     # wisp
  w3g.ITEMS[b'earc'] : (0,0,0),     # archer
  w3g.ITEMS[b'esen'] : (0,0,0),     # huntress
  w3g.ITEMS[b'edry'] : (0,0,0),     # dryad
  w3g.ITEMS[b'edoc'] : (0,0,0),     # druid of the claw
  w3g.ITEMS[b'emtg'] : (0,0,0),     # mountain giant
  w3g.ITEMS[b'ehip'] : (0,0,0),     # hippogryph
  w3g.ITEMS[b'edot'] : (0,0,0),     # druid of the talon
  w3g.ITEMS[b'efdr'] : (0,0,0),     # faerie dragon
  w3g.ITEMS[b'echm'] : (0,0,0),     # chimera
  w3g.ITEMS[b'ehpr'] : (0,0,0),     # hippogryph rider
  w3g.ITEMS[b'ebal'] : (0,0,0),     # glaive thrower
  w3g.ITEMS[b'etol'] : (0,0,0),     # tree of life
  w3g.ITEMS[b'etoa'] : (0,0,0),     # tree of ages
  w3g.ITEMS[b'etoe'] : (0,0,0),     # tree of eternity
  w3g.ITEMS[b'eaom'] : (0,0,0),     # ancient of war
  w3g.ITEMS[b'emow'] : (0,0,0),     # moon well
  w3g.ITEMS[b'eate'] : (0,0,0),     # altar of elders
  w3g.ITEMS[b'eden'] : (0,0,0),     # ancient of wonders
  w3g.ITEMS[b'edob'] : (0,0,0),     # hunters hall
  w3g.ITEMS[b'etrp'] : (0,0,0),     # ancient protector
  w3g.ITEMS[b'eaow'] : (0,0,0),     # ancient of wind
  w3g.ITEMS[b'eaoe'] : (0,0,0),     # ancient of lore
  w3g.ITEMS[b'edos'] : (0,0,0),     # chimera roost
  w3g.ITEMS[b'Recb'] : (0,0,0),     # corrosive breath
  w3g.ITEMS[b'Redc'] : (0,0,0),     # druid of the claw
  w3g.ITEMS[b'Redt'] : (0,0,0),     # druid of the talon
  w3g.ITEMS[b'Reeb'] : (0,0,0),     # mark of the claw
  w3g.ITEMS[b'Reec'] : (0,0,0),     # mark of the talon
  w3g.ITEMS[b'Rehs'] : (0,0,0),     # hardened skin
  w3g.ITEMS[b'Reht'] : (0,0,0),     # hippogryph taming
  w3g.ITEMS[b'Reib'] : (0,0,0),     # improved bows
  w3g.ITEMS[b'Rema'] : (0,0,0),     # moon armor
  w3g.ITEMS[b'Remg'] : (0,0,0),     # moon glaive
  w3g.ITEMS[b'Remk'] : (0,0,0),     # marksmanship
  w3g.ITEMS[b'Renb'] : (0,0,0),     # natures blessing
  w3g.ITEMS[b'Repd'] : (0,0,0),     # vorpal blades
  w3g.ITEMS[b'Rerh'] : (0,0,0),     # reinforced hides
  w3g.ITEMS[b'Rers'] : (0,0,0),     # resistant skin
  w3g.ITEMS[b'Resc'] : (0,0,0),     # sentinel
  w3g.ITEMS[b'Resi'] : (0,0,0),     # abolish magic
  w3g.ITEMS[b'Resm'] : (0,0,0),     # strength of the moon
  w3g.ITEMS[b'Resw'] : (0,0,0),     # strength of the wild
  w3g.ITEMS[b'Reuv'] : (0,0,0),     # ultravision
  w3g.ITEMS[b'Rews'] : (0,0,0),     # well sprint  
  # undead:
  w3g.ITEMS[b'Udea'] : (0,0,0),     # death knight
  w3g.ITEMS[b'Ulic'] : (0,0,0),     # lich
  w3g.ITEMS[b'Ucrl'] : (0,0,0),     # crypt lord
  w3g.ITEMS[b'Udre'] : (0,0,0),     # dread lord
  w3g.ITEMS[b'uaco'] : (0,0,0),     # acolyte
  w3g.ITEMS[b'ugho'] : (0,0,0),     # ghoul
  w3g.ITEMS[b'ucry'] : (0,0,0),     # crypt fiend
  w3g.ITEMS[b'ugar'] : (0,0,0),     # gargoyle
  w3g.ITEMS[b'uabo'] : (0,0,0),     # abomination
  w3g.ITEMS[b'umtw'] : (0,0,0),     # meat wagon
  w3g.ITEMS[b'uobs'] : (0,0,0),     # obsidian statue
  w3g.ITEMS[b'ubsp'] : (0,0,0),     # destroyer
  w3g.ITEMS[b'unec'] : (0,0,0),     # necromancer
  w3g.ITEMS[b'uban'] : (0,0,0),     # banshee
  w3g.ITEMS[b'ushd'] : (0,0,0),     # shade
  w3g.ITEMS[b'ufro'] : (0,0,0),     # frost wyrm
  w3g.ITEMS[b'uaod'] : (0,0,0),     # altar of darkness
  w3g.ITEMS[b'uzig'] : (0,0,0),     # ziggurat
  w3g.ITEMS[b'ugrv'] : (0,0,0),     # graveyard
  w3g.ITEMS[b'unpl'] : (0,0,0),     # necropolis
  w3g.ITEMS[b'usep'] : (0,0,0),     # crypt
  w3g.ITEMS[b'uzg2'] : (0,0,0),     # nerubian tower
  w3g.ITEMS[b'uzg1'] : (0,0,0),     # spirit tower
  w3g.ITEMS[b'utod'] : (0,0,0),     # temple of the damned
  w3g.ITEMS[b'uslh'] : (0,0,0),     # slaughterhouse
  w3g.ITEMS[b'utom'] : (0,0,0),     # tomb of relics
  w3g.ITEMS[b'usap'] : (0,0,0),     # sacrificial pit
  w3g.ITEMS[b'unpl'] : (0,0,0),     # necropolis
  w3g.ITEMS[b'unp1'] : (0,0,0),     # halls of the dead
  w3g.ITEMS[b'unp2'] : (0,0,0),     # black citadel
  w3g.ITEMS[b'ubon'] : (0,0,0),     # boneyard
  w3g.ITEMS[b'ugol'] : (0,0,0),     # haunted goldmine
  w3g.ITEMS[b'Ruab'] : (0,0,0),     # abom
  w3g.ITEMS[b'Ruac'] : (0,0,0),     # cannibalize
  w3g.ITEMS[b'Ruar'] : (0,0,0),     # unholy armor
  w3g.ITEMS[b'Ruax'] : (0,0,0),     # abom expl
  w3g.ITEMS[b'Ruba'] : (0,0,0),     # banshee training
  w3g.ITEMS[b'Rubu'] : (0,0,0),     # burrow
  w3g.ITEMS[b'Rucr'] : (0,0,0),     # creature carapace
  w3g.ITEMS[b'Ruex'] : (0,0,0),     # exhume corpses
  w3g.ITEMS[b'Rufb'] : (0,0,0),     # freezing breath
  w3g.ITEMS[b'Rugf'] : (0,0,0),     # ghoul frenzy
  w3g.ITEMS[b'Rume'] : (0,0,0),     # unholy strength
  w3g.ITEMS[b'Rump'] : (0,0,0),     # meat wagon
  w3g.ITEMS[b'Rune'] : (0,0,0),     # necromancer training
  w3g.ITEMS[b'Rupc'] : (0,0,0),     # disease cloud
  w3g.ITEMS[b'Rura'] : (0,0,0),     # creature attack
  w3g.ITEMS[b'Rurs'] : (0,0,0),     # sacrifice
  w3g.ITEMS[b'Rusf'] : (0,0,0),     # stone form
  w3g.ITEMS[b'Rusl'] : (0,0,0),     # skeletal longevity
  w3g.ITEMS[b'Rusm'] : (0,0,0),     # skeletal mastery
  w3g.ITEMS[b'Rusp'] : (0,0,0),     # destroyer form
  w3g.ITEMS[b'Ruwb'] : (0,0,0),     # Web  
  # other:
  w3g.ITEMS[b'Nngs'] : (0,0,0),     # naga sea witch
  w3g.ITEMS[b'Nbrn'] : (0,0,0),     # dark ranger
  w3g.ITEMS[b'Npbm'] : (0,0,0),     # pandaren brewmaster
  w3g.ITEMS[b'Nbst'] : (0,0,0),     # beastmaster
  w3g.ITEMS[b'Npld'] : (0,0,0),     # pit lord
  w3g.ITEMS[b'Ntin'] : (0,0,0),     # goblin tinker
  w3g.ITEMS[b'Nfir'] : (0,0,0),     # firelord
  w3g.ITEMS[b'Nalc'] : (0,0,0),     # goblin alchemist
  
  w3g.ITEMS[b'amrc'] : (0,0,0),     # amulet of recall
  w3g.ITEMS[b'ankh'] : (0,0,0),     # ankh of reincarnation
  w3g.ITEMS[b'belv'] : (0,0,0),     # boots of quel\'thalas +6
  w3g.ITEMS[b'bgst'] : (0,0,0),     # belt of giant strength +6
  w3g.ITEMS[b'bspd'] : (0,0,0),     # boots of speed
  w3g.ITEMS[b'ccmd'] : (0,0,0),     # scepter of mastery
  w3g.ITEMS[b'ciri'] : (0,0,0),     # robe of the magi +6
  w3g.ITEMS[b'ckng'] : (0,0,0),     # crown of kings +5
  w3g.ITEMS[b'clsd'] : (0,0,0),     # cloak of shadows
  w3g.ITEMS[b'crys'] : (0,0,0),     # crystal ball
  w3g.ITEMS[b'desc'] : (0,0,0),     # kelen's dagger of escape
  w3g.ITEMS[b'gemt'] : (0,0,0),     # gem of true seeing
  w3g.ITEMS[b'gobm'] : (0,0,0),     # goblin land mines
  w3g.ITEMS[b'gsou'] : (0,0,0),     # soul gem
  w3g.ITEMS[b'guvi'] : (0,0,0),     # glyph of ultravision
  w3g.ITEMS[b'gfor'] : (0,0,0),     # glyph of fortification
  w3g.ITEMS[b'soul'] : (0,0,0),     # soul
  w3g.ITEMS[b'mdpb'] : (0,0,0),     # medusa pebble
  w3g.ITEMS[b'rag1'] : (0,0,0),     # slippers of agility +3
  w3g.ITEMS[b'rat3'] : (0,0,0),     # claws of attack +3
  w3g.ITEMS[b'rin1'] : (0,0,0),     # mantle of intelligence +3
  w3g.ITEMS[b'rde1'] : (0,0,0),     # ring of protection +2
  w3g.ITEMS[b'rde2'] : (0,0,0),     # ring of protection +3
  w3g.ITEMS[b'rde3'] : (0,0,0),     # ring of protection +4
  w3g.ITEMS[b'rhth'] : (0,0,0),     # khadgar's gem of health
  w3g.ITEMS[b'rst1'] : (0,0,0),     # gauntlets of ogre strength +3
  w3g.ITEMS[b'ofir'] : (0,0,0),     # orb of fire
  w3g.ITEMS[b'ofro'] : (0,0,0),     # orb of frost
  w3g.ITEMS[b'olig'] : (0,0,0),     # orb of lightning
  w3g.ITEMS[b'oli2'] : (0,0,0),     # orb of lightning
  w3g.ITEMS[b'oven'] : (0,0,0),     # orb of venom
  w3g.ITEMS[b'odef'] : (0,0,0),     # orb of darkness
  w3g.ITEMS[b'ocor'] : (0,0,0),     # orb of corruption
  w3g.ITEMS[b'pdiv'] : (0,0,0),     # potion of divinity
  w3g.ITEMS[b'phea'] : (0,0,0),     # potion of healing
  w3g.ITEMS[b'pghe'] : (0,0,0),     # potion of greater healing
  w3g.ITEMS[b'pinv'] : (0,0,0),     # potion of invisibility
  w3g.ITEMS[b'pgin'] : (0,0,0),     # potion of greater invisibility
  w3g.ITEMS[b'pman'] : (0,0,0),     # potion of mana
  w3g.ITEMS[b'pgma'] : (0,0,0),     # potion of greater mana
  w3g.ITEMS[b'pnvu'] : (0,0,0),     # potion of invulnerability
  w3g.ITEMS[b'pnvl'] : (0,0,0),     # potion of lesser invulnerability
  w3g.ITEMS[b'pres'] : (0,0,0),     # potion of restoration
  w3g.ITEMS[b'pspd'] : (0,0,0),     # potion of speed
  w3g.ITEMS[b'rlif'] : (0,0,0),     # ring of regeneration
  w3g.ITEMS[b'rwiz'] : (0,0,0),     # sobi mask
  w3g.ITEMS[b'sfog'] : (0,0,0),     # horn of the clouds
  w3g.ITEMS[b'shea'] : (0,0,0),     # scroll of healing
  w3g.ITEMS[b'sman'] : (0,0,0),     # scroll of mana
  w3g.ITEMS[b'spro'] : (0,0,0),     # scroll of protection
  w3g.ITEMS[b'sres'] : (0,0,0),     # scroll of restoration
  w3g.ITEMS[b'ssil'] : (0,0,0),     # staff of silence
  w3g.ITEMS[b'stwp'] : (0,0,0),     # scroll of town portal
  w3g.ITEMS[b'tels'] : (0,0,0),     # goblin night scope
  w3g.ITEMS[b'tdex'] : (0,0,0),     # tome of agility
  w3g.ITEMS[b'texp'] : (0,0,0),     # tome of experience
  w3g.ITEMS[b'tint'] : (0,0,0),     # tome of intelligence
  w3g.ITEMS[b'tkno'] : (0,0,0),     # tome of power
  w3g.ITEMS[b'tstr'] : (0,0,0),     # tome of strength
  w3g.ITEMS[b'ward'] : (0,0,0),     # warsong battle drums
  w3g.ITEMS[b'will'] : (0,0,0),     # wand of illusion
  w3g.ITEMS[b'wneg'] : (0,0,0),     # wand of negation
  w3g.ITEMS[b'rdis'] : (0,0,0),     # rune of dispel magic
  w3g.ITEMS[b'rwat'] : (0,0,0),     # rune of the watcher
  w3g.ITEMS[b'fgrd'] : (0,0,0),     # red drake egg
  w3g.ITEMS[b'fgrg'] : (0,0,0),     # stone token
  w3g.ITEMS[b'fgdg'] : (0,0,0),     # demonic figurine
  w3g.ITEMS[b'fgfh'] : (0,0,0),     # spiked collar
  w3g.ITEMS[b'fgsk'] : (0,0,0),     # book of the dead
  w3g.ITEMS[b'engs'] : (0,0,0),     # enchanted gemstone
  w3g.ITEMS[b'k3m1'] : (0,0,0),     # mooncrystal
  w3g.ITEMS[b'modt'] : (0,0,0),     # mask of death
  w3g.ITEMS[b'sand'] : (0,0,0),     # scroll of animate dead
  w3g.ITEMS[b'srrc'] : (0,0,0),     # scroll of resurrection
  w3g.ITEMS[b'sror'] : (0,0,0),     # scroll of the beast
  w3g.ITEMS[b'infs'] : (0,0,0),     # inferno stone
  w3g.ITEMS[b'shar'] : (0,0,0),     # ice shard
  w3g.ITEMS[b'wild'] : (0,0,0),     # amulet of the wild
  w3g.ITEMS[b'wswd'] : (0,0,0),     # sentry wards
  w3g.ITEMS[b'whwd'] : (0,0,0),     # healing wards
  w3g.ITEMS[b'wlsd'] : (0,0,0),     # wand of lightning shield
  w3g.ITEMS[b'wcyc'] : (0,0,0),     # wand of the wind
  w3g.ITEMS[b'rnec'] : (0,0,0),     # rod of necromancy
  w3g.ITEMS[b'pams'] : (0,0,0),     # anti-magic potion
  w3g.ITEMS[b'clfm'] : (0,0,0),     # cloak of flames
  w3g.ITEMS[b'evtl'] : (0,0,0),     # talisman of evasion
  w3g.ITEMS[b'nspi'] : (0,0,0),     # necklace of spell immunity
  w3g.ITEMS[b'lhst'] : (0,0,0),     # the lion horn of stormwind
  w3g.ITEMS[b'kpin'] : (0,0,0),     # khadgar's pipe of insight
  w3g.ITEMS[b'sbch'] : (0,0,0),     # scourge bone chimes
  w3g.ITEMS[b'afac'] : (0,0,0),     # alleria's flute of accuracy
  w3g.ITEMS[b'ajen'] : (0,0,0),     # ancient janggo of endurance
  w3g.ITEMS[b'lgdh'] : (0,0,0),     # legion doom-horn
  w3g.ITEMS[b'hcun'] : (0,0,0),     # hood of cunning
  w3g.ITEMS[b'mcou'] : (0,0,0),     # medallion of courage
  w3g.ITEMS[b'hval'] : (0,0,0),     # helm of valor
  w3g.ITEMS[b'cnob'] : (0,0,0),     # circlet of nobility
  w3g.ITEMS[b'prvt'] : (0,0,0),     # periapt of vitality
  w3g.ITEMS[b'tgxp'] : (0,0,0),     # tome of greater experience
  w3g.ITEMS[b'mnst'] : (0,0,0),     # mana stone
  w3g.ITEMS[b'hlst'] : (0,0,0),     # health stone
  w3g.ITEMS[b'tpow'] : (0,0,0),     # tome of knowledge
  w3g.ITEMS[b'tst2'] : (0,0,0),     # tome of strength +2
  w3g.ITEMS[b'tin2'] : (0,0,0),     # tome of intelligence +2
  w3g.ITEMS[b'tdx2'] : (0,0,0),     # tome of agility +2
  w3g.ITEMS[b'rde0'] : (0,0,0),     # ring of protection +1
  w3g.ITEMS[b'rde4'] : (0,0,0),     # ring of protection +5
  w3g.ITEMS[b'rat6'] : (0,0,0),     # claws of attack +6
  w3g.ITEMS[b'rat9'] : (0,0,0),     # claws of attack +9
  w3g.ITEMS[b'ratc'] : (0,0,0),     # claws of attack +12
  w3g.ITEMS[b'ratf'] : (0,0,0),     # claws of attack +15
  w3g.ITEMS[b'manh'] : (0,0,0),     # manual of health
  w3g.ITEMS[b'pmna'] : (0,0,0),     # pendant of mana
  w3g.ITEMS[b'penr'] : (0,0,0),     # pendant of energy
  w3g.ITEMS[b'gcel'] : (0,0,0),     # gloves of haste
  w3g.ITEMS[b'totw'] : (0,0,0),     # talisman of the wild
  w3g.ITEMS[b'phlt'] : (0,0,0),     # phat lewt
  w3g.ITEMS[b'gopr'] : (0,0,0),     # glyph of purification
  w3g.ITEMS[b'ches'] : (0,0,0),     # cheese
  w3g.ITEMS[b'mlst'] : (0,0,0),     # maul of strength
  w3g.ITEMS[b'rnsp'] : (0,0,0),     # ring of superiority
  w3g.ITEMS[b'brag'] : (0,0,0),     # bracer of agility
  w3g.ITEMS[b'sksh'] : (0,0,0),     # skull shield
  w3g.ITEMS[b'vddl'] : (0,0,0),     # voodoo doll
  w3g.ITEMS[b'sprn'] : (0,0,0),     # spider ring
  w3g.ITEMS[b'tmmt'] : (0,0,0),     # totem of might
  w3g.ITEMS[b'anfg'] : (0,0,0),     # ancient figurine
  w3g.ITEMS[b'lnrn'] : (0,0,0),     # lion\'s ring
  w3g.ITEMS[b'iwbr'] : (0,0,0),     # ironwood branch
  w3g.ITEMS[b'jdrn'] : (0,0,0),     # jade ring
  w3g.ITEMS[b'drph'] : (0,0,0),     # druid pouch
  w3g.ITEMS[b'hslv'] : (0,0,0),     # healing salve
  w3g.ITEMS[b'pclr'] : (0,0,0),     # clarity potion
  w3g.ITEMS[b'plcl'] : (0,0,0),     # lesser clarity potion
  w3g.ITEMS[b'rej1'] : (0,0,0),     # minor replenishment potion
  w3g.ITEMS[b'rej2'] : (0,0,0),     # lesser replenishment potion
  w3g.ITEMS[b'rej3'] : (0,0,0),     # replenishment potion
  w3g.ITEMS[b'rej4'] : (0,0,0),     # greater replenishment potion
  w3g.ITEMS[b'rej5'] : (0,0,0),     # lesser scroll of replenishment
  w3g.ITEMS[b'rej6'] : (0,0,0),     # greater scroll of replenishment
  w3g.ITEMS[b'sreg'] : (0,0,0),     # scroll of regeneration
  w3g.ITEMS[b'gold'] : (0,0,0),     # gold coins
  w3g.ITEMS[b'lmbr'] : (0,0,0),     # bundle of lumber
  w3g.ITEMS[b'fgun'] : (0,0,0),     # flare gun
  w3g.ITEMS[b'pomn'] : (0,0,0),     # potion of omniscience
  w3g.ITEMS[b'gomn'] : (0,0,0),     # glyph of omniscience
  w3g.ITEMS[b'wneu'] : (0,0,0),     # wand of neutralization
  w3g.ITEMS[b'silk'] : (0,0,0),     # spider silk broach
  w3g.ITEMS[b'lure'] : (0,0,0),     # monster lure
  w3g.ITEMS[b'skul'] : (0,0,0),     # sacrificial skull
  w3g.ITEMS[b'moon'] : (0,0,0),     # moonstone
  w3g.ITEMS[b'brac'] : (0,0,0),     # runed bracers
  w3g.ITEMS[b'vamp'] : (0,0,0),     # vampiric potion
  w3g.ITEMS[b'woms'] : (0,0,0),     # wand of mana stealing
  w3g.ITEMS[b'tcas'] : (0,0,0),     # tiny castle
  w3g.ITEMS[b'tgrh'] : (0,0,0),     # tiny great hall
  w3g.ITEMS[b'tsct'] : (0,0,0),     # ivory tower
  w3g.ITEMS[b'wshs'] : (0,0,0),     # wand of shadowsight
  w3g.ITEMS[b'tret'] : (0,0,0),     # tome of retraining
  w3g.ITEMS[b'sneg'] : (0,0,0),     # staff of negation
  w3g.ITEMS[b'stel'] : (0,0,0),     # staff of teleportation
  w3g.ITEMS[b'spre'] : (0,0,0),     # staff of preservation
  w3g.ITEMS[b'mcri'] : (0,0,0),     # mechanical critter
  w3g.ITEMS[b'spsh'] : (0,0,0),     # amulet of spell shield
  w3g.ITEMS[b'sbok'] : (0,0,0),     # spell book
  w3g.ITEMS[b'ssan'] : (0,0,0),     # staff of sanctuary
  w3g.ITEMS[b'shas'] : (0,0,0),     # scroll of speed
  w3g.ITEMS[b'dust'] : (0,0,0),     # dust of appearance
  w3g.ITEMS[b'oslo'] : (0,0,0),     # orb of slow
  w3g.ITEMS[b'dsum'] : (0,0,0),     # diamond of summoning
  w3g.ITEMS[b'sor1'] : (0,0,0),     # shadow orb +1
  w3g.ITEMS[b'sor2'] : (0,0,0),     # shadow orb +2
  w3g.ITEMS[b'sor3'] : (0,0,0),     # shadow orb +3
  w3g.ITEMS[b'sor4'] : (0,0,0),     # shadow orb +4
  w3g.ITEMS[b'sor5'] : (0,0,0),     # shadow orb +5
  w3g.ITEMS[b'sor6'] : (0,0,0),     # shadow orb +6
  w3g.ITEMS[b'sor7'] : (0,0,0),     # shadow orb +7
  w3g.ITEMS[b'sor8'] : (0,0,0),     # shadow orb +8
  w3g.ITEMS[b'sor9'] : (0,0,0),     # shadow orb +9
  w3g.ITEMS[b'sora'] : (0,0,0),     # shadow orb +10
  w3g.ITEMS[b'sorf'] : (0,0,0),     # shadow orb fragment
  w3g.ITEMS[b'fwss'] : (0,0,0),     # frost wyrm skull shield
  w3g.ITEMS[b'ram1'] : (0,0,0),     # ring of the archmagi
  w3g.ITEMS[b'ram2'] : (0,0,0),     # ring of the archmagi
  w3g.ITEMS[b'ram3'] : (0,0,0),     # ring of the archmagi
  w3g.ITEMS[b'ram4'] : (0,0,0),     # ring of the archmagi
  w3g.ITEMS[b'shtm'] : (0,0,0),     # shamanic totem
  w3g.ITEMS[b'shwd'] : (0,0,0),     # shimmerweed
  w3g.ITEMS[b'btst'] : (0,0,0),     # battle standard
  w3g.ITEMS[b'skrt'] : (0,0,0),     # skeletal artifact
  w3g.ITEMS[b'thle'] : (0,0,0),     # thunder lizard egg
  w3g.ITEMS[b'sclp'] : (0,0,0),     # secret level powerup
  w3g.ITEMS[b'gldo'] : (0,0,0),     # orb of kil'jaeden
  w3g.ITEMS[b'tbsm'] : (0,0,0),     # tiny blacksmith
  w3g.ITEMS[b'tfar'] : (0,0,0),     # tiny farm
  w3g.ITEMS[b'tlum'] : (0,0,0),     # tiny lumber mill
  w3g.ITEMS[b'tbar'] : (0,0,0),     # tiny barracks
  w3g.ITEMS[b'tbak'] : (0,0,0),     # tiny altar of kings
  w3g.ITEMS[b'mgtk'] : (0,0,0),     # magic key chain
  w3g.ITEMS[b'stre'] : (0,0,0),     # staff of reanimation
  w3g.ITEMS[b'horl'] : (0,0,0),     # sacred relic
  w3g.ITEMS[b'hbth'] : (0,0,0),     # helm of battlethirst
  w3g.ITEMS[b'blba'] : (0,0,0),     # bladebane armor
  w3g.ITEMS[b'rugt'] : (0,0,0),     # runed gauntlets
  w3g.ITEMS[b'frhg'] : (0,0,0),     # firehand gauntlets
  w3g.ITEMS[b'gvsm'] : (0,0,0),     # gloves of spell mastery
  w3g.ITEMS[b'crdt'] : (0,0,0),     # crown of the deathlord
  w3g.ITEMS[b'arsc'] : (0,0,0),     # arcane scroll
  w3g.ITEMS[b'scul'] : (0,0,0),     # scroll of the unholy legion
  w3g.ITEMS[b'tmsc'] : (0,0,0),     # tome of sacrifices
  w3g.ITEMS[b'dtsb'] : (0,0,0),     # drek'thar's spellbook
  w3g.ITEMS[b'grsl'] : (0,0,0),     # grimoire of souls
  w3g.ITEMS[b'arsh'] : (0,0,0),     # arcanite shield
  w3g.ITEMS[b'shdt'] : (0,0,0),     # shield of the deathlord
  w3g.ITEMS[b'shhn'] : (0,0,0),     # shield of honor
  w3g.ITEMS[b'shen'] : (0,0,0),     # enchanted shield
  w3g.ITEMS[b'thdm'] : (0,0,0),     # thunderlizard diamond
  w3g.ITEMS[b'stpg'] : (0,0,0),     # clockwork penguin
  w3g.ITEMS[b'shrs'] : (0,0,0),     # shimmerglaze roast
  w3g.ITEMS[b'bfhr'] : (0,0,0),     # bloodfeather's heart
  w3g.ITEMS[b'cosl'] : (0,0,0),     # celestial orb of souls
  w3g.ITEMS[b'shcw'] : (0,0,0),     # shaman claws
  w3g.ITEMS[b'srbd'] : (0,0,0),     # searing blade
  w3g.ITEMS[b'frgd'] : (0,0,0),     # frostguard
  w3g.ITEMS[b'envl'] : (0,0,0),     # enchanted vial
  w3g.ITEMS[b'rump'] : (0,0,0),     # rusty mining pick
  w3g.ITEMS[b'mort'] : (0,0,0),     # mogrin's report
  w3g.ITEMS[b'srtl'] : (0,0,0),     # serathil
  w3g.ITEMS[b'stwa'] : (0,0,0),     # sturdy war axe
  w3g.ITEMS[b'klmm'] : (0,0,0),     # killmaim
  w3g.ITEMS[b'rots'] : (0,0,0),     # scepter of the sea
  w3g.ITEMS[b'axas'] : (0,0,0),     # ancestral staff
  w3g.ITEMS[b'mnsf'] : (0,0,0),     # mindstaff
  w3g.ITEMS[b'schl'] : (0,0,0),     # scepter of healing
  w3g.ITEMS[b'asbl'] : (0,0,0),     # assassin's blade
  w3g.ITEMS[b'kgal'] : (0,0,0),     # keg of ale
  w3g.ITEMS[b'dphe'] : (0,0,0),     # thunder phoenix egg
  w3g.ITEMS[b'dkfw'] : (0,0,0),     # keg of thunderwater
  w3g.ITEMS[b'dthb'] : (0,0,0),     # thunderbloom bulb
  }

class W3JSONEncoder(json.JSONEncoder):
  def default(self, o):
    return o.__dict__

class Ability:
  def __init__(self):
    self.name = ""
    self.level = 1
    self.used_recently_countdown = 0

class Hero:
  def __init__(self):
    self.name = ""                    # hero name
    self.revive_time_left = -1
    self.has_been_trained = False     # whether the hero has already been trained
    self.level = 0                    # hero level
    self.abilities = []               # will hold Ability objects
  
  def train_ability(self, ability_name):    
    for ability in self.abilities:
      if ability.name == ability_name:
        self.ability = min(ability.level + 1,3)
        self.level += 1
        return
    
    new_ability = Ability()
    new_ability.name = ability_name
    self.abilities.append(new_ability)
    self.level = min(self.level + 1,10)
  
  def is_alive(self):
    return self.revive_time_left <= 0

class PlayerState:
  def __init__(self):
    self.heroes = []             # will hold Hero objects
    self.current_action = ""
    self.current_apm = 0
    self.apm_action_buffer = []  # holds APM action times in last APM_INTERVAL ms 
    self.gold_spent = 0
    self.lumber_spent = 0
    self.last_actions = ["" for i in range(ACTIONS_SHOWN)]
    self.tier = 1
    self.tier_time_left = -1     # how long till next tier

class Player:
  def __init__(self):
    self.name = ""
    self.race = "human"
    self.state = PlayerState()

  def __str__(self):
    result = "player:" + self.name + "(" + self.race + ")"
    result += ";" + str(self.state)
    return result
  
  def add_action(self,action_string):
    self.state.last_actions.pop()
    self.state.last_actions = [action_string] + self.state.last_actions
  
  def cancel_untrained_heroes(self):
    self.state.heroes =  [hero for hero in self.state.heroes if hero.has_been_trained]
  
  def add_apm_action(self,apm_action):
    self.state.apm_action_buffer.append(APM_INTERVAL)
  
  def tome_of_retraining_used(self):
    #TODO
    pass
  
  def use_ability(self,ability_name):
    for hero in self.state.heroes:
      for ability in hero.abilities:
        if ability.name.lower() == ability_name.lower():
          ability.used_recently_countdown = RECENTLY_USED_COUNTDOWN
          return
  
  def has_hero(self, hero_name):
    return self.get_hero_by_name(hero_name) != None

  def get_hero_by_name(self, hero_name):
    for hero in self.state.heroes:
      if hero_name == hero.name:
        return hero
      
    return None
  
  def update(self, time_difference):
    apm_action_buffer = self.state.apm_action_buffer
    
    for position in range(len(apm_action_buffer)):
      apm_action_buffer[position] -= time_difference

    self.state.apm_action_buffer = [item for item in apm_action_buffer if item > 0]

    self.state.current_apm = len(apm_action_buffer) / float(APM_INTERVAL / 1000) * 60

    for hero in self.state.heroes:
      if hero.revive_time_left > 0:
        hero.revive_time_left = max(hero.revive_time_left - time_difference,-1)
      else:
        hero.has_been_trained = True
      
      for ability in hero.abilities:   
        if ability.used_recently_countdown > 0:
          ability.used_recently_countdown -= time_difference / float(TIME_STEP)

def get_players(replay_file):        # returns dict with players, key is the player id
  player_ids = Set()
  player_races = {}

  for event in replay_file.events:
    if event.apm:
      player_ids.add(event.player_id)
      
      if not event.player_id in player_races:
        player_races[event.player_id] = ""
      
      if len(player_races[event.player_id]) == 0 and type(event) is w3g.Ability:        
        if event.ability[0] == "h" or event.ability[:1] == "AH":
          player_races[event.player_id] = "human"
        elif event.ability[0] == "o" or event.ability[:1] == "AO":
          player_races[event.player_id] = "orc"
        elif event.ability[0] == "e" or event.ability[:1] == "AE":
          player_races[event.player_id] = "night elf"
        elif event.ability[0] == "u" or event.ability[:1] == "AU":
          player_races[event.player_id] = "undead"

  result = {}

  for player_id in player_ids:
    new_player = Player()
    new_player.name = replay_file.player_name(player_id)
    new_player.race = player_races[player_id]
    result[player_id] = new_player

  return result

def list_to_str(what_list,separator=","):
  result = ""
  
  first = True
  
  for item in what_list:
    if first:
      first = False
    else:
      result += separator
    
    result += str(item)

  return result

def get_trained_ability_name(ability_item):    # if the argument represents hero ability, (hero,ability) tuple is returned, otherwise None is returned
  helper_list = ability_item.split(":")
  
  if helper_list[0] == "Firelord":        # casing fix
    helper_list[0] = "FireLord"
  
  if len(helper_list) != 2 or (not helper_list[0] in HERO_STRINGS):
    return None
  
  return (helper_list[0],helper_list[1])
 
def get_used_ability(ability_item):            # if the argument represents used ability, ability string is returned, otherwise None is returned
  helper_list = ability_item.split(":")
  
  if len(helper_list) != 2 or helper_list[0].strip().lower() != "use ability":
    return None
  
  return helper_list[1][:helper_list[1].index("(")].strip()

def check_recordable_action(ability_item):     # checks if given ability is to be recorded, if so, returns string to be recorded, otherwise None
  if ability_item.find("Use item") >= 0:
    return "item used"
  elif ability_item.find("Revive hero") >= 0:
    return "revive hero (altar)"
  elif ability_item.find("Give item") >= 0:
    return "give item"
  elif ability_item.find("Use ability: kaboom") >= 0:
    return "kaboom (Goblin sapper)"  
  elif ability_item.find("Use ability: uproot") >= 0:
    return "uproot"  
  elif ability_item.find("Use ability: uproot") >= 0:
    return "uproot"  
  elif ability_item.find("Use ability: unsummon") >= 0:
    return "unsummon"  
  elif ability_item.find("hero on tavern") >= 0:
    return "revive hero (tavern)"  
  
def process_event_string(event_string):
  result = event_string
  
  helper_position = event_string.find("- ")
  
  if helper_position >= 0:
    result = event_string[helper_position + 2:]
  else:
    helper_position = event_string.find("> ")
  
    if helper_position >= 0:
      result = event_string[helper_position + 2:]
  
  if len(result) > 20:
    result = result[:20] + "..."
  
  return result

#==========================================================

if len(sys.argv) != 2:
  print("Expecting a filename argument.")
  quit()

replay_file = w3g.File(sys.argv[1])

players = get_players(replay_file)

last_update_time = -1 * TIME_STEP
last_event_time = 0

encoder = W3JSONEncoder()

for event in replay_file.events:
  while event.time > last_update_time:
    last_update_time += TIME_STEP
    print(str(last_update_time) + ":" + encoder.encode(players))

  time_difference = event.time - last_event_time
  last_event_time = event.time

  try:
    players[event.player_id].state.current_action = process_event_string(str(event))
  except Exception:
    pass
  
  for player_id in players:
    players[player_id].update(time_difference)
  
  
  if event.apm:
    players[event.player_id].add_apm_action(event)
      
  if type(event) is w3g.Ability or type(event) is w3g.AbilityPosition or type(event) is w3g.AbilityPositionObject:
    player = players[event.player_id]
    ability_item = w3g.ITEMS.get(event.ability,event.ability)
    trained_ability = get_trained_ability_name(ability_item)

    used_ability = get_used_ability(ability_item)
    
    if used_ability != None:
      player.use_ability(used_ability)

    if ability_item in ACTION_COSTS:
      player.add_action(ability_item)
    else:
      recordable = check_recordable_action(ability_item)
      
      if recordable != None:
        player.add_action(recordable)

    if trained_ability != None:
      player.get_hero_by_name(trained_ability[0]).train_ability(trained_ability[1])
    elif ability_item in HERO_STRINGS:     # hero training
      if not player.has_hero(ability_item) and len(player.state.heroes) < 3:    # training a new hero
        player.cancel_untrained_heroes()
        
        new_hero = Hero()
        new_hero.name = ability_item
        
        if not ability_item in NEUTRAL_HERO_STRINGS:                            # neutral heroes trained instantly 
          new_hero.revive_time_left = HERO_REVIVE_TIMES[0]
        
        player.state.heroes.append(new_hero)