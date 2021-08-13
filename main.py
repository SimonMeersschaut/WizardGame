from magic import Magic
from characters import Characters
from screen import Screen, Camera
Screen.init()
from world import World
World.init()
from settings import Settings
from main_menu import Menu
from global_variables import GLOBAL

GLOBAL.variables.update({"screen":Screen, "world":World, "settings":Settings, "main_menu":Menu, "characters":Characters, "camera":Camera, "magic":Magic})

print(dir(Settings))
for module in GLOBAL.variables.values():
  module.init()

Screen.state = 'main_menu'
while Screen.running:
  Screen.render()
Settings.save()
