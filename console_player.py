import sys
import time

SPEEDUP = 5.0

def time_to_string(time_in_ms):
  seconds = time_in_ms / 1000
  minutes = seconds / 60
  seconds = seconds % 60
  return str(minutes) + ":" + str(seconds)

with open(sys.argv[1]) as input_file:
  start_time = time.time()
  
  for line in input_file:
    line_split = line.split("|")
    
    next_time = int(line_split[0])
    
    while True:
      current_time = (time.time() - start_time) * 1000 * SPEEDUP
      
      time.sleep(0.2)     # give the CPU some rest
      
      if current_time >= next_time:
        break

    for i in range(50):   # print some vertical space 
      print("")
 
    print(time_to_string(next_time) + ":")
    
    for line_part in line_split[1:]:  
      line_part_split = line_part.split(";")
      first = True
      print("")
      
      for line_part_part in line_part_split:
        line_part_part_split = line_part_part.split(":")
        
        if line_part_part_split[0] == "gold spent" or line_part_part_split[0] == "lumber spent":
          continue       # these are not working yet
        elif line_part_part_split[0] == "player":
          print(line_part_part_split[1].replace("("," (") + ":")
        elif line_part_part_split[0] == "heroes":
          print("  " + line_part_part_split[0] + ":")
          
          line_part_part_split_split = line_part_part_split[1].split(",")
          
          for line_part_part_split_part in line_part_part_split_split:
            if len(line_part_part_split_part) == 0:
              continue
            
            string_to_print = "    "
            helper = line_part_part_split_part.split("(")
            string_to_print += helper[0] + " ("
            
            helper2 = helper[1][:-1].split("/")
            
            for i in range(len(helper2)):
              if i == 0:
                string_to_print += helper2[i]
              elif i == 1:
                if helper2[i][-2:] != "-1":
                  string_to_print += ", " + helper2[i]
                
                string_to_print += "): "
              else:
                if len(helper2[i]) == 0:
                  continue
                
                highlight = False
                
                if helper2[i][-1] == "*":
                  helper2[i] = helper2[i][:-1]
                  highlight = True
                
                helper2[i] = helper2[i].replace("-","(")
                helper2[i] += ")"
                
                if highlight:
                  helper2[i] = helper2[i] + " <-- used"
                
                string_to_print += "\n      " + helper2[i]
            
            print(string_to_print)
            
        elif line_part_part_split[0] == "last actions":
          line_part_part_split_split = line_part_part_split[1].split(",")
          print("  " + line_part_part_split[0] + ":")
          
          for line_part_part_split_part in line_part_part_split_split:
            print("    " + line_part_part_split_part)
        else:
          string_to_print = "  "
        
          if first:
            first = False
          else:
            string_to_print += "  "     # indent
      
          string_to_print += line_part_part_split[0] + ": " + line_part_part_split[1]
      
          print(string_to_print)