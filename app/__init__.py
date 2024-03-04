'''
Корень приложения.
'''
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
fps = settings["window"]["fps"]

run = True # индикатор работы

scale = 1.0
scale_timer = 0

observer = None

# TEST.entities

entities = Group()
moving_entities = Group()

border_horizontal_texture = pygame.Surface((1000, 50))
border_vertical_texture = pygame.Surface((50, 1000))
border_horizontal_texture.fill((255,255,255))
border_vertical_texture.fill((255,255,255))

border_top = Sprite(border_horizontal_texture, (50, 0), clock, None, entities)
border_bottom = Sprite(border_horizontal_texture, (50, 1000 + 50), clock, None, entities)
border_left = Sprite(border_vertical_texture, (0, 50), clock, None, entities)
border_right = Sprite(border_vertical_texture, (1000 + 50, 50), clock, None, entities)

player_texture = pygame.Surface((10,10))
obstacle_texture = pygame.Surface((randint(5, 200), randint(5, 200)))
player_texture.fill((255,255,255))
obstacle_texture.fill((255,255,255))

player = Entity(player_texture,
                (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                clock,
                gameKeyController,
                None, # pygame.Rect(20,20,30,30),
                entities, moving_entities,
                maxacceleration=5000,
                maxspeed=500)

creature = Entity(player_texture,
                  (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                  clock,
                  gameRandController,
                  None,
                  entities, moving_entities,
                  maxacceleration=3000,
                  maxspeed=200,
                  func=print)

obstacle = Sprite(obstacle_texture,
                      (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                      clock,
                      None,
                      entities)

observer = player

# TEST.DEBUG_PANEL

pygame.font.init()
font = pygame.font.Font(None, 24)