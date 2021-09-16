from math import e
from random import randint
from global_variables import GLOBAL
from screen import Screen
from json import load
from characters import Characters
from time import time
class World:

  current_level = []
  map = []
  height = 20
  width = 90
  square_size = 128
  standables = ['ground', 'ground_bottom', 'spikes', 'spikes_bottom']
  grounds = ['ground.png', 'ground_bottom.png', 'spikes.png', 'spikes_bottom.png']
  deadly = ['spikes']
  world = 0
  level = -2
  finish_x = 0
  def init():
    World.level = 0
    World.world = 0
    World.time_limit = 0
    World.level_time_limit = 1
    World.time_started = 0
    World.next_level()

  def get_level(world, level):

    World.map = [[None for y in range(World.height)] for x in range(World.width)]
    World.current_level = []
    finish_x = 0
    finish_y = 100
    print('get level')
    with open('world.json', 'r') as f:
      print('start')
      file_content = load(f)['levels'][level-1]
      print(file_content)
      World.time_limit = time()+100#time()+file_content[-1]
      World.level_time_limit = time()+100# file_content[-1]
      finish_x = 0
      for name, x, y in file_content:
        World.map[x][y] = name
        xpos, ypos = ((x)*World.square_size, (y)*World.square_size)
        if xpos >= finish_x:
          finish_x = xpos
          finish_y = min(finish_y, ypos)
        
        World.current_level.append([name, xpos, ypos])
        #if commando[0] in Characters.NAMES:
        #  Characters.createNew(commando)
        #else:
        #  if len(commando) == 5:
        #    img, startx, starty, eindx, eindy = commando
        #  else:
        #    img, startx, starty = commando
        #    eindx = startx
        #    eindy = starty
        #  finish_x = max(finish_x, eindx)
        #  #if startx == eindx:
        #  #  eindx += 1
        #  #if starty == eindy:
        #  #  eindy += 1
        #  if abs(startx-eindx) > 0 and abs(starty-eindy) > 0:
        #    for x in range(startx, eindx):
        #      for y in range(starty, eindy):
        #        World.map[x][y] = img
        #        World.current_level.append([img, (x)*World.square_size, y*World.square_size])
        #  else:
        #    
        #    World.map[startx][starty] = img
        #    World.current_level.append([img, (startx)*World.square_size, starty*World.square_size])
    x, y = (int(finish_x/World.square_size), int(finish_y/World.square_size))
    World.map[x-1][y] = 'finish.png'
    World.spawn_grass()
    World.set_bottoms()
    World.current_level.append(['finish.png', finish_x, finish_y])
    World.finish_x = finish_x

    return World.current_level
  def spawn_grass():
    print(World.current_level)
    for block, x, y in World.current_level:
      if block == 'ground.png' and World.get_block(x, y-World.square_size) == None:
        World.current_level.append(['grass.png', x, y-World.square_size])
        print('grass')
  def set_bottoms():
    BOTTOMS = ['ground', 'spike']
    for index, (obj, xpos, ypos) in enumerate(World.current_level):
      if any([obj.split('.')[0] in BOTTOM or BOTTOM in obj.split('.')[0] for BOTTOM in BOTTOMS]) and (World.map[round(xpos/World.square_size)][round(ypos/World.square_size)-1] in World.grounds or World.map[round(xpos/World.square_size)][round(ypos/World.square_size)-1] in BOTTOMS):
        new_name = obj.split('.')[0]+'_bottom.'+obj.split('.')[1]
        World.map[round(xpos/World.square_size)][round(ypos/World.square_size)] = new_name
        World.current_level[index][0] = new_name
      else:
        print(obj)
  def next_level():
    World.level += 1
    World.load_level()

  def load_level():
    World.time_started = time() 
    Characters.init()
    GLOBAL.variables['magic'].init()
    GLOBAL.variables['camera'].init()
    #try:
    World.get_level(World.world, World.level)
  
  def render():
    for index, (obj, xpos, ypos) in enumerate(World.current_level):

      Screen.renderIMG(obj, (xpos-GLOBAL.variables["camera"].x, ypos), resize = 2)
    width, height = ((World.time_limit-time())/World.level_time_limit*1500,50)
    x1 = 200
    y1 = 10
    Screen.draw_rect(x1, y1, width, height, color=(255,0,0))
  def get_square(xpos, ypos):
    xv, yv = (int(xpos/World.square_size), int(ypos/World.square_size))
    return (xv, yv)
  def get_block(xposition, yposition=None):
    try:
      if yposition == None:
        xposition, yposition = xposition
      (xvak, yvak) = World.get_square(xposition, yposition)
      vak = World.map[xvak][yvak]
      if '.' in str(vak):
        return vak.split('.')[0]
      return vak
    except IndexError:
      return None
  def returnToMainMenu():
    Screen.state = 'main_menu'
    GLOBAL.variables['main_menu'].init()
    World.init()
    Characters.init()
  
  def delete_block(xpos, ypos):
    x_block, y_block = (int(xpos/World.square_size), int(ypos/World.square_size))
    block_name = World.map[x_block][y_block]
    World.map[x_block][y_block] = None
    delete_index = False
    for index, (obj, xpos1, ypos1) in enumerate(World.current_level):
      x_block1, y_block1 = (int(xpos1/World.square_size), int(ypos1/World.square_size))
      if obj == block_name:
        if x_block == x_block1 and y_block == y_block1:
          delete_index = index
    if delete_index:
      World.current_level.pop(delete_index)
    
  def die():
    World.load_level()
    #World.returnToMainMenu()


#  @classmethod
#  def onUpdate(cls, state, **options):
#    def decorator(f):
#        cls.update_functions.append([state, f])
#        print('gezet')
#        return f
#
#    return decorator