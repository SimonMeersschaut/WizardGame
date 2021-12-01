import json
import glob
from math import modf
import pygame
from random import randint

pygame.init()
display = pygame.display.set_mode((1920, 1080))
font = pygame.font.Font("freesansbold.ttf", 35)


class Level:
    def __init__(self, data=None):
        self.inhoud = [[None for x in range(World.Config.world_size[1])] for y in range(
            World.Config.world_size[0])]
        if type(data) == list:
            for name, x, y in data:
                self.inhoud[x][y] = name

    def __iter__(self):
        return iter(self.inhoud)


class World:
    levels = []
    current_level = 0

    class Config:
        backgrounds = []
        blocks = ["monster"]
        world_size = (500, 10)
        block_size = (64, 64)
        colours = []

    def get_level(data):
        World.levels.append(Level(data))

    def return_level():
        pass

    def create_level(data):
        for level in data:
            World.levels.append(Level(data=data))

    def get_colour_of(name):
        for index, block in enumerate(World.Config.blocks):
            if name == block:
                try:
                    return World.Config.colours[index]
                except IndexError:
                    World.Config.colours.append(
                        (randint(0, 255), randint(0, 255), randint(0, 255)))
                    try:
                        return World.Config.colours[index]
                    except IndexError:
                        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def convert_world():
        world = []
        for level in enumerate(World.levels):
            level_list = []
            for x, row in enumerate(level[1]):
                for y, item in enumerate(row):
                    if item != None:
                        level_list.append((item, x, y))
            world.append(level_list)
        return world

    def render():
        x_pos = 0
        for x in World.levels[World.current_level]:
            y_pos = 0
            for y in x:
                if y != None:
                    colour = World.get_colour_of(y)
                    pygame.draw.rect(display, colour, (x_pos+offset, y_pos,
                                     World.Config.block_size[0], World.Config.block_size[1]))
                y_pos += World.Config.block_size[1]
            x_pos += World.Config.block_size[0]

    def set_block(x, y, name):
        x = int(x/World.Config.block_size[0])
        y = int(y/World.Config.block_size[1])
        World.levels[World.current_level].inhoud[x][y] = name


def save():
    print('SAVING')
    configs = [attr for attr in dir(World.Config) if (not('__' in attr))]
    config = {}
    for config_name in configs:
        config.update({config_name: getattr(World.Config, config_name)})

    json_file = {
        'config': config,
        'levels': World.convert_world()
    }
    with open('world.json', 'w+') as f:
        json.dump(json_file, f)
    exit()


def load():
    files = glob.glob('*.json')
    if len(files) > 0:
        file = files[0]
        with open(file, 'r') as f:
            inhoud = json.load(f)
        config = inhoud['config']
        for attr in config:
            setattr(World.Config, attr, config[attr])

        World.levels = [Level(data) for data in inhoud['levels']]
    else:
        save()


# World.create_level()
load()
if len(World.Config.colours) == 0:
    World.Config.colours = [(randint(0, 255), randint(
        0, 255), randint(0, 255)) for color in World.Config.blocks]

WHITE = (255, 255, 255)
running = True
selected_block_index = 0

mouse_down = False
button = 0
offset = 0
press = False
speed = 0

BUTTONS = [
    [1800, 0, 120, 50, save, (10, 10, 10)]


]

block_text = font.render("Sand", True, (10, 10, 10))

for i, button in enumerate(BUTTONS):
    color = (255-button[5][0], 255-button[5][1], 255-button[5][2])
    BUTTONS[i].append(font.render(button[4].__name__, True, color))

while running:
    display.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            buttons = [function for x1, y1, width, height, function,
                       _, _ in BUTTONS if (x1 < x < x1+width and y1 < y < y1+height)]
            if any(buttons):
                buttons[0]()
            else:
                if event.button == 4:
                    selected_block_index += 1
                    selected_block_index = selected_block_index % (
                        len(World.Config.blocks))
                elif event.button == 5:
                    selected_block_index -= 1
                else:
                    mouse_down = True
                    button = event.button
                try:
                    block_text = font.render(
                        World.Config.blocks[selected_block_index], True, (10, 10, 10))
                except:
                    pass
        if event.type == pygame.KEYDOWN:
            press = True
            if event.key == pygame.K_s:
                if World.current_level > len(World.levels):
                    World.levels.append(Level())
                World.current_level += 1
            if event.key == pygame.K_q:
                if World.current_level > 0:
                    World.current_level -= 1
            if event.key == pygame.K_a:
                speed = 5
            elif event.key == pygame.K_z:
                speed = -5
            else:
                speed = 0
        if event.type == pygame.KEYUP:
            press = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            button = event.button
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if mouse_down:
            if button == 1:
                try:
                    World.set_block(
                        x-offset, y, World.Config.blocks[selected_block_index])
                except IndexError:
                    pass
            elif button == 3:
                World.set_block(x-offset, y, None)
    if press:
        offset += speed
    World.render()
    for x1, y1, width, height, function, colour, text in BUTTONS:
        pygame.draw.rect(display, colour, (x1, y1, width, height))
        display.blit(text, (x1+10, y1))
    display.blit(block_text, (10, 10))

    pygame.display.flip()
