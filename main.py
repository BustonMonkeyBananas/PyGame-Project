import os
import sys
import sqlite3

import pygame
import pygame_widgets
from pygame_widgets.button import Button

from settings import settings
from login import login


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
start = False
event = pygame.event.get()[0]

account = {"name": "", "password": "", "skin": 0, "difficulty": 0, "volume": 50, "level": 0}
con = sqlite3.connect("grangegrad.sqlite")
cur = con.cursor()

all_sprites = pygame.sprite.Group()
tile_width = tile_height = 100
tile_images = {
    'wall': pygame.transform.scale(load_image('box.png'), (100, 100)),
    'grass': pygame.transform.scale(load_image('grass.png'), (100, 100)),
    'asphalt': pygame.transform.scale(load_image('asphalt.jpg'), (100, 100)),
    'table': pygame.transform.scale(load_image('grangegrad.png'), (100, 100))
}
player_image = pygame.transform.scale(load_image('skins/Vitya/Vitya.png'), (70, 100))

tile_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def acc_quit():
    cur.execute('''UPDATE game SET loged = 0''')
    con.commit()

def start_screen():
    global start
    start = False
    sql = '''SELECT loged FROM game'''
    fon = pygame.transform.scale(load_image('Start.png'), (width, height))
    screen.blit(fon, (0, 0))
    settings_btn = Button(screen,200,120,90,50, margin=20, inactiveColour=(67, 69, 74),
                          hoverColour=(43, 45, 48), pressedColour=(255, 255, 255), radius=20, onClick=settings,
                          text="Настройки")
    start_btn = Button(screen, 1375, 800, 300, 120, margin=20, inactiveColour=(240, 20, 20),
                       hoverColour=(87, 0, 0), pressedColour=(0, 0, 0), radius=20, text="Начать",
                       textColour=(255, 255, 255), font=pygame.font.SysFont("Arial Black", 50), onClick=begin)

    acc_btn = Button(screen,1630,120,90,50, margin=20, inactiveColour=(20, 180, 20),
                     hoverColour=(10, 120, 10), pressedColour=(255, 255, 255), radius=20, onClick=acc_quit,
                     text="Аккаунт")

    while True:
        if cur.execute(sql).fetchall()[0][0] == 1:
            acc_btn.show()
        else:
            acc_btn.hide()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif start:
                return
        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()
        clock.tick(60)

def begin():
    global start
    sql = '''SELECT loged FROM game'''
    if cur.execute(sql).fetchall()[0][0] == 0:
        login()
    start = True

class Tile(pygame.sprite.Sprite):
    def __init__(self, typ, x, y):
        super().__init__(tile_group, all_sprites)
        self.image = tile_images[typ]
        if typ == 'wall':
            wall_group.add(self)
        self.rect = self.image.get_rect().move(tile_width * x,
                                               tile_height * y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tile_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
        self.images = []
        for imPath in os.listdir("data/skins/Vitya/walk"):
            # Appending all the images in the array
            self.images.append(pygame.transform.scale(pygame.image.load(f'data/skins/Vitya/walk/{imPath}'), (70, 100)))

        self.index = 0
        self.rect = pygame.Rect(700, 600, 150, 198)

    def update(self, *args, **kwargs):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.rect.left -= 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.rect.left += 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.rect.top -= 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.rect.top += 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        else:
            self.image = player_image

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(tile_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f'{name}/{name}.png'), (70, 100))
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
        self.images = []
        for imPath in os.listdir(f"data/{name}/walk"):
            # Appending all the images in the array
            self.images.append(pygame.transform.scale(pygame.image.load(f'data/{name}/walk/{imPath}'), (70, 100)))

class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    fon = pygame.transform.scale(load_image('Start.png'), (width, height))
    screen.blit(fon, (0, 0))
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '-':
                Tile('asphalt', x, y)
            elif level[y][x] == 't':
                Tile('table', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'S':
                Tile('asphalt', x, y)
                sanyok = NPC(x, y, "Sanyok")
    return new_player, x, y


dialogue_box_width = 400
dialogue_box_height = 200
dialogue_box_x = (1920 - dialogue_box_width) // 2
dialogue_box_y = (1080 - dialogue_box_height) // 2
dialogue_box = False


camera = Camera()
player = None
clock = pygame.time.Clock()
start_screen()
player, level_x, level_y = generate_level(load_level('map.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
            if player.rect.top in range(700, 900) and player.rect.left in range(1800, 1900):
                dialogue_box = True
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(50)
    screen.fill('#FFFFFF')
    all_sprites.draw(screen)
    all_sprites.update()
    tile_group.draw(screen)
    player_group.draw(screen)
    if dialogue_box:
        pygame.draw.rect(screen, (40, 40, 40), (400, 600, 400, 200))
    pygame.display.flip()
pygame.quit()
