from time import time
from global_variables import GLOBAL
from math import sqrt, sin, cos, radians


class Entity:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.exists = True
        self.active = False
        self.size = (64, 64)

    def check_collision(self):
        if not(-200 < self.x-GLOBAL.variables["camera"].x < 2100) or not(-200 < self.y < 1280):
            self.exists = False
        for obj in GLOBAL.variables["characters"].characters + GLOBAL.variables["magic"].current_spells:
            if obj != self:
                obj_x, obj_y, obj_size = (obj.x, obj.y, obj.size)
                for punt in [(self.x, self.y), (self.x+self.size[0], self.y), (self.x, self.y+self.size[1]), (self.x+self.size[0], self.y+self.size[1])]:
                    px, py = punt
                    if obj_x < px < obj_x+obj_size[0] and obj_y < py < obj_y+obj_size[1]:
                        try:
                            obj.hit(self)
                        except AttributeError:
                            pass


class DarkMinds(Entity):
    IMGS = {}

    def __init__(self, arg, color='yellow'):
        x, y = (arg[0], arg[1])
        self.speed = 5
        try:
            self.angle = arg[2]
        except IndexError:
            self.angle = 0

        super().__init__((x, y))
        self.size = (64, 64)
        self.color = color
        # self.img = f'DarkMind_{self.color}.png'
        if not(self.color in list(DarkMinds.IMGS.keys())):
            DarkMinds.IMGS.update({self.color: GLOBAL.variables['screen'].returnImage(
                f'DarkMind_{self.color}.png')})

    def reverse(self):
        if self.color == 'blue':
            self.angle += 180
            self.speed = 8

    def activate(self):
        self.active = True
        for char in GLOBAL.variables["characters"].characters:
            try:
                if not(char.active) and sqrt((self.x-char.x)**2 + (self.y-char.y)**2) < 200:
                    char.activate()
            except AttributeError:
                pass

    def move(self):
        if self.color == 'red':
            self.x -= cos(radians(self.angle))*self.speed * \
                GLOBAL.variables["screen"].frame_speed
            self.y += sin(radians(self.angle))*self.speed * \
                GLOBAL.variables['screen'].frame_speed
            self.angle += 1
            # self.angle = self.angle%360
        elif self.color == 'blue':
            y = GLOBAL.variables["characters"].wizard.y
            if y > self.y:
                self.y += 1*GLOBAL.variables['screen'].frame_speed
            elif y < self.y:
                self.y -= 1*GLOBAL.variables['screen'].frame_speed
            self.x -= cos(radians(self.angle))*self.speed * \
                GLOBAL.variables['screen'].frame_speed
        elif self.color == 'gray':
            y = GLOBAL.variables["characters"].wizard.y
            self.check_collision()
            # if y > self.y:
            #  self.y += 1
            # elif y < self.y:
            #  self.y -= 1
            self.y += sin(radians(self.angle))*self.speed * \
                GLOBAL.variables['screen'].frame_speed
            self.x -= cos(radians(self.angle))*self.speed * \
                GLOBAL.variables['screen'].frame_speed

    def renderMe(self):
        width, height = (64, 64)
        # wizard =  GLOBAL.variables["characters"].wizard
        if not(self.active) and self.x-GLOBAL.variables["camera"].x < GLOBAL.variables["screen"].window_width and self.x-GLOBAL.variables["camera"].x > -100:
            self.activate()
        if self.active:
            self.move()
            GLOBAL.variables["screen"].blitRotate(DarkMinds.IMGS[self.color], (
                self.x-GLOBAL.variables["camera"].x, self.y), (0, 26), self.angle)
            # self.screen.blitRotate(self.arm, (arm[0]-GLOBAL.variables["camera"].x, arm[1]), (0,26), self.arm_angle)
            # GLOBAL.variables["screen"].renderIMG(self.img, (self.x-GLOBAL.variables["camera"].x, self.y))
            self.check_collision()


class DarkMindsblue(DarkMinds):
    def __init__(self, args):
        super().__init__(args, color='blue')
        self.speed = 5


class DarkMindsGray(DarkMinds):
    def __init__(self, args):
        super().__init__(args, color='gray')
        self.speed = 7


class Witch(Entity):
    def __init__(self, arg):
        super().__init__(arg)
        self.size = (513, 513)
        self.img = f'witch.png'
        self.last_attack = time()
        self.hp = 3
        self.start_angle = 50
        self.color = 0
        self.target_y = arg[1]
        self.start_y = arg[1]

    def attack(self):
        self.last_attack = time()
        if self.hp <= 0:
            if abs(self.target_y-self.y) < 1:
                self.target_y -= 100
                for i in range(self.start_angle, self.start_angle+360, 21):
                    GLOBAL.variables["characters"].createNew(
                        'darkmind_gray', self.x, self.y+100, i)
                    self.start_angle += 11
            if self.y <= -50:
                self.exists = False
        else:

            self.color = (self.color+1) % 2
            if self.color == 0:
                self.target_y = self.start_y-150
                GLOBAL.variables["characters"].createNew(
                    'darkmind_gray', self.x, self.y+130)
            else:
                self.target_y = self.start_y
                GLOBAL.variables["characters"].createNew(
                    'darkmind_blue', self.x, self.y+130)

    def renderMe(self):
        GLOBAL.variables["screen"].renderIMG(
            self.img, (self.x-GLOBAL.variables["camera"].x, self.y))
        for i in range(self.hp):
            GLOBAL.variables["screen"].renderIMG(
                "heart.png", (self.x-GLOBAL.variables["camera"].x+(i*50), self.y-10))
        # GLOBAL.variables["screen"].renderIMG(self.img, (self.x-GLOBAL.variables["camera"].x, self.y))
        if time()-self.last_attack > 2 and 0 < self.x-GLOBAL.variables["camera"].x < 1920:
            self.attack()
        if self.target_y-self.y > 1:
            self.y += GLOBAL.variables["screen"].frame_speed*2
        elif self.target_y-self.y < -1:
            self.y -= GLOBAL.variables['screen'].frame_speed*2
        # if 0 < self.x-GLOBAL.variables['camera'].x < 1920:
        #  GLOBAL.variables["characters"].wizard.x = max(self.x-1920, GLOBAL.variables["characters"].wizard.x)
        # self.check_collision()

    def hit(self, obj):
        if 'DarkMinds' in str(type(obj)):
            if obj.angle == 180 and obj.exists:
                obj.exists = False
                self.hp -= 1

        if type(obj) == GLOBAL.variables["characters"].wizard:
            GLOBAL.variables["world"].die()


class Gromott(Entity):
    def __init__(self, args):
        super().__init__(args)
        self.spawn_time = time()
        self.direction = 'up'
        self.spawn_y = self.y

    def renderMe(self):
        if self.direction == 'up':
            self.y -= 3*GLOBAL.variables['screen'].frame_speed
        else:
            self.y += 3*GLOBAL.variables['screen'].frame_speed

        if self.y < self.spawn_y:
            self.direction = 'down'
        if self.y > self.spawn_y+500:
            self.direction = 'up'

        GLOBAL.variables['screen'].renderIMG(
            'stone.png', (self.x-GLOBAL.variables["camera"].x, self.y))


class Pumpkin(Entity):
    def __init__(self, args):
        super().__init__(args)
        self.time = 0

    def rage(self):
        self.target_y = 0
        self.start_angle = 0
        for i in range(self.start_angle, self.start_angle+360, 21):
            GLOBAL.variables["characters"].createNew(
                'darkmind_gray', self.x, self.y+100, i)
            self.start_angle += 11
        self.exists = False

    def renderMe(self):
        if sqrt((self.x-GLOBAL.variables['characters'].wizard.x)**2 + (self.y-GLOBAL.variables['characters'].wizard.y)**2) < 200:
            self.time += GLOBAL.variables['screen'].frame_speed
        if self.time > 40:
            self.rage()
        GLOBAL.variables['screen'].renderIMG(
            'stone.png', (self.x-GLOBAL.variables['camera'].x, self.y))


class Cauldron(Entity):
    def __init__(self, args):
        super().__init__(args)
        slef.exists = False

    def RenderMe(self):
        pass


class Gamaru(Entity):
    def __init__(self, args):
        super().__init__(args)
        self.size = (175, 50)
        self.y_speed = 0
        self.jumped = True

    def renderMe(self):
        block = GLOBAL.variables['world'].get_block(
            self.x, self.y+self.size[1])
        if not(block in GLOBAL.variables['world'].standables):
            self.y_speed += GLOBAL.variables["screen"].frame_speed/2
        else:
            self.jumped = False
        if not self.jumped:
            self.jumped = True
            self.y_speed = -100
        self.y += self.y_speed
        GLOBAL.variables['screen'].renderIMG(
            'gamaru.png', (self.x-GLOBAL.variables['camera'].x, self.y))
