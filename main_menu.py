from screen import Screen

class Menu:
  
  Screen.loadIMG('main_menu.png')
  def init():
    pass
  def render():
    Screen.renderIMG('main_menu.png', (0,0))
    if 1920 > Screen.mousePos[0] > 0:
      Screen.state = 'game'

  def stop():
    Screen.state = 'game'
    #input('elo bonjoyur')
