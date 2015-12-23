import w3g
from sets import Set
import sys
import json

TIME_STEP = 1000            # time of periodic update, in miliseconds
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

HUMAN_STRINGS = [      # some strings unique to human actions
  w3g.ITEMS[b'hpea'],
  w3g.ITEMS[b'AHab'],
  w3g.ITEMS[b'AHav'],
  w3g.ITEMS[b'AHbh'],
  w3g.ITEMS[b'AHbz'],
  w3g.ITEMS[b'AHmt'],
  w3g.ITEMS[b'AHpx'],
  w3g.ITEMS[b'AHtb'],
  w3g.ITEMS[b'AHwe'],
  w3g.ITEMS[b'npgf'],
  w3g.ITEMS[b'htow'],  
  w3g.ITEMS[b'halt'] 
  ]

ORC_STRINGS = [        # some strings unique to orc actions
  w3g.ITEMS[b'hpea'],
  w3g.ITEMS[b'AOae'],
  w3g.ITEMS[b'AOhx'],
  w3g.ITEMS[b'AOsf'],
  w3g.ITEMS[b'otrb'],
  w3g.ITEMS[b'ogre'],
  w3g.ITEMS[b'Obla'],
  w3g.ITEMS[b'Ofar'],
  w3g.ITEMS[b'oalt']
  ]

ELF_STRINGS = [        # some strings unique to night elf actions
  w3g.ITEMS[b'ewsp'],
  w3g.ITEMS[b'etoa'],
  w3g.ITEMS[b'Ewar'],
  w3g.ITEMS[b'eate'],
  w3g.ITEMS[b'emow'],
  w3g.ITEMS[b'esen'],
  w3g.ITEMS[b'Edem'],
  w3g.ITEMS[b'earc']
  ]

UNDEAD_STRINGS = [     # some strings unique to undead actions
  w3g.ITEMS[b'uaco'],
  w3g.ITEMS[b'unpl'],
  w3g.ITEMS[b'uzig'],
  w3g.ITEMS[b'Udea'],
  w3g.ITEMS[b'Ulic'],
  w3g.ITEMS[b'usep'],
  w3g.ITEMS[b'ugho'],
  w3g.ITEMS[b'AUdc']
  ]

ACTIONS_TO_SHOW_STRINGS = [
  # human:
  w3g.ITEMS[b'hpea'],
  w3g.ITEMS[b'hfoo'],
  w3g.ITEMS[b'hrif'],
  w3g.ITEMS[b'hkni'],
  w3g.ITEMS[b'hmpr'],
  w3g.ITEMS[b'hsor'],
  w3g.ITEMS[b'hspt'],
  w3g.ITEMS[b'hmtm'],
  w3g.ITEMS[b'hmtt'],
  w3g.ITEMS[b'hgry'],
  w3g.ITEMS[b'nws1'],
  w3g.ITEMS[b'htow'],
  w3g.ITEMS[b'hkee'],
  w3g.ITEMS[b'hcas'],
  w3g.ITEMS[b'npgf'],
  w3g.ITEMS[b'halt'],
  w3g.ITEMS[b'hvlt'],
  w3g.ITEMS[b'hars'],
  w3g.ITEMS[b'hbar'],
  w3g.ITEMS[b'hbla'],
  w3g.ITEMS[b'harm'],
  w3g.ITEMS[b'hatw'],
  w3g.ITEMS[b'hctw'],
  w3g.ITEMS[b'hgtw'],
  w3g.ITEMS[b'hlum'],
  w3g.ITEMS[b'hgra'],
  w3g.ITEMS[b'hwtw'],
  w3g.ITEMS[b'hhou'],
  # orc:
  w3g.ITEMS[b'opeo'],
  w3g.ITEMS[b'ogru'],
  w3g.ITEMS[b'ohun'],
  w3g.ITEMS[b'oshm'],
  w3g.ITEMS[b'odoc'],
  w3g.ITEMS[b'ospw'],
  w3g.ITEMS[b'orai'],
  w3g.ITEMS[b'okod'],
  w3g.ITEMS[b'ocat'],
  w3g.ITEMS[b'otbr'],
  w3g.ITEMS[b'otau'],
  w3g.ITEMS[b'ogre'],
  w3g.ITEMS[b'ostr'],
  w3g.ITEMS[b'ofrt'],
  w3g.ITEMS[b'osld'],
  w3g.ITEMS[b'otto'],
  w3g.ITEMS[b'obea'],
  w3g.ITEMS[b'ovln'],
  w3g.ITEMS[b'obar'],
  w3g.ITEMS[b'otrb'],
  w3g.ITEMS[b'owtw'],
  w3g.ITEMS[b'oalt'],
  # night elf:
  w3g.ITEMS[b'ewsp'],
  w3g.ITEMS[b'earc'],
  w3g.ITEMS[b'esen'],
  w3g.ITEMS[b'edry'],
  w3g.ITEMS[b'edoc'],
  w3g.ITEMS[b'emtg'],
  w3g.ITEMS[b'ehip'],
  w3g.ITEMS[b'edot'],
  w3g.ITEMS[b'efdr'],
  w3g.ITEMS[b'echm'],
  w3g.ITEMS[b'ehpr'],
  w3g.ITEMS[b'etol'],
  w3g.ITEMS[b'etoa'],
  w3g.ITEMS[b'etoe'],
  w3g.ITEMS[b'eaom'],
  w3g.ITEMS[b'emow'],
  w3g.ITEMS[b'eate'],
  w3g.ITEMS[b'eden'],
  w3g.ITEMS[b'edob'],
  w3g.ITEMS[b'etrp'],
  w3g.ITEMS[b'eaow'],
  w3g.ITEMS[b'eaoe'],
  w3g.ITEMS[b'edos'],
  # undead:
  w3g.ITEMS[b'uaco'],
  w3g.ITEMS[b'ugho'],
  w3g.ITEMS[b'ucry'],
  w3g.ITEMS[b'ugar'],
  w3g.ITEMS[b'uabo'],
  w3g.ITEMS[b'umtw'],
  w3g.ITEMS[b'uobs'],
  w3g.ITEMS[b'ubsp'],
  w3g.ITEMS[b'unec'],
  w3g.ITEMS[b'uban'],
  w3g.ITEMS[b'ushd'],
  w3g.ITEMS[b'ufro'],
  w3g.ITEMS[b'uaod'],
  w3g.ITEMS[b'uzig'],
  w3g.ITEMS[b'ugrv'],
  w3g.ITEMS[b'unpl'],
  w3g.ITEMS[b'usep'],
  w3g.ITEMS[b'uzg2'],
  w3g.ITEMS[b'uzg1'],
  w3g.ITEMS[b'utod'],
  w3g.ITEMS[b'uslh'],
  w3g.ITEMS[b'utom'],
  w3g.ITEMS[b'usap'],
  w3g.ITEMS[b'unp1'],
  w3g.ITEMS[b'unp2'],
  w3g.ITEMS[b'ubon']
  ]

ACTIONS_TO_SHOW_STRINGS += HERO_STRINGS

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
        ability_string = w3g.ITEMS.get(event.ability,event.ability)
        
        if ability_string in HUMAN_STRINGS:
          player_races[event.player_id] = "human"
        elif ability_string in ORC_STRINGS:
          player_races[event.player_id] = "orc"
        elif ability_string in ELF_STRINGS:
          player_races[event.player_id] = "night elf"
        elif ability_string in UNDEAD_STRINGS:
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

    if ability_item in ACTIONS_TO_SHOW_STRINGS:
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