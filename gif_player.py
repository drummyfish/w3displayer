# -*- coding: utf-8 -*-
#
#  This is a player that outputs gif animation that
#  can be used on web, in videos etc.
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

VERTICAL_SPACE = 5
BIG_FONT_SIZE = 20
MIDDLE_FONT_SIZE = 12
TMP_FOLDER_NAME = "tmp"
RESOURCES_FOLDER_NAME = "resources"

if not os.path.exists(TMP_FOLDER_NAME):
  os.makedirs(TMP_FOLDER_NAME)

player_names = Set()

with open(sys.argv[1]) as input_file:
  counter = 1
  
  font_big = ImageFont.truetype("./resources/OpenSans-Regular.ttf",BIG_FONT_SIZE)
  font_middle = ImageFont.truetype("./resources/OpenSans-Regular.ttf",MIDDLE_FONT_SIZE)

  image_names = sorted((fn for fn in os.listdir(RESOURCES_FOLDER_NAME) if fn.endswith(".png")))
  images = {}
  
  for image_name in image_names:
    images[image_name] = Image.open(RESOURCES_FOLDER_NAME + "/" + image_name,"r")
      
  for line in input_file:
    colon_position = line.index(":")
    line = line[colon_position + 1:]
    data = json.loads(line)
    
    for player_id in data:
      player = data[player_id]
      player_names.add(player["name"])
      y_position = 10

      if player["race"] == "orc":
        background_color = BACKGROUND_COLOR_ORC
        race_image = "race_orc.png"
      elif player["race"] == "human":
        background_color = BACKGROUND_COLOR_HUMAN
        race_image = "race_human.png"
      elif player["race"] == "undead":
        background_color = BACKGROUND_COLOR_UNDEAD
        race_image = "race_undead.png"
      else:
        background_color = BACKGROUND_COLOR_NIGHT_ELF
        race_image = "race_night_elf.png"

      image = Image.new("RGBA",IMAGE_SIZE,background_color)

      image.paste(images[race_image],(IMAGE_SIZE[0] - images[race_image].size[0] - 10,10))

      draw = ImageDraw.Draw(image)
      
      draw.text((MARGIN_LEFT,y_position),str(player["name"]),(0,0,0),font=font_big)
      y_position += BIG_FONT_SIZE + VERTICAL_SPACE

      draw.text((MARGIN_LEFT,y_position),"APM: " + str(player["state"]["current_apm"]),(0,0,0),font=font_middle)
      y_position += MIDDLE_FONT_SIZE + VERTICAL_SPACE
      
      draw.text((MARGIN_LEFT,y_position),str(player["state"]["current_action"]),(0,0,0),font=font_middle)     
      y_position += MIDDLE_FONT_SIZE + VERTICAL_SPACE
      
      draw.line((10,y_position + 10,IMAGE_SIZE[0] - 10,y_position + 10),fill=128)
      y_position += MIDDLE_FONT_SIZE + VERTICAL_SPACE
      
      for action in player["state"]["last_actions"]:
        draw.text((MARGIN_LEFT,y_position),action,(0,0,0),font=font_middle)     
        y_position += MIDDLE_FONT_SIZE + VERTICAL_SPACE
      
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








