from json import dump
from save import Save
from os.path import exists
class Settings:
  keys = [
    ['k_left', 'q'],
    ['k_right', 'd'],
    ['k_jump', ' '],
    ['k_sprint', 'z'],
    ['k_ball_1', '7'],
    ['k_ball_2', '8'],
    ['k_ball_3', '9'],
    ['k_ball_4', '4'],
    ['k_ball_5', '5'],
    ['k_ball_6', '6'],
    ['k_ball_7', '1'],
    ['k_ball_8', '2'],
    ['k_ball_9', '3']
  ]
  attrs = [
    ['fps', 30],
  ]
  for index, (name, key) in enumerate(keys):
      if name in Save.save:
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
    obj = [(attr, getattr(Settings, attr)) for attr in attrs]
    dict = {}
    for key, value in obj:
      dict.update({key: value})
    with open(Save.saveFile, 'w') as f:
      dump(dict, f)
Settings.init()