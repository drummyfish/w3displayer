import w3g
from sets import Set
import sys
import json

TIME_STEP = 500             # time of periodic update, in miliseconds
ACTIONS_SHOWN = 5           # how many last player action to show
RECENTLY_USED_COUNTDOWN = 3 # for how many frames a recently used ability will be shown

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
  w3g.ITEMS[b'Nalc']
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
  w3g.ITEMS[b'Nalc'] : (0,0,0)      # goblin alchemist
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
    self.name = ""        # hero name
    self.revive_time_left = -1
    self.level = 0        # hero level
    self.abilities = []   # will hold Ability objects
  
  def train_ability(self, ability_name):    
    for ability in self.abilities:
      if ability.name == ability_name:
        ability.level += 1
        self.level += 1
        return
    
    new_ability = Ability()
    new_ability.name = ability_name
    self.abilities.append(new_ability)
    self.level += 1
  
  def is_alive(self):
    return self.revive_time_left <= 0

class PlayerState:
  def __init__(self):
    self.heroes = []      # will hold Hero objects
    self.gold_spent = 0
    self.lumber_spent = 0
    self.last_actions = ["" for i in range(ACTIONS_SHOWN)]

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
    for hero in self.state.heroes:
      if hero.revive_time_left > 0:
        hero.revive_time_left = max(hero.revive_time_left - time_difference,-1)
      
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
  
  if len(helper_list) != 2 or (not helper_list[0] in HERO_STRINGS):
    return None
  
  return (helper_list[0],helper_list[1])
 
def get_used_ability(ability_item):            # if the argument represents used ability, ability string is returned, otherwise None is returned
  helper_list = ability_item.split(":")
  
  if len(helper_list) != 2 or helper_list[0].strip().lower() != "use ability":
    return None
  
  return helper_list[1][:helper_list[1].index("(")].strip()

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
  
  for player_id in players:
    players[player_id].update(time_difference)
  
  if type(event) is w3g.Ability or type(event) is w3g.AbilityPosition or type(event) is w3g.AbilityPositionObject:
    player = players[event.player_id]
    ability_item = w3g.ITEMS.get(event.ability,event.ability)
    trained_ability = get_trained_ability_name(ability_item)

    used_ability = get_used_ability(ability_item)
    
    if used_ability != None:
      player.use_ability(used_ability)

    if ability_item in ACTION_COSTS:
      player.add_action(ability_item)

    if trained_ability != None:
      hero = player.get_hero_by_name(trained_ability[0])
      hero.train_ability(trained_ability[1])
    elif ability_item in HERO_STRINGS:     # hero training
      if not player.has_hero(ability_item):                   # training a new hero
        new_hero = Hero()
        new_hero.name = ability_item
        
        if not ability_item in NEUTRAL_HERO_STRINGS:          # neutral heroes trained instantly 
          new_hero.revive_time_left = HERO_REVIVE_TIMES[0]
        
        player.state.heroes.append(new_hero)
        
  #  print(e.time)
  #  print(w3g.ITEMS.get(e.ability, e.ability))