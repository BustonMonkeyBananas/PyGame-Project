import pygame
import os
import sys


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
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tile_width = tile_height = 100
tile_images = {"guitar": pygame.transform.scale(load_image('wall.jpg'), (1920, 1080))}
tile_group = pygame.sprite.Group()

def play():
    fon = pygame.transform.scale(load_image('guitar.png'), (width, height))
    screen.blit(fon, (-20, 0))
    running = True

    melody = ""
    game = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN):
                game += 1
            if game == 1:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_1):
                    pygame.mixer.Sound("data/sounds/1.0.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_2):
                    pygame.mixer.Sound("data/sounds/1.1.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_3):
                    pygame.mixer.Sound("data/sounds/1.2.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_4):
                    pygame.mixer.Sound("data/sounds/1.3.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_5):
                    pygame.mixer.Sound("data/sounds/1.4.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_6):
                    pygame.mixer.Sound("data/sounds/1.5.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_7):
                    pygame.mixer.Sound("data/sounds/1.6.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_8):
                    pygame.mixer.Sound("data/sounds/1.7.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_9):
                    pygame.mixer.Sound("data/sounds/1.8.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_0):
                    pygame.mixer.Sound("data/sounds/1.9.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_q):
                    pygame.mixer.Sound("data/sounds/2.0.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_w):
                    pygame.mixer.Sound("data/sounds/2.1.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_e):
                    pygame.mixer.Sound("data/sounds/2.2.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_r):
                    pygame.mixer.Sound("data/sounds/2.3.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_t):
                    pygame.mixer.Sound("data/sounds/2.4.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_y):
                    pygame.mixer.Sound("data/sounds/2.5.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u):
                    pygame.mixer.Sound("data/sounds/2.6.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_i):
                    pygame.mixer.Sound("data/sounds/2.7.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_o):
                    pygame.mixer.Sound("data/sounds/2.8.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_p):
                    pygame.mixer.Sound("data/sounds/2.9.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_a):
                    pygame.mixer.Sound("data/sounds/3.0.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s):
                    pygame.mixer.Sound("data/sounds/3.1.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d):
                    pygame.mixer.Sound("data/sounds/3.2.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_f):
                    pygame.mixer.Sound("data/sounds/3.3.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_g):
                    pygame.mixer.Sound("data/sounds/3.4.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_h):
                    pygame.mixer.Sound("data/sounds/3.5.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_j):
                    pygame.mixer.Sound("data/sounds/3.6.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_k):
                    pygame.mixer.Sound("data/sounds/3.7.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_l):
                    pygame.mixer.Sound("data/sounds/3.8.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_z):
                    pygame.mixer.Sound("data/sounds/4.0.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_x):
                    pygame.mixer.Sound("data/sounds/4.1.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_c):
                    pygame.mixer.Sound("data/sounds/4.2.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_v):
                    pygame.mixer.Sound("data/sounds/4.3.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_b):
                    pygame.mixer.Sound("data/sounds/4.4.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_n):
                    pygame.mixer.Sound("data/sounds/4.5.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_m):
                    pygame.mixer.Sound("data/sounds/4.6.mp3").play()
            elif game == 2:
                fon = pygame.transform.scale(load_image('drums.png'), (width, height))
                screen.blit(fon, (0, 0))
                game = 3
            elif game == 3:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                    pygame.mixer.Sound("data/sounds/kick.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    pygame.mixer.Sound("data/sounds/snare.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_1):
                    pygame.mixer.Sound("data/sounds/hat.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_2):
                    pygame.mixer.Sound("data/sounds/crash.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_3):
                    pygame.mixer.Sound("data/sounds/ride.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_q):
                    pygame.mixer.Sound("data/sounds/tom1.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_w):
                    pygame.mixer.Sound("data/sounds/tom2.mp3").play()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_e):
                    pygame.mixer.Sound("data/sounds/floortom.mp3").play()
            else:
                return
        pygame.display.flip()
        clock.tick(60)