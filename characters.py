from math import radians
from global_variables import GLOBAL


#from tool import World, Screen, Camera
#from main import returnToMainMenu
class Wizard:
  WALK_SPEED = 5
  JUMP_HEIGHT = 20
  def __init__(self):
    #SETUP VERIABLES
    self.screen = GLOBAL.variables["screen"]
    self.world = GLOBAL.variables["world"]
    self.x = 0
    self.y = 0
    self.scale = 2
    self.direction = 'right'
    self.imgs = {
      'left':self.screen.scale(self.screen.returnImage('wizard_left.png'), self.scale),
      'right':self.screen.scale(self.screen.returnImage('wizard_right.png'), self.scale),
      'static':self.screen.scale(self.screen.returnImage('wizard_static.png'), self.scale)
    }
    self.y_speed = 0
    self.floating = False
    self.arm = self.screen.returnImage('arm.png')
    self.arm_angle = 0
    self.arm_angle_tartget = 0
  def renderMe(self):
    #VARIABLES
    
    left_feed = (self.x+23*self.scale, self.y+64*self.scale)
    right_feed = (self.x+42*self.scale, self.y+64*self.scale)
    arm = (self.x+21*self.scale, self.y+21*self.scale)

    try:
      supported = any([(self.world.get_block(position) in self.world.standables) for position in [left_feed, right_feed]])
    except IndexError:
      supported = False
    
    #RENDERING ALL IMGS
    self.screen.renderSurface(self.imgs[self.direction], (self.x-GLOBAL.variables["camera"].x, self.y))
    self.screen.blitRotate(self.arm, (arm[0]-GLOBAL.variables["camera"].x, arm[1]), (0,26), self.arm_angle)
    #if GLOBAL.variables['magic'].conjuring != '':
    #  self.screen.draw_circle((self.x+64*2, self.y+23*2), radius=10, color=GLOBAL.variables['magic'].COLORS[GLOBAL.variables['magic'].conjuring])
    #rect = rect.move(arm[0]-GLOBAL.variables["camera"].x, arm[1])
    
    #MOVEMENT
    self.direction = 'static'
    if GLOBAL.variables["settings"].k_left in self.screen.keys:
      self.x -= self.WALK_SPEED*self.screen.frame_speed
      self.direction = 'left'
    elif GLOBAL.variables["settings"].k_right in self.screen.keys:
      self. x += self.WALK_SPEED*self.screen.frame_speed
      self.direction = 'right'
    if GLOBAL.variables["settings"].k_jump in self.screen.keys and supported:
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
      if self.y_speed > 0:
        self.y_speed = 0
        print('positie'+str(self.y))
        self.y = int((self.y)/self.world.square_size)*self.world.square_size#-50
    if not supported:
      self.y_speed += 1*self.screen.frame_speed
    if self.floating and GLOBAL.variables['magic'].points > 0:
      self.arm_angle_tartget = -90
      GLOBAL.variables['magic'].points -= 0.1*self.screen.frame_speed
      self.y_speed = min(max(0, self.y_speed-(1.2*self.screen.frame_speed)),self.y_speed)
      GLOBAL.variables['magic'].conjuring = 'movement'
    

    if left_feed[1] > self.screen.window_height: #when touch the bottom
      self.world.returnToMainMenu() #die

    self.y += self.y_speed*self.screen.frame_speed
    if right_feed[0] >= GLOBAL.variables['world'].finish_x:
      GLOBAL.variables['world'].next_level()
class DarkMinds:
  SPEED = 1
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def renderMe(self):
    #if self.x-GLOBAL.variables["camera"].x < GLOBAL.variables["screen"].window_width and self.x-GLOBAL.variables["camera"].x > -100:
      
    self.x -= DarkMinds.SPEED*GLOBAL.variables["screen"].frame_speed
    GLOBAL.variables["screen"].renderIMG('DarkMind.png', (self.x-GLOBAL.variables["camera"].x, self.y))
class Characters:
  NAMES = {"DarkMinds":DarkMinds}
  characters = []
  def init():
    print('nieuwe wizard')
    Characters.characters = []
    Characters.characters = [Wizard()]
    Characters.wizard = Characters.characters[0]
  def render():
    for char in Characters.characters:
      char.renderMe()
  def createNew(command):
    name, x, y = command
    print('created', name)
    Characters.characters.append(Characters.NAMES[name](x, y))