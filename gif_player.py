# -*- coding: utf-8 -*-
#
#  This is a player that outputs gif animation that
#  can be used on web, in videos etc.
#
#  Miloslav Číž, 2015

from images2gif import writeGif
from PIL import Image, ImageFont, ImageDraw
import os
import sys
import shutil
import json
from sets import Set

IMAGE_SIZE = (200,400)

MARGIN_LEFT = 15

BACKGROUND_COLOR_HUMAN = (200,200,255)
BACKGROUND_COLOR_ORC = (200,255,200)
BACKGROUND_COLOR_NIGHT_ELF = (220,200,220)
BACKGROUND_COLOR_UNDEAD = (210,210,210)

VERTICAL_SPACE = 15

TMP_FOLDER_NAME = "tmp"

if not os.path.exists(TMP_FOLDER_NAME):
  os.makedirs(TMP_FOLDER_NAME)

player_names = Set()

with open(sys.argv[1]) as input_file:
  counter = 1
  
  for line in input_file:
    colon_position = line.index(":")
    line = line[colon_position + 1:]
    data = json.loads(line)
    
    for player_id in data:
      player = data[player_id]
      player_names.add(player["name"])

      if player["race"] == "orc":
        background_color = BACKGROUND_COLOR_ORC
      elif player["race"] == "human":
        background_color = BACKGROUND_COLOR_HUMAN
      elif player["race"] == "undead":
        background_color = BACKGROUND_COLOR_UNDEAD
      else:
        background_color = BACKGROUND_COLOR_NIGHT_ELF

      image = Image.new("RGBA",IMAGE_SIZE,background_color)

      draw = ImageDraw.Draw(image)
      
      font_big = ImageFont.truetype("./resources/OpenSans-Regular.ttf",20)
      draw.text((MARGIN_LEFT,VERTICAL_SPACE),str(player["name"]),(0,0,0),font=font_big)

      image.save(TMP_FOLDER_NAME + "/" + player["name"] + "_" + str(counter).zfill(8) + ".png", "PNG")
    
    counter += 1
    
    if counter == 20:
      break

# create the GIFs:

for player_name in player_names:
  file_names = sorted((fn for fn in os.listdir(TMP_FOLDER_NAME) if fn.endswith(".png") and fn.startswith(player_name)))

  images = [Image.open(TMP_FOLDER_NAME + "/" + fn) for fn in file_names]

  filename = player_name + ".gif"
  writeGif(filename, images, duration=0.2)

shutil.rmtree(TMP_FOLDER_NAME)








