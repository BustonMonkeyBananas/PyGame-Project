import os
import sys
from random import *

import pygame


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
all_sprites = pygame.sprite.Group()
tile_width = tile_height = 50
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def start_screen():
    # intro_text = ["Гранжеградские приключения", ""]

    fon = pygame.transform.scale(load_image('Start.png'), (width, height))
    screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    # text_coord = 50
    # for line in intro_text:
    #     string_rendered = font.render(line, 1, pygame.Color('black'))
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 10
    #     intro_rect.top = text_coord
    #     intro_rect.x = 10
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


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
        self.rect = self.image.get_rect().move(tile_width * x + 15,
                                               tile_height * y + 5)


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
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y

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
        if player is not None:
            if pygame.sprite.spritecollideany(player, wall_group) is None:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    player.rect.top -= 50
                    if pygame.sprite.spritecollideany(player, wall_group):
                        player.rect.top += 50

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.rect.top += 50
                if pygame.sprite.spritecollideany(player, wall_group):
                    player.rect.top -= 50

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.rect.left -= 50
                if pygame.sprite.spritecollideany(player, wall_group):
                    player.rect.left += 50

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.rect.right += 50
                if pygame.sprite.spritecollideany(player, wall_group):
                    player.rect.right -= 50

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    clock.tick(50)
    screen.fill('#FFFFFF')
    all_sprites.draw(screen)
    all_sprites.update()
    tile_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()
