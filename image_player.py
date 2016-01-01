# -*- coding: utf-8 -*-
#
#  This is a player that outputs image representing the replay
#  as a timeline.
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

from PIL import Image, ImageFont, ImageDraw
import os
import sys
import shutil
import json
from sets import Set

LEFT_BORDER = 30                      # in pixels
PLAYER_PANEL_HEIGHT = 100             # in pixels

BACKGROUND_COLOR_HUMAN = (200,200,255)
BACKGROUND_COLOR_ORC = (200,255,200)
BACKGROUND_COLOR_NIGHT_ELF = (220,200,220)
BACKGROUND_COLOR_UNDEAD = (210,210,210)

RESOURCES_FOLDER_NAME = "resources"

SAMPLING_PERIOD = 3000                # for one pixel, in ms

with open(sys.argv[1]) as input_file:
  counter = 1
  
  font = ImageFont.truetype("./resources/OpenSans-Regular.ttf",10)
    
  lines = []
  
  for line in input_file:
    colon_position = line.index(":")
    lines.append((int(line[:colon_position]),line[colon_position + 1:]))
  
  number_of_players = len(json.loads(lines[0][1]))
  
  image_size = (LEFT_BORDER + int(lines[-1][0] / SAMPLING_PERIOD),PLAYER_PANEL_HEIGHT * number_of_players)
  image = Image.new("RGBA",image_size,(255,255,255))
  image_pixels = image.load()

  for x in range(LEFT_BORDER + 1,image_size[0]):
    image_pixels[x,0] = (255,0,0)
  
image.save("output.png", "PNG")