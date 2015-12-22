import sys
import time

SPEEDUP = 1.0

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
      
      for line_part_part in line_part_split:
        string_to_print = ""
        
        if first:
          first = False
        else:
          string_to_print += "  "     # indent
      
        string_to_print += line_part_part
        print(string_to_print)