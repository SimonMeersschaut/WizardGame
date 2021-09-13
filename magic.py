from time import time
#from characters import Characters
from characters import DarkMinds
from global_variables import GLOBAL
from screen import Screen
from math import sqrt
class Shield:
  def __init__(self, x, y):
    self.image = 'Shield.png'
    self.x = x
    self.y = y
    self.exists = True
    self.size = 64
  def render(self):
    Screen.renderIMG(self.image, (self.x-GLOBAL.variables["camera"].x, self.y))
  def hit(self, obj):
    if type(obj) == DarkMinds:
      obj.exists = False
      self.exists = False
class Shoot:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.exists = True
    self.size = 64
    self.image = 'Shield.png'
  def render(self):
    Screen.renderIMG(self.image, (self.x-GLOBAL.variables["camera"].x, self.y))
    self.x += 1
  def hit(self, obj):
    if type(obj) == DarkMinds:
      obj.exists = False
      self.exists = False

class Dash:
  def __init__(self, x, y):
    GLOBAL.variables['characters'].wizard.x += 200
    self.exists = False
  def render(self):
    pass
class Magic:
  #SPELLS
  #CODE:(OBJECT, MP)
  SPELLS = {
    'none':{},
    'movement':{
      '45':(Dash, 1),
      "14":(None, 0)
    },
    'combat':{
      "046":(Shield, 10),
      '45':(Shoot, 1)
    }
  }
  points = 0
  refreshed = 0
  spawned = False
  used_balls = False
  last_spell = 0
  CIRCLE_DIST = 50
  CIRCLE_RADIUS = 20
  COLORS = {
    'movement':(0,0,255)
  }
  #VARIABLES
  def init():
    Magic.points = 100
    Magic.injuring = True
    Magic.current_spells = []
    Magic.mode = 'none'
    #Magic.conjuring = "efsdf"

    Magic.CIRCLE_OFFSET = (Magic.CIRCLE_DIST*1.5, Magic.CIRCLE_DIST*2.5) #Screen.window_height-Magic.CIRCLE_DIST/2
    Magic.combination = None

    #Generate ball positions
    Magic.activated_balls = []
    Magic.ball_positions = []
    for y in range(-2*Magic.CIRCLE_DIST, 1*Magic.CIRCLE_DIST, Magic.CIRCLE_DIST):
      for x in range(-1*Magic.CIRCLE_DIST, 2*Magic.CIRCLE_DIST, Magic.CIRCLE_DIST):
        Magic.ball_positions.append((x+Magic.CIRCLE_OFFSET[0],y+Magic.CIRCLE_OFFSET[1]))
    Magic.current_spells = []

  @Screen.onRender('game')
  def render():
    colors = {
      None:[(0,0,0), (120,120,120)],
      'right':[(20,20,20), (180,180,180)],
      'no points':[(80,80,80), (255,100,100)]
    }
    autocomplete = Magic.autocomplete()
    if Magic.injuring:
      for index, position in enumerate(Magic.ball_positions):
        
        if index in Magic.activated_balls:
          ball_color = colors[Magic.combination][1]
        else:
          ball_color = colors[Magic.combination][0]
        if index in autocomplete:
          ball_color = (255,255,255)
        Screen.draw_circle(position, radius=Magic.CIRCLE_RADIUS, border_width=Magic.CIRCLE_RADIUS, color=ball_color)
      Magic.check_balls()
    for spell in Magic.current_spells:
      if spell.render and spell.exists:
        spell.render()
      else:
        Magic.current_spells.remove(spell)
    #RENDER LOADING BAR
    x, y = (GLOBAL.variables['screen'].window_width-210,10)
    GLOBAL.variables['screen'].draw_rect(x, y, Magic.points*2, 40)

  def get_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    b = x2-x1
    c = y2-y1
    a = sqrt(b**2 + c**2)
    return a
  def autocomplete():
    autocomplete = []
    activated = ''.join([str(number) for number in Magic.activated_balls])
    for spell in Magic.SPELLS[Magic.mode]:
      if activated in spell:
        #print('magic autocomplete')
        broke = False
        for index, (letterSPELL, letterBALL) in enumerate(zip(spell, activated)):
          if not broke:
            #print(type(letterSPELL), type(letterBALL))
            if letterSPELL != letterBALL:
              
              if index != 0:
                #print('append',letterSPELL)
                autocomplete.append(letterSPELL)
              broke = True
    return autocomplete
  def check_balls():
    tijd = time()
    if tijd-Magic.last_spell > .5:
      keys  = [setting_key[0] for setting_key in GLOBAL.variables["settings"].keys if 'ball_' in setting_key[0]]
      balls = [index for index, key in enumerate(keys) if key in GLOBAL.variables["screen"].keys]
      
      for ball in balls:
        if ball not in Magic.activated_balls:
          Magic.activated_balls.append(ball)
          Magic.refreshed = tijd
          Magic.used = False
      Magic.activated_balls = sorted(Magic.activated_balls)
      if (tijd-Magic.refreshed > 0.2 and balls == []) or (Magic.used and balls == []):
        Magic.activated_balls = []
        Magic.used = False
        Magic.spawned = False
    #if Screen.mouseDown:
    #  for index, position in enumerate(Magic.ball_positions):
    #    dist = Magic.get_dist(position, Screen.mousePos)
    #    if dist <= Magic.CIRCLE_RADIUS:
    #      if len(Magic.activated_balls) == 0 or index not in Magic.activated_balls:
    #        Magic.activated_balls.append(int(index))
    #        
    #else:
    Magic.check_spell()
    #  Magic.activated_balls = []
    Magic.ball_color()
    GLOBAL.variables['characters'].wizard.floating = bool(''.join([str(number) for number in Magic.activated_balls]) == '14' and (GLOBAL.variables['characters'].wizard.y_speed > 3 or GLOBAL.variables['characters'].wizard.floating) and Magic.mode == 'movement')
  def ball_color():
    combination = None
    spell_combination = ''.join([str(number) for number in Magic.activated_balls])
    for spell_name in Magic.SPELLS[Magic.mode]:
      obj, spell_points = Magic.SPELLS[Magic.mode][spell_name]
      if spell_combination == spell_name:
        if Magic.points > spell_points:
          combination = 'right'
        else:
          if not combination:
            combination = 'no points'
    Magic.combination = combination
  def check_spell():
    spell_combination = ''.join([str(number) for number in Magic.activated_balls])
    for spell_name in Magic.SPELLS[Magic.mode]:
      obj, spell_points = Magic.SPELLS[Magic.mode][spell_name]
      if spell_combination == spell_name:
        Magic.used = True
        if Magic.points > spell_points:
          Magic.points -= spell_points
          if obj != None:
            Magic.activated_balls = []
            Magic.current_spells.append(obj(GLOBAL.variables['characters'].wizard.x+63, GLOBAL.variables['characters'].wizard.y+24))
            Magic.spawned = True
            Magic.last_spell = time()