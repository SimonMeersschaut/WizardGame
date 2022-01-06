
from time import time
# from characters import Characters
from characters import DarkMinds
from global_variables import GLOBAL
from screen import Screen
from math import sqrt, cos, sin, radians, degrees, atan


class Shield:
    # MAX_TIME = 5
    ICON_IMAGE = 'shield_icon.png'

    def __init__(self, x, y):
        self.image = 'Shield.png'
        self.x = x+30
        self.y = y
        self.exists = True
        self.size = (64, 64)
        self.created = time()

    def render(self):
        # if time()-self.created > Shield.MAX_TIME:
        #    self.exists = False
        Screen.renderIMG(
            self.image, (self.x-GLOBAL.variables["camera"].x, self.y))

    def hit(self, obj):
        if 'DarkMinds' in str(type(obj)):
            # obj.direction += 180
            obj.reverse()
            self.exists = False

    def cancel(self):
        self.exists = False


class Shoot:
    MAX_TIME = 5

    BACKFIRE = 10
    SPEED = 0.1

    def __init__(self, x, y, long_press=False):
        if long_press:
            print('LONG PRESS!!')
        self.x = x
        self.y = y
        self.long_press = long_press
        self.exists = True
        self.size = (GLOBAL.variables['world'].square_size,
                     GLOBAL.variables['world'].square_size)
        # if long_press:
        #    self.size = (self.size[0]*2, self.size[1]*2)
        self.image = 'shoot.png'
        self.created = time()
        for x in range(int(self.x), int(self.x)-self.direction[0]*Shoot.BACKFIRE*2, GLOBAL.variables['world'].square_size):
            for y in range(int(self.y), int(self.y)-self.direction[1]*Shoot.BACKFIRE*2, GLOBAL.variables['world'].square_size):
                if GLOBAL.variables['world'].get_block(x, y) in GLOBAL.variables['world'].grounds:
                    self.exists = False
        if self.exists:
            GLOBAL.variables['characters'].wizard.x_speed = self.direction[0]*Shoot.BACKFIRE
            GLOBAL.variables['characters'].wizard.y_speed = self.direction[1]*Shoot.BACKFIRE
        # print(GLOBAL.variables['characters'].wizard.x_speed)

    def render(self):
        if time()-self.created > Shoot.MAX_TIME or self.y > 1920 or self.x < 0:
            self.exists = False
        Screen.renderIMG(
            self.image, (self.x-GLOBAL.variables["camera"].x, self.y))
        self.x -= Shoot.BACKFIRE/4 * \
            self.direction[0]*GLOBAL.variables["screen"].frame_speed
        self.y -= Shoot.BACKFIRE/4 * \
            self.direction[1]*GLOBAL.variables["screen"].frame_speed
        if GLOBAL.variables['world'].get_block(self.x, self.y) == 'marmer':
            GLOBAL.variables['world'].delete_block(self.x, self.y)
            # GLOBAL.variables['world'].map = None
        # else:
        #    print(GLOBAL.variables['world'].get_block(self.x, self.y))

    def hit(self, obj):
        if type(obj) == DarkMinds:
            obj.exists = False
            self.exists = False


class Shoot_left(Shoot):
    LONG_PRESS_TIME = 5

    def __init__(self, x, y, long_press=False):
        self.direction = (1, 0)
        super().__init__(x, y, long_press=long_press)


class Shoot_right(Shoot):
    LONG_PRESS_TIME = 5

    def __init__(self, x, y, long_press=False):
        self.direction = (-1, 0)
        super().__init__(x, y, long_press=long_press)


class Shoot_up(Shoot):
    LONG_PRESS_TIME = 5

    def __init__(self, x, y, long_press=False):
        self.direction = (0, 1)
        super().__init__(x, y, long_press=long_press)


class Shoot_down(Shoot):
    LONG_PRESS_TIME = 5

    def __init__(self, x, y, long_press=False):
        self.direction = (0, -1)
        super().__init__(x, y, long_press=long_press)


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
            # GLOBAL.variables['characters'].wizard.x_speed += distance
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


class Floor():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exists = True
        self.size = (32, 32)

    def render(self):
        pass


class Magic:
    # SPELLS
    # CODE:(OBJECT, MP)

    SPELLS = {
        'none': {},
        'green': [
            {'object': Dash_right, 'points': 1},
            {'object': Dash_left, 'points': 1},
            {'object': Dash_up, 'points': 1},
            {'object': Dash_down, 'points': 1},
            {'object': Floor, 'points': 1}
            # "14":(None, 0)
        ],
        'red': [
            {'object': Shield, 'points': 1},
            {'object': Shoot_right, 'points': 1},
            {'object': Shoot_left, 'points': 1},
            {'object': Shoot_up, 'points': 1},
            {'object': Shoot_down, 'points': 1}
        ]
    }

    points = 0
    refreshed = 0
    spawned = False
    used_balls = False
    start_position = (0, 0)
    mouse_down_time = False
    selected_spell = None
    injuring = False

    injuring_last_index = None
    INJURING_TIME_SPEED = 0.05
    CIRCLE_DIST = 50
    CIRCLE_RADIUS = 20
    COLORS = {
        'movement': (0, 0, 255)
    }
    # VARIABLES

    def init():
        Magic.points = 4
        Magic.mouse_down = True
        Magic.mouse_down_time = None
        # Magic.available_spels = []  # spells available at the time
        Magic.current_spells = []  # spells (rendering) in the world right now
        Magic.mode = 'red'

        # Magic.CIRCLE_OFFSET = (Magic.CIRCLE_DIST*1.5, Magic.CIRCLE_DIST*2.5)
        # Magic.combination = None

        # Generate ball positions
        #  Magic.activated_balls = []
        #  Magic.ball_positions = []
        #   for y in range(-2*Magic.CIRCLE_DIST, 1*Magic.CIRCLE_DIST, Magic.CIRCLE_DIST):
        #      for x in range(-1*Magic.CIRCLE_DIST, 2*Magic.CIRCLE_DIST, Magic.CIRCLE_DIST):
        #          Magic.ball_positions.append(
        #              (x+Magic.CIRCLE_OFFSET[0], y+Magic.CIRCLE_OFFSET[1]))

    @Screen.onRender('game')
    def render():
        # print([
        #    available_spell['object'].__name__ for available_spell in Magic.SPELLS[Magic.mode]])

        unlocked_spells = [spell for spell in GLOBAL.variables["settings"].unlocked_spells if spell in [
            available_spell['object'].__name__ for available_spell in Magic.SPELLS[Magic.mode]]]
        # if GLOBAL.variables["settings"].k_enchant in Screen.keys and not Magic.injuring:
        #    Magic.injuring = True
        #    Magic.mouse_down_time = False
        # elif not GLOBAL.variables['screen'].mouseDown and Magic.mouse_down_time:
        #    Magic.injuring = False
        #    Magic.mouse_down_time = time()

        if GLOBAL.variables["settings"].k_enchant in Screen.keys:
            Magic.injuring = True
            # if GLOBAL.variables["screen"].time_speed != 0.1:
            GLOBAL.variables["screen"].time_speed = Magic.INJURING_TIME_SPEED
            P1 = (GLOBAL.variables["screen"].window_width/2,
                  GLOBAL.variables["screen"].window_height/2)
            P2 = GLOBAL.variables["screen"].mousePos
            angle = 0
            if P2[0] > P1[0]:
                angle = degrees(atan((P2[1]-P1[1])/(P2[0]-P1[0])))
            elif P2[0] == P1[0]:
                if P2[1] > P1[1]:
                    angle = 90
                if P2[1] > P1[1]:
                    angle = 270
            elif P2[0] < P1[0]:
                angle = 180+degrees(atan((P2[1]-P1[1])/(P2[0]-P1[0])))
            if angle < 0:
                angle = 360-abs(angle)

        # try:
        #    angle = degrees(atan(-y_delta/x_delta))
        #    if y_delta > 0:
        #        angle = 270+angle
        #    print(angle)
        # except ZeroDivisionError:  # if the cursor didn't move at all
        #    angle = 0
        #    print('no angle')
            angle_1 = 0
            for index, name in enumerate(unlocked_spells):
                angle_2 = angle_1 + (360/len(unlocked_spells))

                # if len(unlocked_spells) > 1:
                #    angle_2 -= 5
                #    angle_1 += 5

                if angle_1 < angle < angle_2:  # when hovering
                    color = (120, 120, 120)
                    if Magic.injuring_last_index != index or not Magic.mouse_down_time:
                        Magic.mouse_down_time = time()
                    Magic.injuring_last_index = index

                else:  # default color
                    color = (135, 135, 135)

                if 'shield' in name.lower():
                    for spell in Magic.current_spells:
                        if type(spell) == Shield:  # if another shield is already activated
                            color = (100, 100, 100)
                middle_angle = (angle_1+angle_2)/2
                x = 1920/2 + cos(radians(middle_angle)) * \
                    (10)  # +(angle-middle_angle)
                y = 1080/2 + sin(radians(middle_angle)) * \
                    (10)
                # print(angle_1)
                Screen.draw_slice(x, y, angle_1=angle_1+5,
                                  angle_2=angle_2-5, radius=200, color=color)
                # angle_1 += (360-5*(len(unlocked_spells)-1))

                # if angle_1 < angle < angle_2:
                #    if Magic.mouse_down_time:
                #        if time()-Magic.mouse_down_time > 0.1:
                #            # print(Magic.mouse_down_time)
                #            # print('f'+str(Magic.get_spell_by_name(unlocked_spells[index])[
                #            #    'object'].LONG_PRESS_TIME))
                #            # print((time()-Magic.mouse_down_time))
                #            try:
                #                radius = round(
                #                    200*min(1, ((time()-Magic.mouse_down_time)/Magic.get_spell_by_name(name)['object'].LONG_PRESS_TIME)))
                #                # print(radius)
                #                Screen.draw_slice(x, y, angle_1=angle_1+5,
                #                                  angle_2=angle_2-5, radius=radius, color=(0, 0, 0))
                #            except AttributeError:
                #                pass
                try:
                    image = Magic.get_spell_by_name(name)['object'].ICON_IMAGE
                    x = 1920/2 + cos(radians((angle_1+angle_2)/2))*50
                    y = 1080/2 + sin(radians((angle_1+angle_2)/2))*50
                    GLOBAL.variables["screen"].renderIMG(image, (x, y))
                except AttributeError:
                    pass
                angle_1 += 360/len(unlocked_spells)  # /len(unlocked_spells)
            Magic.selected_spell = unlocked_spells[Magic.injuring_last_index]
        else:
            GLOBAL.variables["screen"].time_speed = 1
            if Magic.injuring:
                Magic.injuring = False

        if Magic.mouse_down and GLOBAL.variables["screen"].mouseDown:
            Magic.mouse_down = False
            Magic.mouse_down_time = time()
        if not GLOBAL.variables["screen"].mouseDown:
            print('mouse')
            if Magic.injuring_last_index != None:
                print('i,ndex')
                available = True
                if not Magic.mouse_down:  # and Magic.injuring
                    Magic.mouse_down = True
                    if 'shield' in Magic.selected_spell.lower():
                        for spell in Magic.current_spells:
                            if type(spell) == Shield:
                                available = False
                                print('!CANCELED........')
                                spell.cancel()
                    if available:
                        try:
                            long_press_time = Magic.get_spell_by_name(
                                Magic.selected_spell)['object'].LONG_PRESS_TIME
                        except AttributeError:
                            long_press_time = False
                        if long_press_time and time()-Magic.mouse_down_time > long_press_time:

                            Magic.perform_spell(
                                Magic.selected_spell, long_press=True)
                        else:
                            Magic.perform_spell(
                                Magic.selected_spell)
            #Magic.mouse_down_time = None
            #Magic.injuring = False

        # else:
        #    GLOBAL.variables["screen"].time_speed = 1
#
        #    Magic.injuring = True
        #    Magic.mouse_down_time = False

        # colors = {
        #    None: [(0, 0, 0), (120, 120, 120)],
        #    'right': [(20, 20, 20), (200, 200, 200)],
        #    'no points': [(80, 80, 80), (255, 100, 100)]
        # }
        # autocomplete = Magic.autocomplete()
        # if Magic.injuring:
        #    for index, position in enumerate(Magic.ball_positions):
        #        if not(GLOBAL.variables['characters'].wizard.touched_ground):
        #            ball_color = (50, 0, 0)
        #        else:
        #            if index in Magic.activated_balls:
        #                ball_color = colors[Magic.combination][1]
        #            else:
        #                ball_color = colors[Magic.combination][0]
        #        # if index in autocomplete:
        #        #  ball_color = (255,255,255)
        #        Screen.draw_circle(position, radius=Magic.CIRCLE_RADIUS,
        #                           border_width=Magic.CIRCLE_RADIUS, color=ball_color)
        #    Magic.check_balls()
        # if time()-Magic.spell_ended > 5:
        #    if Magic.mode != 'none':
        #        x = 1915-(Magic.points*100)
        #        for i in range(Magic.points):
        #            GLOBAL.variables['screen'].renderIMG('spell.png', (x, 20))
        #            x += 100
        #    # if Magic.points < 50:
        #    #  Magic.points += Screen.frame_speed*max(time()-Magic.last_spell, 5)
        for spell in Magic.current_spells:
            if spell.render and spell.exists:
                spell.render()
            else:
                Magic.current_spells.remove(spell)
        # RENDER LOADING BAR
        # x, y = (GLOBAL.variables['screen'].window_width-210, 10)
        # GLOBAL.variables['screen'].draw_rect(
        #    Screen.window_width-220, y, Magic.points*2, 40)

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

    def get_spell_by_name(spell_name):
        for spell in Magic.SPELLS[Magic.mode]:
            if spell['object'].__name__ == spell_name:
                return spell
            # else:
            #    print(spell['object'].__name__)

    def perform_spell(spell_name, long_press=False):
        print(spell_name)
        spell = Magic.get_spell_by_name(spell_name)
        if spell != None:
            try:
                Magic.current_spells.append(spell['object'](
                    GLOBAL.variables['characters'].wizard.x+63, GLOBAL.variables['characters'].wizard.y+24, long_press=long_press))
            except TypeError:
                Magic.current_spells.append(spell['object'](
                    GLOBAL.variables['characters'].wizard.x+63, GLOBAL.variables['characters'].wizard.y+24))
    # def check_spell():
    #    wizard = GLOBAL.variables['characters'].wizard
    #    spell_combination = ''.join([str(number)
    #                                 for number in Magic.activated_balls])
    #    if wizard.touched_ground:
    #        for spell_name in Magic.SPELLS[Magic.mode]:
    #            obj, spell_points = Magic.SPELLS[Magic.mode][spell_name]
    #            if spell_combination == spell_name:
    #                Magic.used = True
    #                if Magic.points >= spell_points:
    #                    Magic.points -= spell_points
    #                    if obj != None:
    #                        Magic.activated_balls = []
    #                        Magic.current_spells.append(obj(
    #                            GLOBAL.variables['characters'].wizard.x+63, GLOBAL.variables['characters'].wizard.y+24))
    #                        Magic.spawned = True
    #                        Magic.last_spell = time()
    #                        wizard.touched_ground = False
