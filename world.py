from random import randint
from global_variables import GLOBAL
from screen import Screen
from json import load
from characters import Characters
class World:

  current_level = []
  map = []
  height = 20
  width = 64
  square_size = 128
  standables = ['ground']
  grounds = ['ground.png', 'ground_bottom.png']
  world = 0
  level = -1
  finish_x = 0
  def init():
    World.next_level()
  def get_level(world, level):

    World.map = [[None for y in range(World.height)] for x in range(World.width)]
    World.current_level = []
    with open('levels.json', 'r') as f:
      file_content = load(f)[world][level]
      for commando in file_content:
        if commando[0] in Characters.NAMES:
          Characters.createNew(commando)
        else:
            img, startx, starty, eindx, eindy = commando
            if startx == eindx:
              eindx += 1
            if starty == eindy:
              eindy += 1
            for x in range(startx, eindx):
              for y in range(starty, eindy):
                World.map[x][y] = img
                World.current_level.append([img, x*World.square_size, y*World.square_size])
      World.spawn_grass()
      print(file_content)
      x, y = (file_content[0][3], file_content[0][2]-1)
      World.map[x][y] = 'finish.png'
      World.current_level.append(['finish.png', x*World.square_size, y*World.square_size])
      World.finish_x = x*World.square_size
    return World.current_level
  def spawn_grass():
    for x, stroke in enumerate(World.map):
      for y, block in enumerate(stroke):
        if block == 'ground.png' and World.map[x][y-1] == None:
          print('grass', x, y)
          World.current_level.append(['grass.png', x*World.square_size, (y-1)*World.square_size])
          
  def next_level():
    World.level += 1
    #with open('levels.json', 'r') as f:
    #  if len(load(f)[World.world]) <= World.level:
    #    World.level = 0
    #    World.world += 1 
    try:
      GLOBAL.variables['characters'].init()
      GLOBAL.variables['magic'].init()
      GLOBAL.variables['camera'].init()
    except KeyError:
      pass
    World.get_level(World.world, World.level)
  #def gen_map():
  #    #input(World.current_level)
  #    for (obj, x, y) in World.current_level:
  #      xv, yv = World.get_square(x, y)
  #      World.map[xv][yv] = obj
  def render():
    for index, (obj, xpos, ypos) in enumerate(World.current_level):

      if obj == 'ground.png' and World.map[round(xpos/World.square_size)][round(ypos/World.square_size)-1] in World.grounds:
        print('changed')
        World.map[round(xpos/World.square_size)][round(ypos/World.square_size)] = 'ground_bottom.png'
        World.current_level[index][0] = 'ground_bottom.png'
      
      Screen.renderIMG(obj, (xpos-GLOBAL.variables["camera"].x, ypos), resize = 2)
   
  def get_square(xpos, ypos):
    xv, yv = (int(xpos/World.square_size), int(ypos/World.square_size))
    return (xv, yv)
  def get_block(xposition, yposition=None):
    if yposition == None:
      xposition, yposition = xposition
    (xvak, yvak) = World.get_square(xposition, yposition)
    vak = World.map[xvak][yvak]
    if '.' in str(vak):
      return vak.split('.')[0]
    return vak
  def returnToMainMenu():
    Screen.state = 'main_menu'
    World.init()
    Characters.init()
    


#  @classmethod
#  def onUpdate(cls, state, **options):
#    def decorator(f):
#        cls.update_functions.append([state, f])
#        print('gezet')
#        return f
#
#    return decorator