from magic import Magic
from characters import Characters
from screen import Screen, Camera
from world import World
from settings import Settings
from main_menu import Menu
from global_variables import GLOBAL

GLOBAL.variables.update({"screen":Screen, "characters":Characters, "world":World, "settings":Settings, "main_menu":Menu, "camera":Camera, "magic":Magic})

for module in GLOBAL.variables.values():
  module.init()

Screen.state = 'main_menu'
while Screen.running:
  Screen.render()
Settings.save()