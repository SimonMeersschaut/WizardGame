from math import sqrt
from json import load

from pygame.constants import SCALED
from characters import Wizard
import pygame
#from pygame.time import Clock
from time import time
from global_variables import GLOBAL
from settings import Settings


class Screen:
    render_functions = []
    BACKGROUND_COLORS = {
        'levels_menu': (12, 12, 12),
        'settings': (20, 20, 20),
        'game': (44, 165, 255)
    }
    NO_ALPHAS = ['ground.png', 'ground_bottom.png', 'spikes_bottom.png']

    @classmethod
    def init(cls):
        import pygame
        pygame.init()
        cls.imgs = {}
        cls.clock = pygame.time.Clock()
        cls.running = True
        infoObject = pygame.display.Info()
        cls.window_height = infoObject.current_h
        cls.window_width = infoObject.current_w
        cls.display = pygame.display.set_mode(
            (cls.window_width, cls.window_height), pygame.FULLSCREEN)

        cls.fonts = {100: pygame.font.Font('freesansbold.ttf', 100)}
        cls.render_functions = []
        cls.bg_color = (255, 255, 255)
        cls.state = 'starting'
        cls.events = []
        cls.event_types = []
        cls.clickListener = []
        cls.keys = []

        cls.last_time = time()
        cls.frame_speed = 0
        cls.mouseDown = False
        cls.mousePos = (0, 0)
        cls.time_speed = 1
        cls.texts = {}

    def load_background(name):
        Screen.background_image = pygame.image.load(
            f'textures/{name}').convert()

    def check_events():
        if GLOBAL.variables['book'].open:
            Screen.frame_speed = 0
        else:
            Screen.frame_speed = (
                ((time()-Screen.last_time)*60))*Screen.time_speed
        Screen.last_time = time()
        Screen.events = pygame.event.get()
        Screen.event_types = [event.type for event in Screen.events]
        if pygame.QUIT in Screen.event_types:
            Screen.running = False
        if pygame.MOUSEBUTTONDOWN in Screen.event_types:
            Screen.mouseDown = True
            x, y = pygame.mouse.get_pos()
            Screen.mousePos = (x, y)
            print((x+Camera.x, y))

            for click in Screen.clickListener:
                x1, y1, x2, y2 = click[0]
                if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                    click[1]()
        if pygame.MOUSEMOTION in Screen.event_types:
            Screen.mousePos = pygame.mouse.get_pos()
        if pygame.MOUSEBUTTONUP in Screen.event_types:
            Screen.mouseDown = False
        #Screen.keys = []
        for event in Screen.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Screen.state = 'main_menu'
                else:
                    for let in Settings.keys:
                        if let[1] == 'shift':
                            if event.key == pygame.K_LSHIFT:
                                Screen.keys.append('shift')
                        else:
                            try:
                                key = int(let[1])
                            except ValueError:
                                key = ord(let[1])
                            if key == event.key:
                                Screen.keys.append(let[1])
            elif event.type == pygame.KEYUP:
                for let in Settings.keys:
                    if let[1] == 'shift':
                        if event.key == pygame.K_LSHIFT:
                            Screen.keys.remove('shift')
                    else:
                        try:
                            key = int(let[1])
                        except ValueError:
                            key = ord(let[1])
                        if key == event.key:
                            Screen.keys.remove(let[1])

    def render():
        if Screen.state in Screen.BACKGROUND_COLORS:
            Screen.display.fill(Screen.BACKGROUND_COLORS[Screen.state])
        else:
            Screen.display.fill(Screen.bg_color)
        if Screen.state == 'game':
            Screen.display.blit(Screen.background_image, (0, 0))
            #Screen.renderIMG('background.jpg', (0-(Camera.x/25),-20), resize=2, full_scale=True, visible=1920)
            GLOBAL.variables["world"].render()
            GLOBAL.variables["characters"].render()
            GLOBAL.variables['magic'].render()
            GLOBAL.variables['book'].render()
        elif '_menu' in Screen.state:
            GLOBAL.variables["main_menu"].render()
        elif Screen.state == 'settings':
            GLOBAL.variables['settings'].render()
        GLOBAL.variables["camera"].render()
        Screen.check_events()
        pygame.display.flip()
        Screen.clock.tick(Settings.fps)
#  @classmethod
#  def update(cls):
#    for (updateState, function) in cls.update_functions:
#      if cls.state == updateState:
#        function()

    def loadIMG(path, resize=False, full_scale=False):
        path = 'textures/'+path
        if not path in Screen.imgs:
            try:
                img = pygame.image.load(path)
            except FileNotFoundError:
                input('FileNotFound: '+path)
            if resize:
                if full_scale:
                    size = img.get_rect()
                    # input(resize)
                    size = (size.size[0]*resize, size.size[1]*resize)
                    img = Screen.scale_img(img, size)
                else:

                    img = Screen.scale(img, resize)
            if path in Screen.NO_ALPHAS:
                img = img.convert()
            else:
                img = img.convert_alpha()
            Screen.imgs.update({path: img})

    # def blitIMG(img, pos):
    #  Screen.display.blit(img, pos)
    def returnImage(path):
        return pygame.image.load("textures/"+path)

    def renderIMG(path, pos, resize=False, full_scale=False, visible=128):
        if -visible < pos[0] < Screen.window_width:
            if not(path in Screen.imgs):
                Screen.loadIMG(path, resize=resize, full_scale=full_scale)
            Screen.display.blit(Screen.imgs['textures/'+path], pos)

    def renderSurface(surface, pos):
        Screen.display.blit(surface, pos)

    def blitRotate(image, pos, originPos, angle):
        surf = Screen.display
        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p)
               for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[
                   0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[
                   0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0],
                  pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        # rotate and blit the image
        surf.blit(rotated_image, origin)

        # draw rectangle around the image
        #pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)
    def scale_img(surface, size):
        return pygame.transform.scale(surface, size)

    def scale(surface, scale):
        size = (64*scale, 64*scale)
        return pygame.transform.scale(surface, size)

    def draw_rect(x1, y1, w, h, color=(0, 0, 0)):
        pygame.draw.rect(Screen.display, color, (x1, y1, w, h))

    def draw_circle(pos, radius=10, border_width=5, color=(0, 0, 0)):
        pygame.draw.circle(Screen.display, color, pos, radius, border_width)

    def draw_line(pos1, pos2, color=(0, 0, 0), width=5):
        pygame.draw.line(Screen.display, color, pos1, pos2, width)

    def render_text(text, x, y, color=(0, 0, 0), fontsize=100):
        if not(fontsize in list(Screen.fonts.keys())):
            Screen.fonts.update(
                {fontsize: pygame.font.Font('freesansbold.ttf', fontsize)})
        if not(text in Screen.texts):
            font = Screen.fonts[fontsize]
            Screen.texts.update({text: font.render(text, True, color)})
        Screen.display.blit(Screen.texts[text], (x, y))

    def click(x1, y1, x2, y2):
        def decorator(f):
            Screen.clickListener.append([[x1, y1, x2, y2], f])
            return f

        return decorator

    def onRender(state="game", **options):
        """A decorator that is used to register functions, wich should run on render time
        ex
        @Screen.onRender()
        def f():
          //render me
        """

        def decorator(f):
            Screen.render_functions.append([state, f])
            return f

        return decorator


class Camera:
    x = -200
    hor_speed = 0

    def init():
        Camera.x = -200

    def render():
        # if GLOBAL.variables["characters"].characters[0].x - Camera.x > GLOBAL.variables["screen"].window_width*0.7:
        #  if not Camera.x+1920 > GLOBAL.variables["world"].finish_x+100:
        #    Camera.hor_speed += ((GLOBAL.variables["characters"].characters[0].x - Camera.x)-(GLOBAL.variables["screen"].window_width*0.7))/100
        # if GLOBAL.variables["characters"].characters[0].x - Camera.x < GLOBAL.variables["screen"].window_width*0.2:
        #  Camera.hor_speed += ((GLOBAL.variables["characters"].characters[0].x - Camera.x)-(GLOBAL.variables["screen"].window_width*0.2))/100
        afstand_midden = ((GLOBAL.variables["characters"].characters[0].x -
                          Camera.x)-GLOBAL.variables["screen"].window_width*0.5)+100
        if afstand_midden > -100:
            Camera.x += (afstand_midden+100)/20
        elif afstand_midden < -500:  # links
            Camera.x += (afstand_midden)/100

        #Camera.hor_speed += ((GLOBAL.variables["characters"].characters[0].x - Camera.x)-(GLOBAL.variables["screen"].window_width*0.7))/500
        #Camera.x += Camera.hor_speed
