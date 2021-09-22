from math import radians, sqrt
from global_variables import GLOBAL
from time import time
import numpy

class Wizard:
  WALK_SPEED = 7.0
  SPRINT_SPEED = 15.0
  JUMP_HEIGHT = 23
  JUMP_DELAY = .1
  FEED_Y = 62
  def __init__(self):

    #SETUP VERIABLES
    self.screen = GLOBAL.variables["screen"]
    self.world = GLOBAL.variables["world"]
    self.x = 0
    self.y = 0
    self.scale = 2
    self.jump_available = False
    self.direction = 'right'
    self.last_jump = time()
    self.imgs = {
      'left':self.screen.scale(self.screen.returnImage('wizard_left.png'), self.scale),
      'right':self.screen.scale(self.screen.returnImage('wizard_right.png'), self.scale),
      'static':self.screen.scale(self.screen.returnImage('wizard_static.png'), self.scale)
    }
    self.y_speed = 0
    self.x_speed = 0
    self.touched_ground = True
    self.speed = 0
    self.floating = False
    self.exists = True
    self.arm = self.screen.returnImage('arm.png')
    self.arm_angle = 0
    self.arm_angle_tartget = 0
    self.size = 128
  def renderMe(self):
    
    #VARIABLES
    left_feed = (self.x+23*self.scale, self.y+Wizard.FEED_Y*self.scale)
    right_feed = (self.x+42*self.scale, self.y+Wizard.FEED_Y*self.scale)
    arm = (self.x+21*self.scale, self.y+21*self.scale)
    head = (self.x+34*self.scale, self.y+7*self.scale)
    x_speed = self.x_speed*GLOBAL.variables['screen'].frame_speed
    if x_speed > 0:
      if not(GLOBAL.variables['world'].get_block((right_feed[0]+x_speed), right_feed[1]-5) in GLOBAL.variables['world'].standables):
        self.x += x_speed
      else:
        self.x_speed = 0
    if abs(self.x_speed) > 1:
      #self.x_speed -= GLOBAL.variables['screen'].frame_speed
      self.x_speed -= (GLOBAL.variables['screen'].frame_speed*2)*numpy.sign(x_speed)
      print(self.x_speed)
    else:
      self.x_speed = 0
    if GLOBAL.variables['world'].get_block(head[0], head[1]) in GLOBAL.variables['world'].standables:
      self.y -= 3
      self.y_speed = 0
    if head[1] < -10:
      self.y += -head[1]
      self.y_speed = 0
    try:
      supported = any([(self.world.get_block(position) in self.world.standables) for position in [left_feed, right_feed]])
    except IndexError:
      supported = False

    if supported and self.y > 5:
      self.touched_ground = True

    #RENDERING ALL IMGS
    self.screen.renderSurface(self.imgs[self.direction], (self.x-GLOBAL.variables["camera"].x, self.y))
    self.screen.blitRotate(self.arm, (arm[0]-GLOBAL.variables["camera"].x, arm[1]), (0,26), self.arm_angle)
    #if GLOBAL.variables['magic'].conjuring != '':
    #  self.screen.draw_circle((self.x+64*2, self.y+23*2), radius=10, color=GLOBAL.variables['magic'].COLORS[GLOBAL.variables['magic'].conjuring])
    #rect = rect.move(arm[0]-GLOBAL.variables["camera"].x, arm[1])
    for position in [(self.x, self.y), (self.x+128, self.y), left_feed, right_feed]:
      if type(self.world.get_block(position)) != str and type(self.world.get_block(position)) !=  type(None):
        x_pos, y_pos = (position[0], position[1])
        block = self.world.get_block(position)
        print(block)
        block.collide()
        
        self.world.delete_block(x_pos, y_pos)
        
   #for block, disapear, position2 in [(self.world.get_block(position), disapear, position) for position, disapear in [(self.x, self.y), (self.x+128, self.y), left_feed, right_feed] if self.world.get_block(position) in blocks]:
   #  if disapear:
   #    x, y = (int(position2[0]/self.world.block_size), int(position2[1]/self.world.block_size))
   #    self.world.map[x][y] = None
   #  collide(block)


    #MOVEMENT
    self.direction = 'static'
    if GLOBAL.variables["settings"].k_left in self.screen.keys:
      pos = (left_feed[0]-15, left_feed[1]-10)
      if not(self.world.get_block(pos) in self.world.standables):
        self.x -= Wizard.WALK_SPEED*self.screen.frame_speed
        self.direction = 'left'
    elif GLOBAL.variables["settings"].k_right in self.screen.keys:
      pos = (right_feed[0]+15, right_feed[1]-10)
      if not(self.world.get_block(pos) in self.world.standables):
        if GLOBAL.variables['settings'].k_sprint in self.screen.keys:
          self.speed = min(Wizard.SPRINT_SPEED, self.speed+GLOBAL.variables['screen'].frame_speed)
        else:
          self.speed = Wizard.WALK_SPEED
        self. x += self.speed*self.screen.frame_speed
      self.direction = 'right'
    if GLOBAL.variables["settings"].k_jump in self.screen.keys and supported and self.jump_available:
      if time()-self.last_jump > Wizard.JUMP_DELAY:
        self.jump_available = False
        self.last_jump = time()
        self.y_speed -= self.JUMP_HEIGHT
    a = self.arm_angle_tartget - self.arm_angle
    a = (a + 180) % 360 - 180
    self.arm_angle_tartget = 87
    increment = ((abs(a)/10)+0.25)*self.screen.frame_speed
    if a > increment:
      self.arm_angle += increment
    elif a < -increment:
      self.arm_angle -= increment
    if supported:
      positions = [(position[0], position[1]-2) for position in [left_feed, right_feed, head]]
      if any([GLOBAL.variables['world'].get_block(position) in GLOBAL.variables['world'].deadly for position in positions]):
        GLOBAL.variables['world'].die()
      if not GLOBAL.variables["settings"].k_jump in self.screen.keys:
        self.jump_available = True
      if self.y_speed > 0:
        self.y_speed = 0
        self.y = int((self.y)/self.world.square_size)*self.world.square_size+(69-Wizard.FEED_Y)
        
    if not supported:
      self.y_speed += 1*self.screen.frame_speed
    if self.floating and GLOBAL.variables['magic'].points > 0:
      self.arm_angle_tartget = -90
      GLOBAL.variables['magic'].points -= 0.2*self.screen.frame_speed
      self.y_speed = min(max(0, self.y_speed-(1.2*self.screen.frame_speed)),self.y_speed)    

    if left_feed[1] > self.screen.window_height: #when touch the bottom
      self.world.die() #die

    self.y += self.y_speed*self.screen.frame_speed
    if right_feed[0] >= GLOBAL.variables['world'].finish_x:
      GLOBAL.variables['world'].next_level()
  def hit(self, obj):
    if type(obj) == DarkMinds:
      GLOBAL.variables["world"].die()

class DarkMinds:
  SPEED = 5
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.size = 64
    self.exists = True
    self.active = False
  def activate(self):
    self.active = True
    for char in Characters.characters:
      try:
        if not(char.active) and sqrt((self.x-char.x)**2 + (self.y-char.y)**2) < 200:
          char.activate()
      except AttributeError:
        pass
  def renderMe(self):
    width, height = (64,64)
    #wizard =  Characters.wizard
    if not(self.active) and self.x-GLOBAL.variables["camera"].x < GLOBAL.variables["screen"].window_width and self.x-GLOBAL.variables["camera"].x > -100:
      self.activate()
    if self.active:
      self.x -= DarkMinds.SPEED*GLOBAL.variables["screen"].frame_speed
      GLOBAL.variables["screen"].renderIMG('DarkMind.png', (self.x-GLOBAL.variables["camera"].x, self.y))
      for obj in Characters.characters + GLOBAL.variables["magic"].current_spells:
        if obj != self:
          obj_x, obj_y, obj_size = (obj.x, obj.y, obj.size)
          for punt in [(self.x, self.y), (self.x+width, self.y), (self.x, self.y+height), (self.x+width, self.y+width)]:
            px, py = punt
            if obj_x < px < obj_x+obj_size and obj_y < py < obj_y+obj_size:
              obj.hit(self)

class Characters:
  NAMES = {"darkmind":DarkMinds}
  characters = []
  def init():
    Characters.characters = []
    Characters.characters = [Wizard()]
    Characters.wizard = Characters.characters[0]
  def render():
    for char in Characters.characters:
      if char.exists:
        char.renderMe()
      else:
        Characters.characters.remove(char)
  def createNew(command):
    name, x, y = command
    
    Characters.characters.append(Characters.NAMES[name](x, y))
  
