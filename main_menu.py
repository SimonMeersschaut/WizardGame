from screen import Screen
from global_variables import GLOBAL
class Menu:
  
  class Level:
    WIDTH = 200
    offset_x = 20
    def __init__(self, index):
      self.index = index
      x, y = (0,100)
      for i in range(GLOBAL.variables['world'].levels):
        
        if i == self.index:
          self.x, self.y = (x, y)
        x += Menu.Level.WIDTH+10
        if x+Menu.Level.WIDTH > Screen.window_width:
          #Menu.Level.offset_x = abs((Screen.window_width-(x+Menu.Level.WIDTH))/2)
          print(Menu.Level.offset_x)
          y += Menu.Level.WIDTH+10
          x = 0
    def render(self):
      Screen.draw_rect(self.x+Menu.Level.offset_x, self.y, Menu.Level.WIDTH, Menu.Level.WIDTH, color=(0,0,0))
      Screen.render_text(str(self.index+1), self.x+Menu.Level.offset_x+10, self.y, color=(255,255,255))
    def clicked(self, x, y):
      if self.x < x < self.x+Menu.Level.WIDTH and self.y < y < self.y+Menu.Level.WIDTH:

        GLOBAL.variables['world'].level += self.index
        GLOBAL.variables['world'].get_level(self.index+1)
        Screen.state = 'game'

  OPTIONS = 3
  X_VALUES = [960-897, 960-827, 960-902]
  state = 'main_menu'
  levels = []
  def init():
    Screen.loadIMG('main_menu.png')
    Screen.mousePos = (-1, -1)
    
  def render():
    index = round((Screen.mousePos[1]-534)/(628-534))
    index = min(max(0, index), Menu.OPTIONS-1)
    if Menu.state == 'main_menu':
      Screen.renderIMG('main_menu.png', (0,0))
      Screen.renderIMG('arrow_right.png', (960-Menu.X_VALUES[index]-75, index*(628-534)+509))
      Screen.renderIMG('arrow_left.png', (960+Menu.X_VALUES[index]+75-50, index*(628-534)+509))
      if Screen.mouseDown:
        if index == 0:
          Menu.state = 'levels_wachten'
          Menu.create_levels()
        elif index == 1:
          Screen.state = 'options'
        elif index == 2:
          Screen.running = False
    elif Menu.state == 'levels_wachten':
      if not(Screen.mouseDown):
        Menu.state = 'levels'
    elif Menu.state == 'levels':
      for level in Menu.levels:
        level.render()
      if Screen.mouseDown:
        x, y = Screen.mousePos
        for level in Menu.levels:
          level.clicked(x, y)
    #if 1920 > Screen.mousePos[0] > 0:
    #  Screen.state = 'game'
  def create_levels():
    Menu.levels = [Menu.Level(i) for i in range(GLOBAL.variables['world'].levels)]
    print(f'LEVELS:' + str(GLOBAL.variables['world'].levels))
  def stop():
    Screen.state = 'game'
