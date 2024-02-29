import pygame
from tools.load_tools import loadJson
from objects.sprites import Entity, Sprite, Group
from objects.behavior.controllers import gameKeyController, appKeyController, gameRandController
from random import randint

scale = 1.0
scale_timer = 0

settings = loadJson("data/settings.json") # словарь содержащий текущие настройки

window = pygame.display.set_mode(settings["window"]["resolution"]) # главная поверхность
pygame.display.set_caption(settings["window"]["caption"])
resolution_modes = pygame.display.list_modes() # список доступных разрешений

clock = pygame.time.Clock() # объект pygame для отслеживания времени

run = True # индикатор работы

observer = None

# TEST.SPRITES

sprites = Group()

border_horizontal_texture = pygame.Surface((1000, 50))
border_vertical_texture = pygame.Surface((50, 1000))
border_horizontal_texture.fill((255,255,255))
border_vertical_texture.fill((255,255,255))

border_top = Sprite(border_horizontal_texture, (50, 0), sprites)
border_bottom = Sprite(border_horizontal_texture, (50, 1000 + 50), sprites)
border_left = Sprite(border_vertical_texture, (0, 50), sprites)
border_right = Sprite(border_vertical_texture, (1000 + 50, 50), sprites)

player_texture = pygame.Surface((70,50))
obstacle_texture = pygame.Surface((30,60))
player_texture.fill((255,255,255))
obstacle_texture.fill((255,255,255))

player = Entity(player_texture,
                (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                gameKeyController,
                sprites,
                maxacceleration=5000,
                maxspeed=700)

creature = Entity(player_texture,
                  (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                  gameRandController,
                  sprites,
                  maxacceleration=5000,
                  maxspeed=100,
                  func=print)

obstacle = Sprite(obstacle_texture,
                      (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                      sprites)

observer = player

# TEST.DEBUG_PANEL

pygame.font.init()
font = pygame.font.Font(None, 24)