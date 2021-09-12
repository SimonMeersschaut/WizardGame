from math import radians
from global_variables import GLOBAL


#from tool import World, Screen, Camera
#from main import returnToMainMenu
class Wizard:
  WALK_SPEED = 7.2
  JUMP_HEIGHT = 25
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
    self.exists = True
    self.arm = self.screen.returnImage('arm.png')
    self.arm_angle = 0
    self.arm_angle_tartget = 0
    self.size = 128
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
    blocks = [('book_purple', True)]
    for position in [(self.x, self.y), (self.x+128, self.y), left_feed, right_feed]:
      if self.world.get_block(position) in [block[0] for block in blocks]:
        x_pos, y_pos = (position[0], position[1])
        print(self.world.get_block(position))
        collide(self.world.get_block(position))
        
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
        self.x -= self.WALK_SPEED*self.screen.frame_speed
        self.direction = 'left'
    elif GLOBAL.variables["settings"].k_right in self.screen.keys:
      pos = (right_feed[0]+10, right_feed[1]-10)
      if not(self.world.get_block(pos) in self.world.standables):
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
        self.y = int((self.y)/self.world.square_size)*self.world.square_size#-50
    if not supported:
      self.y_speed += 1*self.screen.frame_speed
    if self.floating and GLOBAL.variables['magic'].points > 0:
      self.arm_angle_tartget = -90
      GLOBAL.variables['magic'].points -= 0.2*self.screen.frame_speed
      self.y_speed = min(max(0, self.y_speed-(1.2*self.screen.frame_speed)),self.y_speed)    

    if left_feed[1] > self.screen.window_height: #when touch the bottom
      self.world.returnToMainMenu() #die

    self.y += self.y_speed*self.screen.frame_speed
    if right_feed[0] >= GLOBAL.variables['world'].finish_x:
      GLOBAL.variables['world'].next_level()
  def hit(self, obj):
    if type(obj) == DarkMinds:
      GLOBAL.variables["world"].returnToMainMenu()

class DarkMinds:
  SPEED = 3
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.size = 64
    self.exists = True
  def renderMe(self):
    width, height = (64,64)
    #wizard =  Characters.wizard
    if self.x-GLOBAL.variables["camera"].x < GLOBAL.variables["screen"].window_width and self.x-GLOBAL.variables["camera"].x > -100:
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
  NAMES = {"DarkMinds":DarkMinds}
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
  
def collide(block):
  color = block.split('book_')[1]
  if color == 'purple':
    GLOBAL.variables['magic'].mode = 'movement'