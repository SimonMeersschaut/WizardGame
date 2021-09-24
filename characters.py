from math import radians, sqrt, cos, sin, radians
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
      if not(GLOBAL.variables['world'].get_block((right_feed[0]+x_speed), right_feed[1]-10) in GLOBAL.variables['world'].standables):
        self.x += x_speed
      else:
        self.x_speed = 0
    if abs(self.x_speed) > 0.1:
      #self.x_speed -= GLOBAL.variables['screen'].frame_speed
      self.x_speed -= (GLOBAL.variables['screen'].frame_speed)*numpy.sign(self.x_speed)
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

class Entity:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.exists = True
    self.active = False
    self.size = 64
  def check_collision(self):
    if not(-200 < self.x-GLOBAL.variables["camera"].x < 2100) or not(-200 < self.y < 1280):
      self.exists = False
    for obj in Characters.characters + GLOBAL.variables["magic"].current_spells:
      if obj != self:
        obj_x, obj_y, obj_size = (obj.x, obj.y, obj.size)
        for punt in [(self.x, self.y), (self.x+self.size, self.y), (self.x, self.y+self.size), (self.x+self.size, self.y+self.size)]:
          px, py = punt
          if obj_x < px < obj_x+obj_size and obj_y < py < obj_y+obj_size:
            try:
              obj.hit(self)
            except AttributeError:
              pass
class DarkMinds(Entity):
  SPEED = 5
  IMGS = {}
  def __init__(self, arg):
    x, y = (arg[0], arg[1])
    try:
      color = arg[2]
    except IndexError:
      color = 'red'
    try:
      self.angle = arg[3]
    except IndexError:
      self.angle = 0
    
    super().__init__(x, y)
    self.size = 64
    self.color = color
    #self.img = f'DarkMind_{self.color}.png'
    if not(self.color in list(DarkMinds.IMGS.keys())):
      DarkMinds.IMGS.update({self.color:GLOBAL.variables['screen'].returnImage(f'DarkMind_{self.color}.png')})
  def reverse(self):
    if self.color == 'red':
      self.angle += 180
  def activate(self):
    self.active = True
    for char in Characters.characters:
      try:
        if not(char.active) and sqrt((self.x-char.x)**2 + (self.y-char.y)**2) < 200:
          char.activate()
      except AttributeError:
        pass
  def move(self):
    if self.color == 'blue':
      self.x -= cos(radians(self.angle))*DarkMinds.SPEED*GLOBAL.variables["screen"].frame_speed
      self.y += sin(radians(self.angle))*DarkMinds.SPEED*GLOBAL.variables['screen'].frame_speed
      self.angle += 1
      #self.angle = self.angle%360
    elif self.color == 'red':
      y = Characters.wizard.y
      if y > self.y:
        self.y += 1
      elif y < self.y:
        self.y -= 1
      self.x -= cos(radians(self.angle))*DarkMinds.SPEED
    elif self.color == 'gray':
      y = Characters.wizard.y
      self.check_collision()
      #if y > self.y:
      #  self.y += 1
      #elif y < self.y:
      #  self.y -= 1
      self.y += sin(radians(self.angle))*DarkMinds.SPEED
      self.x -= cos(radians(self.angle))*DarkMinds.SPEED
  def renderMe(self):
    width, height = (64,64)
    #wizard =  Characters.wizard
    if not(self.active) and self.x-GLOBAL.variables["camera"].x < GLOBAL.variables["screen"].window_width and self.x-GLOBAL.variables["camera"].x > -100:
      self.activate()
    if self.active:
      self.move()
      GLOBAL.variables["screen"].blitRotate(DarkMinds.IMGS[self.color], (self.x-GLOBAL.variables["camera"].x, self.y), (0,26), self.angle)
      #self.screen.blitRotate(self.arm, (arm[0]-GLOBAL.variables["camera"].x, arm[1]), (0,26), self.arm_angle)
      #GLOBAL.variables["screen"].renderIMG(self.img, (self.x-GLOBAL.variables["camera"].x, self.y))
      self.check_collision()
class Witch(Entity):
  def __init__(self, arg):
    x, y = arg
    super().__init__(x, y)
    self.size = 513
    self.img = f'witch.png'
    self.last_attack = time()
    self.hp = 3
    self.start_angle = 50
    self.color = 0
    self.target_y = y
    self.start_y = y
  def attack(self):
    self.last_attack = time()
    if self.hp <= 0:
      if abs(self.target_y-self.y) < 1 :
        self.target_y -= 100
        for i in range(self.start_angle,self.start_angle+360, 21):
          Characters.createNew('darkmind', self.x, self.y+100, 'gray', i)
          self.start_angle += 11
      if self.y <= -50:
        self.exists = False
    else:
      
      self.color = (self.color+1)%2
      if self.color == 0:
        self.target_y = self.start_y-150
        Characters.createNew('darkmind', self.x, self.y+130, 'gray')
      else:
        self.target_y = self.start_y
        Characters.createNew('darkmind', self.x, self.y+130, 'red')
      
  def renderMe(self):
    GLOBAL.variables["screen"].renderIMG(self.img, (self.x-GLOBAL.variables["camera"].x, self.y))
    for i in range(self.hp):
      GLOBAL.variables["screen"].renderIMG("heart.png", (self.x-GLOBAL.variables["camera"].x+(i*50), self.y-10))
    #GLOBAL.variables["screen"].renderIMG(self.img, (self.x-GLOBAL.variables["camera"].x, self.y))
    if time()-self.last_attack > 2 and 0<self.x-GLOBAL.variables["camera"].x<1920:
      self.attack()
    if self.target_y-self.y > 1:
      self.y += GLOBAL.variables["screen"].frame_speed*2
    elif self.target_y-self.y < -1:
      self.y -= GLOBAL.variables['screen'].frame_speed*2
    #self.check_collision()
  def hit(self, obj):
    if type(obj) == DarkMinds:
      if obj.angle == 180 and obj.exists:
        obj.exists = False
        self.hp -= 1
    
    if type(obj) == Characters.wizard:
      GLOBAL.variables["world"].die()

class Characters:
  NAMES = {"darkmind":DarkMinds, "witch":Witch}
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
  def createNew(*commands):
    name = commands[0]
    vars = commands[1:]
    Characters.characters.append(Characters.NAMES[name](vars))