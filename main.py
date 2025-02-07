import os
import sys
import sqlite3

import pygame
import pygame_widgets
from pygame_widgets.button import Button
import keyboard
import time

from settings import settings
from music_game import play

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
    'wall': pygame.transform.scale(load_image('wall.jpg'), (100, 100)),
    'window': pygame.transform.scale(load_image('window.png'), (100, 100)),
    'roof': pygame.transform.scale(load_image('roof.jpg'), (100, 100)),
    'sky': pygame.transform.scale(load_image('sky.png'), (100, 100)),
    'grass': pygame.transform.scale(load_image('grass.png'), (100, 100)),
    'kust': pygame.transform.scale(load_image('kust.png'), (100, 100)),
    'kustik': pygame.transform.scale(load_image('kustik.png'), (100, 100)),
    'tree': pygame.transform.scale(load_image('tree.png'), (100, 100)),
    'flower': pygame.transform.scale(load_image('flower.png'), (100, 100)),
    'asphalt': pygame.transform.scale(load_image('asphalt.jpg'), (100, 100)),
    'table': pygame.transform.scale(load_image('grangegrad.png'), (100, 100)),
    'floor': pygame.transform.scale(load_image('floor.jpg'), (100, 100)),
    'white': pygame.transform.scale(load_image('white.jpeg'), (100, 100)),
    'scene': pygame.transform.scale(load_image('scene.jpg'), (100, 100)),
    'rightup': pygame.transform.scale(load_image('rightup.png'), (100, 100)),
    'rightdown': pygame.transform.scale(load_image('rightdown.png'), (100, 100)),
    'leftup': pygame.transform.scale(load_image('leftup.png'), (100, 100)),
    'leftdown': pygame.transform.scale(load_image('leftdown.png'), (100, 100)),
    'stairs': pygame.transform.scale(load_image('stairs.png'), (100, 100)),
    'leftstairs': pygame.transform.scale(load_image('leftstairs.png'), (100, 100)),
    'rightstairs': pygame.transform.scale(load_image('rightstairs.png'), (100, 100)),
    'hall_wall': pygame.transform.scale(load_image('hall_wall.jpg'), (100, 100)),
    'black': pygame.transform.scale(load_image('black.jpg'), (100, 100))
}
player_image = pygame.transform.scale(load_image('skins/Vitya/Vitya.png'), (70, 100))

tile_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

playlist = ["data/ost/soundtrack.mp3", "data/ost/soundtrack.mp3"]

def acc_quit():
    cur.execute('''UPDATE game SET loged = 0''')
    con.commit()

def start_screen():
    global start, playlist, event
    start = False
    sql = '''SELECT loged FROM game'''
    fon = pygame.transform.scale(load_image('Start.png'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.mixer.music.load(playlist.pop())
    pygame.mixer.music.queue(playlist.pop())
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    if event.type == pygame.USEREVENT:
        if len(playlist) > 1:
            pygame.mixer.music.queue(playlist.pop())
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
        __import__("login").login()
    pygame.mixer.music.pause()
    start = True

class Tile(pygame.sprite.Sprite):
    def __init__(self, typ, x, y):
        super().__init__(tile_group, all_sprites)
        self.image = tile_images[typ]
        if typ == 'wall' or typ == 'window' or typ == 'hall_wall' or typ == 'roof':
            wall_group.add(self)
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tile_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
        self.images = []
        for imPath in os.listdir("data/skins/Vitya/walk"):
            self.images.append(pygame.transform.scale(pygame.image.load(f'data/skins/Vitya/walk/{imPath}'), (70, 100)))

        self.index = 0
        self.rect = pygame.Rect(x, y, 150, 198)

    def update(self, *args, **kwargs):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.rect.left -= 10 if all(not pygame.sprite.collide_mask(player, i) for i in walls) else -10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.rect.left += 10 if all(not pygame.sprite.collide_mask(player, i) for i in walls) else -10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.rect.top -= 10 if all(not pygame.sprite.collide_mask(player, i) for i in walls) else -10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.rect.top += 10 if all(not pygame.sprite.collide_mask(player, i) for i in walls) else -10
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
        self.index = 0
        self.mode = False
        self.name = name
        self.x, self.y = x, y
        if name == "Vitalik":
            self.image = pygame.transform.scale(load_image(f'{name}/{name}.png'), (140, 200))
            self.rect = self.image.get_rect().move(tile_width * x - 100, tile_height * y - 90)
        elif name == "Headmaster":
            self.image = pygame.transform.scale(load_image(f'{name}/{name}.png'), (90, 150))
            self.rect = self.image.get_rect().move(tile_width * x - 50, tile_height * y - 50)
        else:
            self.image = pygame.transform.scale(load_image(f'{name}/{name}.png'), (70, 100))
            self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y)
        self.images = []
        for imPath in os.listdir(f"data/{name}/sing"):
            if name == "Vitalik":
                self.images.append(pygame.transform.scale(pygame.image.load(f'data/{name}/sing/{imPath}'), (140, 200)))
            elif name == "Headmaster":
                self.images.append(pygame.transform.scale(pygame.image.load(f'data/{name}/sing/{imPath}'), (90, 150)))
            else:
                self.images.append(pygame.transform.scale(pygame.image.load(f'data/{name}/sing/{imPath}'), (70, 100)))

    def walk(self, mode):
        if mode == "left":
            self.rect.left -= 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif mode == "right":
            self.rect.left += 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif mode == "up":
            self.rect.top -= 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif mode == "down":
            self.rect.top += 10
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        elif mode == "standing":
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            clock.tick(15)
        else:
            if self.name == "Vitalik":
                self.image = pygame.transform.scale(load_image(f'{self.name}/{self.name}.png'), (140, 200))
            elif self.name == "Headmaster":
                self.image = pygame.transform.scale(load_image(f'{self.name}/{self.name}.png'), (90, 150))
            else:
                self.image = pygame.transform.scale(load_image(f'{self.name}/{self.name}.png'), (70, 100))

    def move(self, mode):
        self.mode = mode
        self.index = (self.index + 1) % len(self.images)
        if self.mode:
            self.image = self.images[self.index]
        else:
            if self.name == "Vitalik":
                self.image = pygame.transform.scale(load_image(f'{self.name}/{self.name}.png'), (140, 200))
            elif self.name == "Headmaster":
                self.image = pygame.transform.scale(load_image(f'{self.name}/{self.name}.png'), (90, 150))
            else:
                self.image = pygame.transform.scale(load_image(f'{self.name}/{self.name}.png'), (70, 100))
        clock.tick(15)
sanyok = NPC(0, 0, "Sanyok")
vitalik = NPC(0, 0, "Vitalik")
headmster = NPC(0, 0, "Headmaster")
volodya = NPC(0, 0, "Volodya")
t = Tile("table", 0, 0)

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

walls = []
def generate_level(level, xp, yp):
    global sanyok, vitalik, headmster, volodya, t, walls
    fon = pygame.transform.scale(load_image('black.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            if level[y][x] == 'k':
                Tile('grass', x, y)
                Tile('kust', x, y)
            if level[y][x] == 'K':
                Tile('grass', x, y)
                Tile('kustik', x, y)
            if level[y][x] == 'T':
                Tile('grass', x, y)
                Tile('tree', x, y)
            if level[y][x] == '*':
                Tile('grass', x, y)
                Tile('flower', x, y)
            elif level[y][x] == '#':
                walls.append(Tile('wall', x, y))
            elif level[y][x] == 'w':
                walls.append(Tile('window', x, y))
            elif level[y][x] == 'r':
                walls.append(Tile('roof', x, y))
            elif level[y][x] == '-':
                Tile('asphalt', x, y)
            elif level[y][x] == 'n':
                Tile('sky', x, y)
            elif level[y][x] == 't':
                t = Tile('table', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = Player(xp, yp)
            elif level[y][x] == 's':
                Tile('asphalt', x, y)
                sanyok = NPC(x, y, "Sanyok")
            elif level[y][x] == 'f':
                Tile('floor', x, y)
            elif level[y][x] == 'c':
                Tile('white', x, y)
            elif level[y][x] == 'C':
                Tile('scene', x, y)
            elif level[y][x] == 'Z':
                Tile('white', x, y)
                walls.append(Tile('leftup', x, y))
            elif level[y][x] == 'z':
                Tile('white', x, y)
                walls.append(Tile('leftdown', x, y))
            elif level[y][x] == 'L':
                Tile('white', x, y)
                walls.append(Tile('rightup', x, y))
            elif level[y][x] == 'l':
                Tile('white', x, y)
                walls.append(Tile('rightdown', x, y))
            elif level[y][x] == 'j':
                Tile('floor', x, y)
                Tile('stairs', x, y)
            elif level[y][x] == '/':
                Tile('floor', x, y)
                Tile('leftstairs', x, y)
            elif level[y][x] == '\\':
                Tile('floor', x, y)
                Tile('rightstairs', x, y)
            elif level[y][x] == '!':
                walls.append(Tile('hall_wall', x, y))
            elif level[y][x] == 'b':
                Tile('black', x, y)
            elif level[y][x] == 'S':
                Tile('scene', x, y)
                sanyok = NPC(x, y, "Sanyok")
            elif level[y][x] == 'v':
                Tile('scene', x, y)
                vitalik = NPC(x, y, "Vitalik")
            elif level[y][x] == 'H':
                Tile('floor', x, y)
                headmster = NPC(x, y, "Headmaster")
            elif level[y][x] == 'V':
                Tile('asphalt', x, y)
                volodya = NPC(x, y, "Volodya")
    return new_player, x, y

def enter():
    global sd
    sd -= 1
    keyboard.press('enter')
    keyboard.release('enter')

dialogue_box = 0
sd = - 1
sanya_dialogs = ['Здарова, кент! Меня зовут Санёк.\n      Как тебе в нашем городе?', 'Тут интересно, могу провести экскурсию',
                 'Хочешь покажу своё любимое место?', 'Ну как тебе песня?', 'Это наш актовый зал, здесь мы собираемся, чтобы навалить рока',
                 'Кстати, это Виталик, он барабанщик\nОн довольно молчалив, так что не обижайся на него',
                 'Хочешь попробовать поиграть?', 'Да, такое тоже случается\nНо ты держался молодцом',
                 'Слушай, не хочешь к нам в группу "Сухой газон"?\n                       Ты бы точно вписался', '']

camera = Camera()
player = None
clock = pygame.time.Clock()
start_screen()
player, level_x, level_y = generate_level(load_level('map.txt'), 800, 800)
move = False

playlist = ["data/ost/main_ost.wav", "data/ost/main_ost.wav"]
pygame.mixer.music.load(playlist.pop())
pygame.mixer.music.queue(playlist.pop())
pygame.mixer.music.set_endevent(pygame.USEREVENT)
pygame.mixer.music.play()
if event.type == pygame.USEREVENT:
    if len(playlist) > 1:
        pygame.mixer.music.queue(playlist.pop())

def school():
    global player, level_x, level_y, dialogue_box, sd, move
    all_sprites.empty()
    tile_group.empty()
    wall_group.empty()
    player_group.empty()
    pygame.mixer.music.load("data/ost/school.mp3")
    pygame.mixer.music.play()
    fon = pygame.transform.scale(load_image('school.png'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    time.sleep(4)
    pygame.draw.rect(screen, (40, 40, 40), (400, 700, 1100, 200))
    rendered_text = pygame.font.Font(None, 40).render("Это наша гранжеградская школа номер 63", True, "white")
    text_rect = rendered_text.get_rect(center=(950, 800))
    screen.blit(rendered_text, text_rect)
    pygame.display.flip()
    time.sleep(4)
    pygame.draw.rect(screen, (40, 40, 40), (400, 700, 1100, 200))
    rendered_text = pygame.font.Font(None, 40).render("Хотя всего в городе 5 школ", True, "white")
    text_rect = rendered_text.get_rect(center=(950, 800))
    screen.blit(rendered_text, text_rect)
    pygame.display.flip()
    time.sleep(4)
    dialogue_box = 0
    player, level_x, level_y = generate_level(load_level('school.txt'), 800, 800)
    pygame.mixer.music.load("data/ost/sanyok_sing.mp3")
    pygame.mixer.music.play()
    move = True

def music_hero():
    global dialogue_box, player, level_x, level_y
    play()
    dialogue_box = 3
    player, level_x, level_y = generate_level(load_level('headmaster.txt'), 1500, 1000)

dialog = pygame.mixer.Sound('data/sounds/dialog.ogg')
spawn = pygame.mixer.Sound('data/sounds/spawn.ogg')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
            move = False
            pygame.mixer.music.pause()
            if pygame.sprite.collide_mask(player, t):
                dialogue_box = 1 if dialogue_box == 0 else 0
            if pygame.sprite.collide_mask(player, sanyok):
                dialog.play()
                if dialogue_box == 0:
                    dialogue_box = 2
                    sd += 1
                else:
                    dialogue_box = 0
                    playlist = ["data/ost/main_ost.wav", "data/ost/main_ost.wav"]
                    pygame.mixer.music.load(playlist.pop())
                    pygame.mixer.music.queue(playlist.pop())
                    pygame.mixer.music.set_endevent(pygame.USEREVENT)
                    pygame.mixer.music.play()
            if dialogue_box == 3:
                pygame.mixer.music.load('data/sounds/chase.mp3')
                pygame.mixer.music.play()
                dialogue_box = 0
                for _ in range(10):
                    headmster.walk("up")
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                for _ in range(45):
                    headmster.walk("left")
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                for _ in range(10):
                    headmster.walk("standing")
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                for _ in range(25):
                    headmster.walk("left")
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                for _ in range(10):
                    headmster.walk("standing")
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                for _ in range(10):
                    headmster.walk("down")
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                pygame.mixer.music.load('data/sounds/bonk.mp3')
                pygame.mixer.music.play()
                fon = pygame.transform.scale(load_image('black.jpg'), (width, height))
                screen.blit(fon, (0, 0))
                pygame.display.flip()
                time.sleep(3)
                pygame.mixer.music.load('data/ost/main_ost.wav')
                pygame.mixer.music.play()
                all_sprites.empty()
                wall_group.empty()
                tile_group.empty()
                player_group.empty()
                walls = []
                player, level_x, level_y = generate_level(load_level("volodya.txt"), 1500, 1000)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(50)
    screen.fill('#FFFFFF')
    all_sprites.draw(screen)
    all_sprites.update()
    if move:
        sanyok.move(move)
        vitalik.move(move)
    tile_group.draw(screen)
    player_group.draw(screen)
    if dialogue_box == 1:
        box = pygame.draw.rect(screen, (40, 40, 40), (400, 700, 1100, 200))
        rendered_text = pygame.font.Font(None, 40).render("Добро пожаловать в Великий Гранжеград\n"
                                                          "      Нижний Гранжеград через 300 км -->", True, "white")
        text_rect = rendered_text.get_rect(center=(950, 800))
        screen.blit(rendered_text, text_rect)
    if dialogue_box == 2:
        box = pygame.draw.rect(screen, (40, 40, 40), (400, 700, 1100, 200))
        rendered_text = pygame.font.Font(None, 40).render(sanya_dialogs[sd], True, "white")
        text_rect = rendered_text.get_rect(center=(950, 800))
        screen.blit(rendered_text, text_rect)
        if sd == 2:
            btn1 = Button(screen, 800, 820, 90, 50, margin=20, inactiveColour=(67, 69, 74),
                          hoverColour=(43, 45, 48), pressedColour=(255, 255, 255), radius=20, onClick=school,
                          text="ДА", textColour=(255, 255, 255))
            btn2 = Button(screen, 980, 820, 90, 50, margin=20, inactiveColour=(67, 69, 74),
                          hoverColour=(43, 45, 48), pressedColour=(255, 255, 255), radius=20, onClick=enter,
                          text="НЕТ", textColour=(255, 255, 255))
            pygame_widgets.update(pygame.event.get())
            pygame.display.flip()
        if sd == 6:
            btn1 = Button(screen, 800, 820, 90, 50, margin=20, inactiveColour=(67, 69, 74),
                          hoverColour=(43, 45, 48), pressedColour=(255, 255, 255), radius=20, onClick=music_hero,
                          text="ДА", textColour=(255, 255, 255))
            btn2 = Button(screen, 980, 820, 90, 50, margin=20, inactiveColour=(67, 69, 74),
                          hoverColour=(43, 45, 48), pressedColour=(255, 255, 255), radius=20, onClick=enter,
                          text="НЕТ", textColour=(255, 255, 255))
            pygame_widgets.update(pygame.event.get())
            pygame.display.flip()
        if sd == 9:
            time.sleep(3)
            dialogue_box = 4
    if dialogue_box == 3:
        spawn.play()
        box = pygame.draw.rect(screen, (40, 40, 40), (400, 700, 1100, 200))
        rendered_text = pygame.font.Font(None, 40).render("Сколько можно тут орать? А ну пошли прочь!!!", True, "white")
        text_rect = rendered_text.get_rect(center=(950, 800))
        screen.blit(rendered_text, text_rect)
    if dialogue_box == 4:
        for _ in range(50):
            volodya.walk("left")
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
        dialogue_box = 5
    if dialogue_box == 5:
        volodya.move(False)
        all_sprites.update()
        player_group.update()
        tile_group.update()
        box = pygame.draw.rect(screen, (40, 40, 40), (400, 700, 1100, 200))
        rendered_text = pygame.font.Font(None, 40).render("Добрый вечер музыканты! Позвонить дадите?", True, "white")
        text_rect = rendered_text.get_rect(center=(950, 800))
        screen.blit(rendered_text, text_rect)
        pygame.display.flip()
        time.sleep(3)
        spawn.play()
        fon = pygame.transform.scale(load_image('black.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        rendered_text = pygame.font.Font(None, 80).render("TO BE CONTINUED", True, "red")
        text_rect = rendered_text.get_rect(center=(950, 530))
        screen.blit(rendered_text, text_rect)
        pygame.display.flip()
        time.sleep(5)
        running = False
    pygame.display.flip()
pygame.quit()