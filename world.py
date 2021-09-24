from math import e
from random import randint
from global_variables import GLOBAL
from screen import Screen
from json import load
from characters import Characters
from time import time

COLORS = {
  'red':(200,0,0),
  'green':(0,200,0)
}

class Book:
  def __init__(self, name):
    self.name = name
    self.color = name.split('book_')[1].split('.')[0]
    self.rgb = COLORS[self.color]
  def render(self, xpos, ypos):
    GLOBAL.variables['screen'].draw_rect(xpos-GLOBAL.variables["camera"].x, ypos, World.square_size, World.square_size, color=self.rgb)
    Screen.renderIMG('book_blueprint.png', (xpos-GLOBAL.variables["camera"].x, ypos), resize = 2)
  
  def collide(self):
    GLOBAL.variables['magic'].mode = self.color

class World:

  current_level = []
  map = []
  height = 20
  width = 90
  square_size = 128
  standables = ['ground', 'ground_bottom', 'spikes_bottom']
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
    World.state = ''
    World.time_completed = time()-2
    #World.get_level(Wo)
    with open('world.json', 'r') as f:
      file_content = load(f)['levels']
      World.levels = len(file_content)

  def get_level(level):

    World.map = [[None for y in range(World.height)] for x in range(World.width)]
    World.current_level = []
    finish_x = 0
    finish_y = 1920
    GLOBAL.variables['screen'].time_speed = 1
    with open('world.json', 'r') as f:
      print('start')
      file_content = load(f)['levels']
      World.levels = len(file_content)
      file_content = file_content[level-1]
      print(file_content)
      World.time_limit = time()+100#time()+file_content[-1]
      World.level_time_limit = time()+100# file_content[-1]
      finish_x = 0
      for name, x, y in file_content:
        if not('book' in name):
          if name in GLOBAL.variables['characters'].NAMES:
            GLOBAL.variables['characters'].createNew(name, x*World.square_size, y*World.square_size)
            continue
          try:
            World.map[x][y] = name
          except IndexError:
            continue
        else:
          book = Book(name)
          World.map[x][y] = book
        xpos, ypos = ((x)*World.square_size, (y)*World.square_size)
        if xpos >= finish_x:
          finish_x = xpos
          finish_y = min(finish_y, ypos)
        if type(name) != str or not('book' in name):
          World.current_level.append([name, xpos, ypos])
        else:
          World.current_level.append([book, xpos, ypos])

    x, y = (int(finish_x/World.square_size), int(finish_y/World.square_size))
    World.map[x][y-2] = 'finish.png'
    World.current_level.append(['finish.png', finish_x, finish_y-World.square_size])
    World.spawn_grass()
    World.set_bottoms()
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
      if type(obj) == str:
        if any([obj.split('.')[0] in BOTTOM or BOTTOM in obj.split('.')[0] for BOTTOM in BOTTOMS]) and (World.map[round(xpos/World.square_size)][round(ypos/World.square_size)-1] in World.grounds or World.map[round(xpos/World.square_size)][round(ypos/World.square_size)-1] in BOTTOMS):
          new_name = obj.split('.')[0]+'_bottom.'+obj.split('.')[1]
          World.map[round(xpos/World.square_size)][round(ypos/World.square_size)] = new_name
          World.current_level[index][0] = new_name
        else:
          print(obj)
  def next_level():
    if World.state != 'completed':
      World.state = 'completed'
      GLOBAL.variables['screen'].time_speed = 0.1
      World.time_completed = time()
  def load_next_level():
    World.level += 1
    GLOBAL.variables['screen'].time_speed = 1
    GLOBAL.variables['settings'].unlocked_levels = max(World.level, GLOBAL.variables['settings'].unlocked_levels)
    GLOBAL.variables['settings'].save()
    World.load_level()
  def load_level():
    World.time_started = time() 
    Characters.init()
    GLOBAL.variables['magic'].init()
    GLOBAL.variables['camera'].init()
    #try:
    World.get_level(World.level)
  
  def render():
    for index, (obj, xpos, ypos) in enumerate(World.current_level):
      if type(obj) == str:
        Screen.renderIMG(obj, (xpos-GLOBAL.variables["camera"].x, ypos), resize = 2)
      else:
        obj.render(xpos, ypos)
    width, height = ((World.time_limit-time())/World.level_time_limit*1500,50)
    x1 = 200
    y1 = 10
    Screen.draw_rect(x1, y1, width, height, color=(255,0,0))
    if World.state == 'completed':
      #if round((time()-World.time_completed)*2.5) % 2 == 0:
      chars = round((time()-World.time_completed)*20)
      Screen.render_text('mission accomplished!'[0:chars], 500, 300, color=(20,20,20))
      if time()-World.time_completed > 2:
        World.state = ''
        World.load_next_level()
    try:
      list = Tutorial.TEXT[World.level-1]
      camera_x = GLOBAL.variables['camera'].x
      for text, posx, posy in list:

        Screen.render_text(text, posx-camera_x, posy, color=(255,255,255), fontsize=40)
    except:
      pass
  def get_square(xpos, ypos):
    xv, yv = (int(xpos/World.square_size), int(ypos/World.square_size))
    return (xv, yv)
  def get_block(xposition, yposition=None):
    try:
      if yposition == None:
        xposition, yposition = xposition
      (xvak, yvak) = World.get_square(xposition, yposition)
      vak = World.map[xvak][yvak]
      if type(vak) == str:
        if '.' in str(vak):
          return vak.split('.')[0]
        return vak
      else:
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

class Tutorial:
  TEXT = [
    [('use <WASD> to walk and jump with <SPACE>', 50, 200), ('Collect books for new enchantmens', 5994, 297)]
  ]
#  @classmethod
#  def onUpdate(cls, state, **options):
#    def decorator(f):
#        cls.update_functions.append([state, f])
#        print('gezet')
#        return f
#
#    return decorator