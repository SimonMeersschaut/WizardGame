from screen import Screen
from global_variables import GLOBAL
class Menu:
  BOSS_FIGHTS = [5]
  class Level:
    WIDTH = 200
    offset_x = 20
    def __init__(self, index, last):
      
      self.index = index
      self.last = bool(last)
      self.text_color = (255,255,255)
      if index in Menu.BOSS_FIGHTS:
          self.text_color = (212, 129, 130)
      if self.last:
        self.color = (20,20,20)
      else:
        self.color = (0,0,0)
      x, y = (0,100)
      for i in range(GLOBAL.variables['world'].levels):
        
        if i == self.index:
          self.x, self.y = (x, y)
        x += Menu.Level.WIDTH+10
        if x+Menu.Level.WIDTH > Screen.window_width:
          #Menu.Level.offset_x = abs((Screen.window_width-(x+Menu.Level.WIDTH))/2)
          y += Menu.Level.WIDTH+10
          x = 0
    def render(self):
      x, y = Screen.mousePos
      if self.x < x < self.x+Menu.Level.WIDTH and self.y < y < self.y+Menu.Level.WIDTH:
        Screen.draw_rect(self.x+Menu.Level.offset_x-2, self.y-2, Menu.Level.WIDTH+4, Menu.Level.WIDTH+4, color=(255,255,255))
      else:
        Screen.draw_rect(self.x+Menu.Level.offset_x-2, self.y-2, Menu.Level.WIDTH+4, Menu.Level.WIDTH+4, color=(40,40,40))
      Screen.draw_rect(self.x+Menu.Level.offset_x, self.y, Menu.Level.WIDTH, Menu.Level.WIDTH, color=self.color)
      Screen.render_text(str(self.index+1), self.x+Menu.Level.offset_x+10, self.y, color=self.text_color)
      
    def clicked(self, x, y):
      if self.x < x < self.x+Menu.Level.WIDTH and self.y < y < self.y+Menu.Level.WIDTH:

        GLOBAL.variables['world'].level = self.index+1
        GLOBAL.variables['world'].load_level()
        Screen.state = 'game'

  OPTIONS = 3
  X_VALUES = [960-897, 960-827, 960-902]
  levels = []
  def init():
    Screen.loadIMG('main_menu.png')
    Screen.mousePos = (-1, -1)
    
  def render():
    index = round((Screen.mousePos[1]-534)/(628-534))
    index = min(max(0, index), Menu.OPTIONS-1)
    if Screen.state == 'main_menu':
      Screen.renderIMG('main_menu.png', (0,0))
      Screen.renderIMG('arrow_right.png', (960-Menu.X_VALUES[index]-75, index*(628-534)+509))
      Screen.renderIMG('arrow_left.png', (960+Menu.X_VALUES[index]+75-50, index*(628-534)+509))
      if Screen.mouseDown:
        if index == 0:
          Screen.state = 'levels_wachten_menu'
          Menu.create_levels()
        elif index == 1:
          Screen.state = 'settings'
        elif index == 2:
          Screen.running = False
    if Screen.state == 'levels_wachten_menu':
      if not(Screen.mouseDown):
        Screen.state = 'levels_menu'
    if Screen.state == 'levels_menu':
      for level in Menu.levels:
        level.render()
      if Screen.mouseDown:
        x, y = Screen.mousePos
        for level in Menu.levels:
          level.clicked(x, y)
    #if 1920 > Screen.mousePos[0] > 0:
    #  Screen.state = 'game'
  def create_levels():
    unlocked = GLOBAL.variables['settings'].unlocked_levels
    Menu.levels = [Menu.Level(i, (i+1)==unlocked) for i in range(min(GLOBAL.variables['world'].levels, unlocked))]
    #print(f'LEVELS:' + str(GLOBAL.variables['world'].levels))