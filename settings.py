from json import dump
from save import Save
from os.path import exists
class Settings:
  keys = [
    ['k_left', 'q'],
    ['k_right', 'd'],
    ['k_jump', ' ']
  ]
  attrs = [
    ['fps', 30],
  ]
  for index, (name, key) in enumerate(keys):
      if name in Save.save:
        print(Save.save[name])
        keys[index][1] = Save.save[name]
  attrs = attrs + keys
  @classmethod
  def init(cls):
    for (attr, defaultValue) in cls.attrs:
      
      if attr in Save.save:
        
        setattr(cls, attr, Save.save[attr])
      else:
        setattr(cls, attr, defaultValue)
  def save():
    attrs = [attr for attr in dir(Settings) if not callable(getattr(Settings, attr)) and not attr.startswith("__") and not attr in ('attrs', 'keys')]
    print(attrs)
    obj = [(attr, getattr(Settings, attr)) for attr in attrs]
    dict = {}
    for key, value in obj:
      dict.update({key: value})
    print(obj)
    with open(Save.saveFile, 'w') as f:
      dump(dict, f)
Settings.init()