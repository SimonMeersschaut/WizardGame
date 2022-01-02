from time import time
#from characters import Characters
from characters import DarkMinds
from global_variables import GLOBAL
from screen import Screen
from math import sqrt


class Shield:
    MAX_TIME = 5

    def __init__(self, x, y):
        self.image = 'Shield.png'
        self.x = x+30
        self.y = y
        self.exists = True
        self.size = (64, 64)
        self.created = time()

    def render(self):
        if time()-self.created > Shield.MAX_TIME:
            self.exists = False
        Screen.renderIMG(
            self.image, (self.x-GLOBAL.variables["camera"].x, self.y))

    def hit(self, obj):
        if 'DarkMinds' in str(type(obj)):
            #obj.direction += 180
            obj.reverse()
            self.exists = False


class Shoot:
    MAX_TIME = 5
    BACKFIRE = 40

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exists = True
        self.size = (64, 64)
        self.image = 'shoot.png'
        self.created = time()
        for x in range(int(self.x), int(self.x)-self.direction[0]*Shoot.BACKFIRE*2, GLOBAL.variables['world'].square_size):
            for y in range(int(self.y), int(self.y)-self.direction[1]*Shoot.BACKFIRE*2, GLOBAL.variables['world'].square_size):
                if GLOBAL.variables['world'].get_block(x, y) in GLOBAL.variables['world'].grounds:
                    self.exists = False
        if self.exists:
            GLOBAL.variables['characters'].wizard.x_speed += self.direction[0]*Shoot.BACKFIRE
            GLOBAL.variables['characters'].wizard.y_speed += self.direction[1]*Shoot.BACKFIRE
        print(GLOBAL.variables['characters'].wizard.x_speed)

    def render(self):
        if time()-self.created > Shield.MAX_TIME:
            self.exists = False
        Screen.renderIMG(
            self.image, (self.x-GLOBAL.variables["camera"].x, self.y))
        self.x -= Shoot.BACKFIRE/4*self.direction[0]
        self.y -= Shoot.BACKFIRE/4*self.direction[1]
        if GLOBAL.variables['world'].get_block(self.x, self.y) == 'marmer':
            GLOBAL.variables['world'].delete_block(self.x, self.y)
            #GLOBAL.variables['world'].map = None
        else:
            print(GLOBAL.variables['world'].get_block(self.x, self.y))

    def hit(self, obj):
        if type(obj) == DarkMinds:
            obj.exists = False
            self.exists = False


class Shoot_left(Shoot):
    def __init__(self, x, y):
        self.direction = (1, 0)
        super().__init__(x, y)


class Shoot_right(Shoot):
    def __init__(self, x, y):
        self.direction = (-1, 0)
        super().__init__(x, y)


class Shoot_up(Shoot):
    def __init__(self, x, y):
        self.direction = (0, 1)
        super().__init__(x, y)


class Shoot_down(Shoot):
    def __init__(self, x, y):
        self.direction = (0, -1)
        super().__init__(x, y)


class Dash:
    def __init__(self, x, y):
        possible = True
        distance = 50
        for x in range(int(GLOBAL.variables['characters'].wizard.x), int(GLOBAL.variables['characters'].wizard.x+(distance*self.direction[0])), int(GLOBAL.variables['world'].square_size/2)):
            for y in range(int(GLOBAL.variables['characters'].wizard.y), int(GLOBAL.variables['characters'].wizard.y+(distance*self.direction[1])), int(GLOBAL.variables['world'].square_size/2)):
                block = GLOBAL.variables['world'].get_block(x, y)
                if block in GLOBAL.variables['world'].grounds or block in GLOBAL.variables['world'].standables:
                    possible = False
        if possible:
            #GLOBAL.variables['characters'].wizard.x_speed += distance
            GLOBAL.variables['characters'].wizard.x_speed = self.direction[0]*distance
            GLOBAL.variables['characters'].wizard.y_speed = self.direction[1]*distance
            print('DASH')
            # input(GLOBAL.variables['characters'].wizard.y_speed)
        self.exists = False

    def render(self):
        pass


class Dash_left(Dash):
    def __init__(self, x, y):
        self.direction = (-1, 0)
        super().__init__(x, y)


class Dash_right(Dash):
    def __init__(self, x, y):
        self.direction = (1, 0)
        super().__init__(x, y)


class Dash_up(Dash):
    def __init__(self, x, y):
        self.direction = (0, -1)
        super().__init__(x, y)


class Dash_down(Dash):
    def __init__(self, x, y):
        self.direction = (0, 1)
        super().__init__(x, y)


class Magic:
    # SPELLS
    #CODE:(OBJECT, MP)
    SPELLS = {
        'none': {},
        'green': {
            '45': (Dash_right, 1),
            '34': (Dash_left, 1),
            '14': (Dash_up, 1),
            '47': (Dash_down, 1)
            # "14":(None, 0)
        },
        'red': {
            "03": (Shield, 1),
            '45': (Shoot_right, 1),
            '34': (Shoot_left, 1),
            '14': (Shoot_up, 1),
            '47': (Shoot_down, 1)
        }
    }

    points = 0
    refreshed = 0
    spawned = False
    used_balls = False
    last_spell = 0
    spell_ended = 0
    CIRCLE_DIST = 50
    CIRCLE_RADIUS = 20
    COLORS = {
        'movement': (0, 0, 255)
    }
    # VARIABLES

    def init():
        Magic.points = 4
        Magic.injuring = True
        Magic.current_spells = []
        Magic.mode = 'none'
        #Magic.conjuring = "efsdf"

        # Screen.window_height-Magic.CIRCLE_DIST/2
        Magic.CIRCLE_OFFSET = (Magic.CIRCLE_DIST*1.5, Magic.CIRCLE_DIST*2.5)
        Magic.combination = None

        # Generate ball positions
        Magic.activated_balls = []
        Magic.ball_positions = []
        for y in range(-2*Magic.CIRCLE_DIST, 1*Magic.CIRCLE_DIST, Magic.CIRCLE_DIST):
            for x in range(-1*Magic.CIRCLE_DIST, 2*Magic.CIRCLE_DIST, Magic.CIRCLE_DIST):
                Magic.ball_positions.append(
                    (x+Magic.CIRCLE_OFFSET[0], y+Magic.CIRCLE_OFFSET[1]))
        Magic.current_spells = []

    @Screen.onRender('game')
    def render():
        print(GLOBAL.variables['screen'].keys)
        if 'a' in GLOBAL.variables['screen'].keys:
            print('e')
            GLOBAL.variables["screen"].time_speed = 0.1
        else:
            GLOBAL.variables["screen"].time_speed = 1
        colors = {
            None: [(0, 0, 0), (120, 120, 120)],
            'right': [(20, 20, 20), (200, 200, 200)],
            'no points': [(80, 80, 80), (255, 100, 100)]
        }
        #autocomplete = Magic.autocomplete()
        if Magic.injuring:
            for index, position in enumerate(Magic.ball_positions):
                if not(GLOBAL.variables['characters'].wizard.touched_ground):
                    ball_color = (50, 0, 0)
                else:
                    if index in Magic.activated_balls:
                        ball_color = colors[Magic.combination][1]
                    else:
                        ball_color = colors[Magic.combination][0]
                # if index in autocomplete:
                #  ball_color = (255,255,255)
                Screen.draw_circle(position, radius=Magic.CIRCLE_RADIUS,
                                   border_width=Magic.CIRCLE_RADIUS, color=ball_color)
            Magic.check_balls()
        if time()-Magic.spell_ended > 5:
            if Magic.mode != 'none':
                x = 1915-(Magic.points*100)
                for i in range(Magic.points):
                    GLOBAL.variables['screen'].renderIMG('spell.png', (x, 20))
                    x += 100
            # if Magic.points < 50:
            #  Magic.points += Screen.frame_speed*max(time()-Magic.last_spell, 5)
        for spell in Magic.current_spells:
            if spell.render and spell.exists:
                spell.render()
            else:
                Magic.current_spells.remove(spell)
        # RENDER LOADING BAR
        x, y = (GLOBAL.variables['screen'].window_width-210, 10)
        #GLOBAL.variables['screen'].draw_rect(Screen.window_width-220, y, Magic.points*2, 40)

    def get_dist(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        b = x2-x1
        c = y2-y1
        a = sqrt(b**2 + c**2)
        return a
    # def autocomplete():
    #  autocomplete = []
    #  activated = ''.join([str(number) for number in Magic.activated_balls])
    #  for spell in Magic.SPELLS[Magic.mode]:
    #    if activated in spell:
    #      #print('magic autocomplete')
    #      broke = False
    #      for index, (letterSPELL, letterBALL) in enumerate(zip(spell, activated)):
    #        if not broke:
    #          #print(type(letterSPELL), type(letterBALL))
    #          if letterSPELL != letterBALL:
    #
    #            if index != 0:
    #              #print('append',letterSPELL)
    #              autocomplete.append(letterSPELL)
    #            broke = True
    #  return autocomplete

    def check_balls():
        tijd = time()

        if tijd-Magic.last_spell > .5:
            keys = [setting_key[1]
                    for setting_key in GLOBAL.variables["settings"].keys if 'ball_' in setting_key[0]]
            balls = [index for index, key in enumerate(
                keys) if key in GLOBAL.variables["screen"].keys]

            for ball in balls:
                if ball not in Magic.activated_balls:
                    Magic.activated_balls.append(ball)
                 #    Magic.refreshed = tijd
                 #    #Magic.used = False
            Magic.activated_balls = sorted(Magic.activated_balls)
            if (tijd-Magic.refreshed > 1 and balls == []):
                Magic.activated_balls = []
            #  #Magic.used = False
            #  #Magic.spawned = False
        # if Screen.mouseDown:
        #  for index, position in enumerate(Magic.ball_positions):
        #    dist = Magic.get_dist(position, Screen.mousePos)
        #    if dist <= Magic.CIRCLE_RADIUS:
        #      if len(Magic.activated_balls) == 0 or index not in Magic.activated_balls:
        #        Magic.activated_balls.append(int(index))
        #
        # else:
        Magic.check_spell()
        #  Magic.activated_balls = []
        Magic.ball_color()
        GLOBAL.variables['characters'].wizard.floating = bool(''.join([str(number) for number in Magic.activated_balls]) == '14' and (
            GLOBAL.variables['characters'].wizard.y_speed > 3 or GLOBAL.variables['characters'].wizard.floating) and Magic.mode == 'movement')

    def ball_color():
        combination = None
        spell_combination = ''.join([str(number)
                                    for number in Magic.activated_balls])
        for spell_name in Magic.SPELLS[Magic.mode]:
            obj, spell_points = Magic.SPELLS[Magic.mode][spell_name]
            if spell_combination == spell_name:
                if Magic.points >= spell_points:
                    combination = 'right'
                else:
                    if not combination:
                        combination = 'no points'
        Magic.combination = combination

    def check_spell():
        wizard = GLOBAL.variables['characters'].wizard
        spell_combination = ''.join([str(number)
                                    for number in Magic.activated_balls])
        if wizard.touched_ground:
            for spell_name in Magic.SPELLS[Magic.mode]:
                obj, spell_points = Magic.SPELLS[Magic.mode][spell_name]
                if spell_combination == spell_name:
                    Magic.used = True
                    if Magic.points >= spell_points:
                        Magic.points -= spell_points
                        if obj != None:
                            Magic.activated_balls = []
                            Magic.current_spells.append(obj(
                                GLOBAL.variables['characters'].wizard.x+63, GLOBAL.variables['characters'].wizard.y+24))
                            Magic.spawned = True
                            Magic.last_spell = time()
                            wizard.touched_ground = False
