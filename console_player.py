import sys
import time
import json

SPEEDUP = 5.0

def time_to_string(time_in_ms):
  seconds = time_in_ms / 1000
  minutes = seconds / 60
  seconds = seconds % 60
  return str(minutes) + ":" + str(seconds)

with open(sys.argv[1]) as input_file:
  start_time = time.time()
  
  for line in input_file:
    colon_position = line.index(":")
    next_time = int(line[:colon_position])
    line = line[colon_position + 1:]
    
    while True:
      current_time = (time.time() - start_time) * 1000 * SPEEDUP
      time.sleep(0.2)     # give the CPU some rest
      
      if current_time >= next_time:
        break

    for i in range(50):   # print some vertical space 
      print("")
      
    data = json.loads(line)
    
    print(time_to_string(next_time) + ":")
    
    for player_id in data:
      player = data[player_id]
      print("")
      print(player["name"] + " (" + player["race"] + "):")
      print("  current action: " + player["state"]["current_action"])
      print("  current apm: " + str(player["state"]["current_apm"]))
      print("  heroes:")
      
      for hero in player["state"]["heroes"]:
        helper_string = "    "
        helper_string += hero["name"]
        helper_string += " " + str(max(1,hero["level"]))
        
        if hero["revive_time_left"] > 0:
          helper_string += ", revives: " + time_to_string(hero["revive_time_left"])
          
        helper_string += ":"
        
        print(helper_string)
        
        for ability in hero["abilities"]:
          helper_string = "      "
          helper_string += ability["name"]
          helper_string += " " + str(ability["level"])
          
          if ability["used_recently_countdown"] > 0:
            helper_string += " <-- used"
          
          print(helper_string)
        
      print("  last actions:")
      
      for action in player["state"]["last_actions"]:
        print("    " + action)
      
